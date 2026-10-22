# Club Ledger

Club Ledger is a web application built with Django to manage
seasonal accounts, payments, and outstanding balances for
sports clubs.

## Overview

Small sports clubs often place orders throughout a season
and make payments gradually, rather than paying for every
order individually.

Club Ledger provides a centralized system to track charges,
register payments, monitor outstanding balances, and
manage payment follow-ups.

The project focuses on applying backend development,
business logic, and automation to a real-world business
problem.

## Tech Stack

**Backend**
- Python
- Django
- Django REST Framework

**Database**
- PostgreSQL

**Frontend**
- HTML
- Tailwind CSS
- Flowbite
- JavaScript

**Automation**
- n8n
- OpenAI API

**Development Tools**
- Git & GitHub
- Docker

## Features

### Account Management
- Manage sports clubs and seasonal accounts.
- Register charges and payments.
- Track outstanding balances.
- Close settled accounts with confirmation and business-rule validation.

### Account Statements
- Generate PDF account statements.
- Download, print, and email statements.

### Payment Follow-ups
- Track outstanding debts and payment deadlines.
- Manage payment follow-up statuses.
- Generate AI-assisted payment reminders through n8n and OpenAI.
- Review and edit reminder drafts before sending.

### REST API
- REST endpoints for account operations.
- API-based integration capabilities using Django REST Framework.


## Installation & Setup

### Prerequisites

Before running Club Ledger, make sure you have:

- Python 3.12+
- PostgreSQL
- Node.js and npm
- Git

### Clone the repository

```bash
git clone https://github.com/yoerguille/club_ledger.git
cd club_ledger
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure your Django secret key,
PostgreSQL credentials, email settings, and n8n webhook
URL as needed.

Never commit your `.env` file.

### Database Setup

Create a PostgreSQL database and user using the
credentials configured in your `.env` file.

Apply Django migrations:

```bash
python manage.py migrate
```

### Tailwind CSS

Install the frontend dependencies:

```bash
python manage.py tailwind install
```

For development, run Django and the Tailwind watcher:

```bash
python manage.py tailwind dev
```

Alternatively, compile the CSS:

```bash
python manage.py tailwind build
```

Then start the Django development server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Project Status

Club Ledger is currently under active development.

Core account management, payment tracking, account
statements, REST API endpoints, and AI-assisted payment
reminder generation have been implemented.

The project is being progressively improved with a focus
on backend architecture, maintainability, and automation.

## Roadmap

Planned improvements include:

- [ ] Automated tests for business logic and API endpoints.
- [ ] Docker-based development environment.
- [ ] Improved REST API documentation.
- [ ] Enhanced payment follow-up workflows.
- [ ] Production deployment.
