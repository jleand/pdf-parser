# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. Please report them responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report via email to: [me@joaoleandro.com]

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Updates**: Regular progress updates
- **Resolution**: We'll work to address critical vulnerabilities promptly

### Disclosure Policy

- We follow responsible disclosure practices
- Please do not disclose the vulnerability publicly until we've had a chance to address it
- We'll credit reporters in security advisories (unless anonymity is requested)

## Security Best Practices

When deploying PDF Parser:

1. **File size limits**: Set appropriate `MAX_FILE_SIZE` for your use case
2. **Concurrency limits**: Configure `MAX_CONCURRENT` based on available resources
3. **CORS**: Restrict `CORS_ORIGINS` to trusted domains in production
4. **Resource limits**: Set memory/CPU limits in container orchestration
5. **Input validation**: The service validates PDF files, but consider additional validation at the API gateway level
6. **Monitoring**: Monitor for unusual patterns (large files, high concurrency)

## Security Features

- Input validation (file type, size, magic bytes)
- Concurrency limits to prevent resource exhaustion
- OCR page limits to prevent memory issues
- Non-root container user
- Minimal Docker image surface
