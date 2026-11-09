from django.shortcuts import render
from .models import Account
from ..customers.models import Customer
from apps.seasons.models import Season
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import AccountForm, AccountUpdateForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from django.db.models import Case, DecimalField, F, Sum, Value, When
from apps.transactions.models import Transaction
from apps.collection.models import CollectionReminder
from .services import register_new_account, AccountCloseService
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from apps.transactions.forms import ChargeForm, PaymentForm
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

@require_POST
def closed_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    try:
        AccountCloseService.close(account)

    except ValidationError as e:

        messages.error(request,"; ".join(e.messages))

    else:
        messages.success(
            request,
            "La cuenta ha sido cerrada correctamente."
        )

    return redirect(
        "accounts:account_detail",
        pk=account.pk
    )

class AccountListView(ListView):
    model=Account
    template_name ="accounts/accounts_list.html"
    context_object_name ="accounts"
    paginate_by = 20

    def get_season(self):
        if not hasattr(self, "_selected_season"):
            # Solo entra aquí la PRIMERA vez que se llama a get_season()
            season_id = self.request.GET.get("season")
            if season_id:
                self._selected_season = Season.objects.filter(pk=season_id).first()

            else:
                self._selected_season = Season.objects.filter(is_active=True).first()

        return self._selected_season

    def get_queryset(self):

        selected_season = self.get_season()

        queryset = Account.objects.filter(
            season=selected_season
        ).select_related("season")

        search = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "name_asc")
        statuses = self.request.GET.getlist("status")


        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(customer__name__icontains=search)
            )

        queryset = queryset.annotate(
            account_balance = Coalesce(
                Sum(
                    Case(
                        When(
                            transactions__movement_type=Transaction.MovementType.CHARGE,
                            then=F("transactions__amount"),
                        ),
                        When(
                            transactions__movement_type=Transaction.MovementType.PAYMENT,
                            then=-F("transactions__amount"),
                        ),
                        output_field=DecimalField(
                            max_digits=12,
                            decimal_places=2,   
                        ),
                    )
                ),
                Value(0),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2, 
                ),
            )
        )

        status_filter = Q()
        
        # FILTRADO POR SITUACIÓN
        if "pending" in statuses:
            status_filter |= Q(account_balance__gt=0, is_closed=False)

        if "negative" in statuses:
            status_filter |= Q(account_balance__lt=0, is_closed=False)

        if "zero" in statuses:
            status_filter |= Q(account_balance=0, is_closed=False)

        if "closed" in statuses:
            status_filter |= Q(is_closed=True)

        if statuses:
            queryset = queryset.filter(status_filter)


        # ORDENACIÓN
        if sort == "name_desc":
            queryset = queryset.order_by("-name")

        elif sort == "balance_asc":
            queryset = queryset.order_by("account_balance")

        elif sort == "balance_desc":
            queryset = queryset.order_by("-account_balance")

        else:
            queryset = queryset.order_by("name")

        return queryset


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
    
            active_season = Season.objects.filter(
                is_active = True
            ).first()
    
            selected_season = self.get_season()

            query_params = self.request.GET.copy()
            query_params.pop("page", None)

            context["pagination_query"] = query_params.urlencode()
            context["active_season"] = active_season
            context["selected_season"] = selected_season
            context["seasons"] = Season.objects.all()
            context["selected_statuses"] = self.request.GET.getlist("status")
            context['payment_form'] = PaymentForm()
            context['charge_form'] = ChargeForm()
            context['account_update_form'] = AccountUpdateForm()
            return context


    

class AccountDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Account
    permission_required="accounts.view_account"
    context_object_name = "account"
    template_name = "accounts/accounts_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.object.transactions.all().order_by("-date", "-pk")

        paginator = Paginator(transactions, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["transactions"] = page_obj.object_list
        context["collection_reminders"] = (
            CollectionReminder.objects
            .filter(follow_up__account=self.object)
            .select_related("follow_up")
            .order_by("-sent_at")
        )
        context['charge_form'] = ChargeForm()
        context['payment_form'] = PaymentForm()
        context["payment_methods"] = Transaction.PaymentMethod.choices

        return context

class AccountCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Account
    permission_required="accounts.add_account"
    context_object_name = "account"
    template_name = "accounts/account_form.html"
    form_class=AccountForm

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(
            Customer,
            pk=kwargs["customer_pk"],
        )

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["customer"] = self.customer

        return kwargs 

    def form_valid(self, form):
        season = Season.objects.filter(
            is_active=True
        ).first()

        if season is None:
            form.add_error(
                None,
                "No hay ninguna temporada activa. Por favor, cree una temporada antes de crear una cuenta."
            )
            return self.form_invalid(form)

        try:
            register_new_account(
                customer=self.customer,
                season=form.season,
                name=form.cleaned_data['name'],
                notes = form.cleaned_data.get("notes") or "",

            )
        except ValidationError as e:
            for message in e.messages:
                form.add_error(None, message)

            return self.form_invalid(form)


        messages.success(
            self.request,
            "La cuenta se ha creado correctamente"
        )
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "customers:customer_detail",
            kwargs={"pk" : self.customer.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.customer
        context["title"] = "Nueva cuenta"
        context["active_season"] = Season.objects.filter(
            is_active=True
        ).first()
        return context

class AccountUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Account
    form_class = AccountUpdateForm
    permission_required="accounts.change_account"

    def form_valid(self, form):
        if self.object.is_closed:
            return JsonResponse({
                "success": False,
                "errors": {
                    "__all__" : ["No se puede actualizar una cuenta cerrada."],
            },
                },
                status=400,
                )

        self.object = form.save()

        return JsonResponse({
            "success": True,
            "message": "Cuenta actualizada correctamente.",
            "account": {
                "id": self.object.pk,
                "name": self.object.name,
                "notes": self.object.notes,
            },
        }, status=200)

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data(),
        }, status=400)