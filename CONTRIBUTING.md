# Contributing to PDF Parser

Thank you for your interest in contributing to PDF Parser! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- Clear descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, Docker version)
- Sample PDF if possible (or description of PDF characteristics)

### Suggesting Enhancements

Enhancement suggestions are welcome. Please include:

- Clear use case description
- Expected behavior
- Any alternatives you've considered

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes locally
5. Commit with clear, descriptive messages following [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Git Branching Strategy

This project follows a simplified Git flow for managing development and releases.

### Branches

#### `main`
- Production-ready code
- Always stable and deployable
- Protected branch (requires PR approval)
- Tagged with version numbers for releases

#### Feature Branches
- Branch from `main`
- Naming: `feature/description` or `feat/description`
- Examples: `feature/ocr-improvement`, `feat/add-caching`
- Merge back to `main` via PR

#### Bugfix Branches
- Branch from `main`
- Naming: `fix/description` or `bugfix/description`
- Examples: `fix/memory-leak`, `bugfix/empty-file-handling`
- Merge back to `main` via PR

#### Hotfix Branches
- For urgent production fixes
- Branch from `main`
- Naming: `hotfix/description`
- Merge to `main` and tag immediately

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, CI, etc.)

#### Examples

```
feat(parser): add support for batch processing
fix(api): handle corrupted PDF files gracefully
docs(readme): update deployment instructions
refactor(ocr): extract OCR logic to separate module
perf(parser): optimize text extraction for large PDFs
test(api): add integration tests for parse endpoint
chore(deps): update fastapi to 0.115.6
```

### Pull Request Process

1. **Create branch** from `main`
2. **Make changes** with clear, atomic commits
3. **Test locally** (run tests, build Docker image)
4. **Push branch** to your fork
5. **Open PR** with descriptive title and description
6. **Address review** feedback
7. **Squash and merge** to `main`

#### PR Title Format

Follow the same convention as commit messages:
- `feat: add batch processing support`
- `fix: resolve memory leak in OCR`
- `docs: update API documentation`

### Release Process

1. Ensure `main` is stable and all tests pass
2. Update version in relevant files (if applicable)
3. Create a [GitHub Release](https://github.com/jleand/pdf-parser/releases)
4. Tag the release: `v1.0.0`, `v1.0.1`, etc.
5. Docker image is automatically built and pushed

### Protected Branch Rules

- `main` requires PR approval before merging
- `main` requires status checks to pass
- Force pushes to `main` are disabled
- Branch deletion is disabled

## Development Setup

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pdf-parser.git
cd pdf-parser

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

### Building Docker Image

```bash
docker build -t pdf-parser .
docker run -p 8000:8000 pdf-parser
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Keep functions focused and small
- Document complex logic
- Use meaningful variable names

## Testing Guidelines

- Write tests for new features
- Ensure existing tests pass
- Test edge cases (empty files, large files, corrupted PDFs)
- Test both text-based and OCR paths

## Tips

- Keep PRs small and focused
- Write descriptive commit messages
- Update documentation with code changes
- Add tests for new features
- Run linting before committing

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!
