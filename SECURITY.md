# Security Policy

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| 0.1.x | ✅ | Active development |

## Reporting Security Issues

Please report security issues via GitHub Security Advisories or by emailing security@project-j.org.

## Security Best Practices

### Environment Configuration
- Never commit `.env` files or expose secrets
- Use the `.env.example` template for new settings
- Rotate keys regularly if compromised

### Authentication
- Use strong, randomly generated `SECRET_KEY`
- Set appropriate token expiration times
- Implement rate limiting on auth endpoints
- Use HTTPS in production

### Database Security
- Use strong PostgreSQL passwords
- Restrict database access to trusted hosts
- Enable pgvector extension only in trusted environments
- Regular database backups

### OCR and AI Services
- Restrict PaddleOCR service to internal network
- Validate LLM input/output to prevent prompt injection
- Monitor API usage for abuse

### Storage Security
- MinIO credentials should be rotated regularly
- Use bucket policies to restrict access
- Enable encryption at rest for object storage

## Dependencies

- Regularly update dependencies via `pip install --upgrade`
- Review security advisories for all third-party packages
- Use `pip-audit` or `safety` to check for known vulnerabilities