# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/claude-code) or any ai assistant when working with code in this repository.

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

## Python Version

- Requires Python 3.12 or higher (specified in `.python-version` and `pyproject.toml`)

## Development Commands:
uv run <filename>
IMPORTANT: Always run `uv run ruff format` before committing your code.
IMPORTANT: Always run `uv run ruff` before committing your code.

## Architecture

This is a Python 3.12 starter template for AI-powered applications with Agents can provide user variaous product intentory and pricing information. The data it has access is based on Amazon Reviews dataset for 2023.

## Core Stack

- Python 3.12 with uv as the package manager
- Any UI update always bump the version up by 0.0.1 in `src/chatbot_ui/app.py`