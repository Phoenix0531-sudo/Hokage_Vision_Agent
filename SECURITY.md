# Security Policy

## Supported Versions

The project is in alpha while the legacy repository is being migrated. Security fixes target the latest `main` or `master` branch.

## Reporting a Vulnerability

Please report security issues privately to the repository maintainers. Do not open public issues for vulnerabilities involving arbitrary file access, unsafe agent tool execution, leaked credentials, or model/data supply chain risks.

## Security Boundaries

- The default agent is rule-based and must not execute arbitrary shell commands.
- LLM providers are optional and must use allowlisted project tools only.
- API keys, private datasets, and model weights must not be committed.
- Real training remains dry-run by default unless the user explicitly confirms execution.
