# Security Policy

## Supported Versions

We actively support the following versions of {{cookiecutter.project_name}} with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

We follow a rolling release model where only the latest version receives security updates. We recommend always using the latest version.

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### For Critical Security Issues

**DO NOT** open a public issue for security vulnerabilities.

1. **Email us directly**: Send details to {{cookiecutter.author_email}}
2. **Include in your report**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if you have one)
   - Your contact information

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity, typically within 30 days for critical issues

### What to Expect

1. We'll acknowledge receipt of your vulnerability report
2. We'll confirm the issue and determine its severity
3. We'll work on a fix and coordinate disclosure timing with you
4. We'll release the fix and publicly disclose the vulnerability
5. We'll credit you in our security advisory (unless you prefer to remain anonymous)

## Security Best Practices

When using {{cookiecutter.project_name}}:

### Configuration Security
- Never commit secrets, API keys, or passwords to version control
- Use environment variables for sensitive configuration
- Regularly rotate API keys and secrets
- Review the `.env.example` file for secure configuration patterns

### Dependency Security
- Keep dependencies updated (use `pip list --outdated`)
- Monitor security advisories for dependencies
- Use tools like `safety` to check for known vulnerabilities
- Enable Dependabot for automatic security updates

### Code Security
- Follow secure coding practices
- Validate all user inputs
- Use parameterized queries for database operations
- Implement proper authentication and authorization
- Log security events for monitoring

## Responsible Disclosure

We believe in responsible disclosure and will work with security researchers to:

- Understand and validate reported vulnerabilities
- Develop and test fixes
- Coordinate public disclosure timing
- Provide credit to researchers (if desired)

## Security Updates

Security updates will be:

- Released as soon as possible after validation
- Announced in our release notes
- Tagged with security advisory labels
- Communicated through GitHub Security Advisories

## Contact

For any security-related questions or concerns:

- **Security Email**: {{cookiecutter.author_email}}
- **Maintainer**: {{cookiecutter.author_name}}
- **GitHub**: [@{{cookiecutter.github_username}}](https://github.com/{{cookiecutter.github_username}})

Thank you for helping keep {{cookiecutter.project_name}} and our community safe!
