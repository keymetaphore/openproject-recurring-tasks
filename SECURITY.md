# Security Policy

## Supported Versions

We currently support the latest `main` branch only. If vulnerabilities are discovered in older versions, they may or may not receive patches depending on severity and capacity.

## Reporting a Vulnerability

If you discover a security vulnerability, **please do not create a public issue**.

Instead, report it responsibly via email:

- **Email**: `kevins17@lidmasina.lv`  
- **PGP Key (optional)**:
  -----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEZZ3VCBYJKwYBBAHaRw8BAQdA4FMr3sZa4ONkEbNySG9RuPMl1QfVd50DGG7/
H5EoONm0IFRvbWFzcyBCcmllZGlzIDx0bXVzZXJAcHVsa3MubHY+iJoEExYKAEIW
IQSJC9pyajP0p00owcjWNKT1p0hJMgUCZZ3VCAIbAwUJA8ROGAULCQgHAgMiAgEG
FQoJCAsCBBYCAwECHgcCF4AACgkQ1jSk9adISTIIAQD+PqDBETy+nXYWD7TqGWnu
ThkgY1IwnsnU0MxMfmv77mMA/ieHROyxeRUiKHWpeAPYVQ1pzYc4JwTzzxx5pPi6
x6oAuDgEZZ3VCBIKKwYBBAGXVQEFAQEHQM7OzOLVQRDnv44KC2HSgdnSitLqTBZz
/nW+6WkCCiRJAwEIB4h+BBgWCgAmFiEEiQvacmoz9KdNKMHI1jSk9adISTIFAmWd
1QgCGwwFCQPEThgACgkQ1jSk9adISTKWdQEA/quUVXV0onqhCwxP/SE51ePR+gEv
JGHPqNwfmkiQX6sBALWPhtAyhhA9JA6Bh6J8NjmWFmnUJC4WzpxoHEYNMToB
=uD90
-----END PGP PUBLIC KEY BLOCK-----


Please include:

- Description of the vulnerability
- Steps to reproduce
- Affected endpoints or files (if known)
- Any potential impact or exploit paths
- Suggestions (if any) for remediation

## Scope

This project is a self-hosted task scheduling frontend for OpenProject. The following are **in scope** for vulnerability reporting:

- Authentication bypass
- API token leakage
- Insecure cron/job scheduling manipulation
- Persistent cross-site scripting (XSS)
- Server-side request forgery (SSRF)
- Privilege escalation
- OIDC misconfigurations with external impact

The following are **out of scope**:

- Issues requiring full control of a user’s host or Docker environment
- Missing or weak authentication when `OIDC_ENABLED=false`
- Self-inflicted misconfigurations
- Vulnerabilities in OpenProject itself (report upstream)

## Disclosure Process

1. Vulnerability is reported privately.
2. The report is verified.
3. We coordinate and develop a patch.
4. A security advisory will be published upon release.
5. Credit is given to reporters if desired.

## Responsible Disclosure

We support and appreciate responsible disclosure practices. Please note that this is a small backyard project, and no compensation will be provided.
