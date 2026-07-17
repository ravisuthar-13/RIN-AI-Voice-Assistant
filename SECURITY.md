# 🔐 Security Policy

## Project Status

RIN is currently under active development and is not production-ready.

The project is being built as a personal AI desktop assistant and currently
contains experimental features that interact with the Windows operating system.

RIN should not yet be used in security-critical, production, enterprise, or
sensitive environments.

---

## Supported Versions

RIN has not yet reached a stable public release.

| Version | Security Support |
|---------|------------------|
| Development versions | Limited |
| Experimental builds | Limited |
| Stable release | Not yet available |

Security support will become more structured once RIN reaches a stable release.

---

## Reporting a Vulnerability

If you discover a security or privacy issue, please do not publish sensitive
details in a public GitHub issue.

Please report the issue through one of the following methods:

- Open a private GitHub Security Advisory.
- Contact the project maintainer privately.
- Provide a clear explanation of the issue and how it can be reproduced.

Please include:

- A description of the vulnerability
- Steps to reproduce the issue
- The affected file or feature
- The possible security impact
- Screenshots or logs, if appropriate
- A suggested solution, if available

---

## Privacy Principles

RIN is being designed with privacy and local-first development principles.

The project aims to follow these practices:

- Prefer local processing whenever possible
- Avoid unnecessary data collection
- Avoid telemetry and user tracking
- Avoid storing sensitive information in source code
- Avoid exposing local file paths
- Avoid committing passwords, tokens, API keys, or credentials
- Use environment variables for future secrets
- Request only the permissions required for a feature

---

## Current Security Limitations

Because RIN is still under active development, the following limitations may
exist:

- Voice commands are not yet protected by owner authentication
- Some system-control features may execute commands immediately
- Permission management is still under development
- Input validation may not yet cover every possible command
- Security testing is currently limited
- Experimental features may behave differently across Windows systems

Users should review the code before running it on their own computer.

---

## Safe Usage

Before running RIN:

1. Review the source code.
2. Verify application and folder paths.
3. Do not add passwords or private information directly to Python files.
4. Do not run unknown third-party modifications.
5. Test new features in isolated files before integration.
6. Keep personal configuration files outside the public repository.
7. Use a virtual environment when installing dependencies.

---

## Future Security Plans

Planned security improvements include:

- Owner voice authentication
- Permission-based command execution
- Confirmation for sensitive actions
- Secure configuration management
- Encrypted local memory
- PIN-based protection
- Face recognition
- Local audit logs
- Sensitive-command restrictions
- Improved input validation
- Offline processing options

---

## Responsible Disclosure

Please allow reasonable time for a security issue to be investigated and fixed
before sharing it publicly.

Thank you for helping improve the security and privacy of RIN.