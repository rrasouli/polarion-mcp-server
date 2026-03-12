# Contributing to Polarion MCP Server

Thank you for your interest in contributing to the Polarion MCP Server!

## Development Workflow

This repository uses a protected main branch workflow:

1. **Fork or Clone** the repository
2. **Create a feature branch** from `master`
3. **Make your changes** with clear, descriptive commits
4. **Test your changes** thoroughly
5. **Submit a Pull Request** against `master`

## Branch Naming Convention

Use descriptive branch names:
- `feature/add-bulk-import` - New features
- `fix/soap-auth-issue` - Bug fixes
- `docs/api-examples` - Documentation updates
- `refactor/client-structure` - Code refactoring

## Pull Request Guidelines

### Before Submitting

- Ensure your code follows existing style conventions
- Test all changes locally
- Update documentation if needed
- Add examples for new features

### PR Description Should Include

- Clear description of what changed
- Why the change was needed
- Any breaking changes
- Testing performed

### Example PR Title

```
Add support for bulk test case import from spreadsheet
```

## Code Standards

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Documentation
- Update README.md for new features
- Add examples in `/examples` directory
- Comment complex logic
- No emojis in code or docs

## Testing

Before submitting a PR:

```bash
# Test REST API functionality
python3 examples/create_test_case.py

# Test SOAP API fallback (if credentials available)
export POLARION_USERNAME="test-user"
export POLARION_PASSWORD="test-pass"
python3 examples/update_test_steps.py

# Verify imports work
python3 -c "from polarion_client import PolarionClient; print('OK')"
```

## Security

- Never commit credentials or tokens
- Use environment variables for sensitive data
- Review `.gitignore` before committing

## Questions or Issues?

- Open an issue for bugs or feature requests
- Tag issues appropriately (bug, enhancement, documentation)
- Provide clear reproduction steps for bugs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
