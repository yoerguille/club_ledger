# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

## [2026-10-28]

### Added
- Added AJAX season editing modal to update seasons withour reload page.
- Added an automated test for SeasonUpdateView, validating permissions, invalid dates and update succesfully.


## [2026-10-27]

### Added
- Added SeasonListView to manage and review registered seasons.
- Added season management to the application sidebar navigation.
- Added season cards displaying financial statistics, including total charges, payments, outstanding balances, and accounts with pending debt.
- Added navigation from each season card to the account list filtered by season.
- Added an automated test for get_season_stats(), validating account and transaction counts, charges, payments, net balances, and outstanding debts.

### Changed
- Refactored modal templates to use a shared `base_modal.html` component, reducing duplicated HTML and standardizing their appearance.
- Updated customer creation and editing modals to share a consistent structure and styling.
- Reused Django `CustomerForm` and the shared form field component in the customer creation modal.
- Updated the season creation modal to use the shared layout while preserving its confirmation workflow and validation messages.
- Centralized season financial calculations in the reusable `get_season_stats()` service.
- Refactored dashboard statistics to reuse the shared season statistics service.
- Enhanced season cards with financial indicators, including charges, payments, outstanding balances, and accounts with pending debt.
## [2026-10-26]

### Added
- Added season creation through a modal form.
- Added automatic activation of newly created seasons.
- Added a confirmation step before replacing the currently active season.
- Added a summary of outstanding account balances before changing seasons.
- Added automated tests for season creation, activation, confirmation, duplicate names, date validation, and outstanding balance calculations.

### Changed
- Updated season management to ensure only one season can be active at a time.
- Automatically deactivate the previous active season after confirming a season change.

### Fixed
- Prevented active seasons from being replaced without explicit user confirmation.
- Fixed season date validation in `SeasonService` to reject invalid date ranges independently of form validation.

## [2026-10-25]

### Added
- Added a Flowbite modal to create customers directly from the customer list.
- Implemented asynchronous customer creation using the Fetch API and Django ModelForms.
- Added JSON responses for successful submissions and validation errors.
- Added inline field validation and general form error messages.

### Changed
- Replaced the standalone customer creation workflow with a modal-based interface.
- Improved client-side form handling by clearing previous errors and preventing duplicate submissions.
- Added handling for unexpected server responses and connection errors.
- Preserved customer creation through the existing service layer and permission checks.

### Fixed
- Fixed an issue where the season selector was empty when creating accounts for newly registered customers.
- Updated the account creation modal to display all active seasons, regardless of existing customer accounts.
- Separated season filtering for customer account history from season selection for new accounts.

## [2026-10-24]

### Added
- Added a Flowbite modal for creating customers directly from the customer list.
- Implemented asynchronous customer creation using the Fetch API and Django ModelForms.
- Added JSON responses for successful customer creation and form validation errors.
- Added inline validation error messages for customer form fields.

### Changed
- Updated the customer creation workflow to reload the customer list after successful submission.
- Preserved customer creation business logic and permission checks.

## [2026-10-23]

### Added
- Automated tests for account closure business rules.
- HTTP test to ensure account closure rejects GET requests.
- Multi-stage Dockerfile for Django and frontend asset compilation.
- Docker Compose development environment with Django and PostgreSQL 17.
- Persistent PostgreSQL storage using a Docker named volume.
- Docker development and testing instructions in README.

### Fixed
- Added missing `apps/__init__.py` to enable Django test discovery.

## [2026-10-22]

### Added
- Account closure confirmation modal using Flowbite.
- Account closure service to centralize business rules.

### Changed
- Reorganized account detail actions for better usability.
- Refactored account closure view to delegate business logic to the service.
- Restricted account closure to POST requests.

