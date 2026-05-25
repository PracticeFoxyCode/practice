# On Setup

## Basics

* Learn touch typing.
* Use scaffolding for bootstraping your project, e.g. `cookiecutter`. Good for standardizing your organization's projects and saving time on setup.
* Never write wikis, always scripts.
* Get your minimal hooks set up from the start with your CI.
  * tests, linters, formatters.
* Use pull requests from the start.
* If reasonable, use a build system, `make` or `rake` or `just`.
* Know your ecosystem, e.g. `uv` for Python, `cargo` for Rust, `npm` for node, etc.
  * use lock-files for reproducible builds.
  * Save artifacts tagged by commit hash.
  * Leverage ecosystem documentation.
* For a very lean project, the README lists
  * one liner for setting up the project
  * one liner for running tests
  * minimal further explanations
  * expand this only when actually needed: e.g. team members cannot onboard without it.
* Story Tests are the ultimate user guide

## Security

* Know what secrets are
* Scan for accidentally committed secrets with a pre-commit hook (e.g. `gitleaks`, `truffleHog`).
* Audit your dependencies for known vulnerabilities. Automate it in CI.
* DO NOT BE LAZY with root-level permissions. Use the principle of least privilege.
* Use vaults for secrets management, e.g. `vault` or `aws secrets manager`.

## Advanced

* Use docker for a full working environment.
* Everything should be text based.
* Use mock services for E2E tests.
* Use infrastructure-as-code even for small projects (terraform, CloudFormation). "I'll do it properly later" never happens.
