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

### Prerequisites

Choose one of the following development setups:

**Docker (recommended)**
- Docker
- Docker Compose
- Git

**Local development**
- Python 3.12+
- PostgreSQL
- Node.js and npm
- Git

### Clone the repository

```bash
git clone https://github.com/yoerguille/club_ledger.git
cd club_ledger
```

### Docker Setup

Club Ledger provides a Docker Compose development environment with two services:

- **web:** Django application with Python 3.12, Tailwind CSS, Flowbite, and WeasyPrint.
- **db:** PostgreSQL 17 with persistent database storage.

**1. Configure environment variables**

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure the required variables, including `SECRET_KEY`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

If a value contains `$`, use single quotes to prevent Docker Compose variable interpolation.

Never commit `.env` to version control.

**2. Build and start the containers**

```bash
docker compose up -d --build
```

**3. Apply database migrations**

```bash
docker compose exec web python manage.py migrate
```

**4. Create an administrator account**

```bash
docker compose exec web python manage.py createsuperuser
```

**5. Access the application**

Open http://localhost:8000/ in your browser.

**Run automated tests**

```bash
docker compose exec web python manage.py test
```

**View container logs**

```bash
docker compose logs -f web
```

**Stop the environment**

```bash
docker compose down
```

PostgreSQL data is stored in a named Docker volume and persists when containers are stopped or recreated.

**Important:** Running `docker compose down -v` removes the Compose-managed volumes, including the PostgreSQL database volume. Use this command only when you intentionally want to delete the Docker database.

**Development notes**

- The Docker environment is intended for local development, not production deployment.
- Django runs using its built-in development server.
- Tailwind CSS is compiled during the Docker image build.
- After modifying application code or frontend assets, rebuild the image with `docker compose up -d --build`.
- The Docker PostgreSQL database is separate from any locally installed PostgreSQL instance.
- The n8n automation service is not included in this Docker Compose configuration and requires separate setup.

### Local Development Setup

The following instructions describe how to run Club Ledger
without Docker.

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

- [x] Initial automated tests for account closure business rules.
- [x] Docker-based development environment.
- [ ] Improved REST API documentation.
- [ ] Enhanced payment follow-up workflows.
- [ ] Production deployment.
