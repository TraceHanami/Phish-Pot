# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please report it by opening an issue or emailing the maintainer. All security vulnerabilities will be promptly addressed.

### Security Best Practices Implemented
- Localhost default binding (`127.0.0.1`)
- XSS prevention via Jinja2 auto-escaping
- Unique UUID string paths for dynamic SHAP plot assets
- Non-hardcoded secrets support via environment variables
