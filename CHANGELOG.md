
# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

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

