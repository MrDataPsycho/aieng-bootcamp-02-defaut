# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/claude-code) when working with code in this repository.

## Project Overview

This is an AI Engineering Bootcamp project scaffold using Python 3.12+ with uv as the package manager.

## Development Setup

This project uses **uv** for dependency management:

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --group dev

# Run the main entry point
uv run python main.py
```

## Project Structure

- `main.py` - Main entry point for the application
- `notebooks/` - Jupyter notebooks for experimentation and analysis
- `.venv/` - Virtual environment (managed by uv)
- `pyproject.toml` - Project configuration and dependencies

## Working with Notebooks

The project includes Jupyter notebook support. To work with notebooks:

```bash
# The ipykernel package is available in dev dependencies
uv sync --group dev

# Run Jupyter
uv run jupyter lab
# or
uv run jupyter notebook
```

## Python Version

- Requires Python 3.12 or higher (specified in `.python-version` and `pyproject.toml`)
