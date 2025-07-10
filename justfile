# -*- mode: just -*-

# Run main program
main:
    uv run main

# Linting and formatting
fmt:
    uv run pre-commit run --all

# Audit project dependencies
audit:
    uv tree
    uv pip compile pyproject.toml -o requirements.txt
    uvx pip-audit -r requirements.txt --fix
