from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal
from smtplib import SMTPDataError
from threading import Event
from unittest.mock import patch
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import DatabaseError, connections
from django.test import TransactionTestCase
from django.utils import timezone

from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.transactions.services import register_charge
from .delivery import deliver, Status
from .models import CollectionFollowUp, CollectionReminder, DeliveryAttempt


class DeliveryTests(TransactionTestCase):
    def setUp(self):
        customer = Customer.objects.create(name="Club", email="club@example.org")
        season = Season.objects.create(name="Test", start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))
        self.account = Account.objects.create(customer=customer, season=season, name="General")
        self.balance = Decimal("25.00")
        register_charge(account=self.account, date=date.today(), description="Cargo", amount=self.balance)
        self.follow = CollectionFollowUp.objects.create(account=self.account, sent_at=timezone.now(),
                                                       due_date=date.today(), amount=self.balance)
        self.key = uuid4()

    def reminder(self, key=None):
        return deliver(self.account.pk, key or self.key, follow_up_id=self.follow.pk,
                       message="Mensaje", expected_balance=self.balance)

    @patch.object(EmailMultiAlternatives, "send")
    def test_simultaneous_clicks(self, send):
        entered, release = Event(), Event()

        def wait_for_second_request():
            entered.set()
            self.assertTrue(release.wait(10))
            return 1

        def first_request():
            try:
                return self.reminder()
            finally:
                connections.close_all()

        send.side_effect = wait_for_second_request
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(first_request)
            try:
                self.assertTrue(entered.wait(10))
                self.assertEqual(self.reminder(), Status.SENDING)
            finally:
                release.set()
            self.assertEqual(future.result(), Status.SENT)
        self.assertEqual(self.reminder(), Status.SENT)
        self.assertEqual(CollectionReminder.objects.count(), 1)
        send.assert_called_once()

    @patch.object(EmailMultiAlternatives, "send", side_effect=[SMTPDataError(550, b"Rejected"), 1])
    def test_explicit_rejection_can_retry(self, send):
        self.assertEqual(self.reminder(), Status.REJECTED)
        self.assertEqual(self.reminder(), Status.SENT)
        self.assertEqual(DeliveryAttempt.objects.count(), 1)

    @patch.object(EmailMultiAlternatives, "send", side_effect=ConnectionResetError())
    def test_lost_confirmation_blocks_resend(self, send):
        self.assertEqual(self.reminder(), Status.UNKNOWN)
        self.assertEqual(self.reminder(), Status.UNKNOWN)
        with self.assertRaises(ValidationError):
            self.reminder(uuid4())
        send.assert_called_once()

    @patch.object(EmailMultiAlternatives, "send", return_value=1)
    def test_database_failure_after_acceptance(self, send):
        with patch.object(CollectionReminder.objects, "create", side_effect=DatabaseError):
            with self.assertRaises(DatabaseError):
                self.reminder()
        self.assertEqual(self.reminder(), Status.SENDING)
        self.assertFalse(CollectionReminder.objects.exists())
        send.assert_called_once()

    @patch("apps.statements.email.PdfRenderer.render", return_value=b"pdf")
    @patch.object(EmailMultiAlternatives, "send", return_value=1)
    def test_statement_registered_once(self, send, render_pdf):
        self.follow.delete()
        for _ in range(2):
            self.assertEqual(deliver(self.account.pk, self.key, base_url="http://localhost/"), Status.SENT)
        self.assertEqual(CollectionFollowUp.objects.count(), 1)
        self.assertEqual(bytes(DeliveryAttempt.objects.get().pdf), b"pdf")
        send.assert_called_once()
