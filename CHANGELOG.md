# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

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

