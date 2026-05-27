# Contributing to Fhircraft

Thank you for your interest in contributing to Fhircraft! This guide provides detailed instructions for setting up your development environment and contributing to both the codebase and documentation. Whether you're fixing bugs, adding features, or improving docs, your help makes Fhircraft better for everyone.

## Ways to Contribute

We welcome all types of contributions:

<div class="grid cards" markdown>

-   :material-bug:{ .lg .middle } __Report Bugs__

    ---

    Found an issue? [Open a bug report](https://github.com/luisfabib/fhircraft/issues/new?labels=bug) with reproduction steps, expected vs actual behavior, and relevant logs

-   :material-lightbulb:{ .lg .middle } __Suggest Features__

    ---

    Have ideas for improvements? [Open a feature request](https://github.com/luisfabib/fhircraft/issues/new?labels=enhancement) or start a discussion

-   :material-code-braces:{ .lg .middle } __Submit Code__

    ---

    Fix bugs, add features, or improve performance by submitting pull requests

-   :material-file-document-edit:{ .lg .middle } __Improve Documentation__

    ---

    Help keep docs accurate, clear, and up-to-date

-   :material-comment-text:{ .lg .middle } __Review & Discuss__

    ---

    Participate in code reviews or help answer community questions

</div>

No contribution is too small—every improvement counts!


!!! info "AI Tools and Human Attribution"
    
    We **welcome** the use of AI tools and AI-based changes to help solve issues and implement features. However, contributions must be submitted by **humans** who take responsibility for the changes.
    
    **We do not accept:**
    
    - Automated bot-driven contributions or pull requests
    - Unattended automated commits or pushes
    - Autonomous AI agent contributions without human oversight
    - Automated dependency update bots, auto-formatting bots, etc. without human review
    
    **What we do accept:**
    
    - Code and documentation created or improved with AI assistance (ChatGPT, Copilot, Claude, etc.)
    - Any changes where **you (the human contributor) personally review, test, and validate** all code before submitting
    - Pull requests from humans who take responsibility and attest to understanding every change
    
    **The key requirement:** The person submitting the contribution must be human and must personally verify that all changes are correct, tested, and align with project standards. You are responsible for attesting that you understand and agree with every change you submit.

---

## Quick Start for Contributors

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher**
- **Git** for version control
- **pip** for package management

### Initial Setup

1. **Fork and clone the repository:**
    ```bash
    git clone https://github.com/YOUR-USERNAME/fhircraft.git
    cd fhircraft
    ```

2. **Add the upstream remote:**
    ```bash
    git remote add upstream https://github.com/luisfabib/fhircraft.git
    ```

3. **Verify your Python version:**
    ```bash
    python --version  # Should be 3.10+
    ```

Now proceed to the appropriate setup section based on your contribution type.

---

## Contributing Code Changes

Follow these steps when contributing bug fixes, new features, or code improvements.

### 1. Environment Setup for Code Development

**Install the package in editable mode with development dependencies:**

```bash
# Install core package + development tools
pip install -e ".[dev]"
```

This installs:

- **Core dependencies** - Required for Fhircraft to run (Pydantic, requests, etc.)
- **Testing tools** - pytest, pytest-mock, parameterized, coverage
- **The package in editable mode** - Changes to code are immediately reflected

**Verify your installation:**

```bash
# Check that pytest is available
pytest --version

# Run a quick test to ensure everything works
pytest test/test_config.py -v
```

### 2. Create a Feature Branch

Always work on a dedicated branch:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch with a descriptive name
git checkout -b fix/issue-123-patient-validation
# or
git checkout -b feature/add-fhirpath-function
```

Branch naming conventions:

- `fix/` - Bug fixes
- `feature/` - New features
- `refactor/` - Code improvements without changing behavior
- `docs/` - Documentation-only changes

### 3. Make Your Changes

**Write clean, maintainable code:**

- Follow [PEP 8](https://pep8.org/) style guidelines
- Ideally, use the Black formatter
- Use type hints for function signatures
- Keep functions focused and single-purpose
- Add docstrings for public APIs

**Example of well-documented code:**

```python
def validate_fhir_resource(resource: dict, resource_type: str) -> bool:
    """Validate a FHIR resource against its structure definition.
    
    Args:
        resource: The FHIR resource as a dictionary
        resource_type: The FHIR resource type (e.g., "Patient", "Observation")
        
    Returns:
        True if validation succeeds, False otherwise
        
    Raises:
        ValueError: If resource_type is not a valid FHIR resource
    """
    # Implementation here
```

### 4. Write Tests

**All code changes must include tests.** Fhircraft uses pytest for testing.

**Test file structure:**

```
test/
├── test_fhir_path_engine.py          # FHIRPath functionality
├── test_fhir_mapper.py                # Mapping language
├── test_fhir_resources_factory.py     # Resource construction
└── test_*.py                          # Other test modules
```

**Writing tests:**

```python
# test/test_my_feature.py
import pytest
from fhircraft.fhir.resources import get_fhir_type

def test_patient_creation_validates_gender():
    """Test that invalid gender codes raise validation errors."""
    Patient = get_fhir_type("Patient", "R5")
    
    # Valid gender should work
    patient = Patient(gender="female")
    assert patient.gender == "female"
    
    # Invalid gender should raise error
    with pytest.raises(ValueError):
        Patient(gender="invalid-gender")
```

**Run tests:**

```bash
# Run all tests
pytest

# Run specific test file
pytest test/test_fhir_resources_factory.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=fhircraft --cov-report=html
```

**Test guidelines:**

- Test both success and failure cases
- Use descriptive test names that explain what is being tested
- Keep tests isolated - each test should run independently
- Mock external dependencies (network calls, file I/O)
- Aim for high code coverage (>80%)

### 5. Run the Test Suite

Before submitting, ensure all tests pass:

```bash
# Run full test suite
pytest

# Check for any warnings
pytest -v --tb=short

# Run tests for specific Python version (if using pyenv/tox)
python3.10 -m pytest
```

### 6. Commit Your Changes

Write clear, descriptive commit messages:

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "fix: resolve patient validation for edge cases

- Add validation for missing name fields
- Handle null gender values gracefully  
- Add tests for edge cases in test_fhir_resources_factory.py

Fixes #123"
```

**Commit message format:**

```
<type>: <short summary>

<optional detailed description>

<optional footer with issue references>
```

Types: `fix`, `feature`, `refactor`, `test`, `docs`, `chore`

### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin fix/issue-123-patient-validation

# Create pull request via GitHub UI
```

**Pull request checklist:**

- All tests pass locally
- New tests added for new functionality
- Code follows project style guidelines
- Docstrings added for any new functions or classes
- Related issues referenced in PR description
- PR description clearly explains the changes

---

## Contributing Documentation Changes

Follow these steps when improving user guides, API documentation, or examples.

### 1. Environment Setup for Documentation

**Install the package with documentation dependencies:**

```bash
# Install core package + documentation tools
pip install -e ".[dev, docs]"
```

This installs:

- **MkDocs Material** - Modern documentation theme
- **mkdocstrings** - Automatic API documentation generation
- **Supporting plugins** - For navigation, code generation, etc.

**Verify your installation:**

```bash
# Check that mkdocs is available
mkdocs --version
```


### 2. Preview Documentation Locally

**Start the development server:**

```bash
# From project root
mkdocs serve
```

This starts a local server at `http://127.0.0.1:8000` with live reloading. Changes to markdown files automatically refresh the browser.

### 3. Writing Documentation

**Follow the established style:**

- Use clear, concise language
- Start with a brief introduction explaining what/why
- Include practical code examples
- Add admonitions for important notes, warnings, tips
- Link to related pages and external resources

### 4. Testing Documentation

**Check for broken links and issues:**

```bash
# Build in strict mode to catch warnings
mkdocs build --strict

# Manually review your changes
mkdocs serve
```

**Documentation checklist:**

- All code examples are tested and work
- Links to other pages are valid
- External links use the correct format
- Images load correctly
- Tables render properly
- Admonitions display correctly

### 5. Testing Code Examples in Documentation

Some documentation includes doctest examples. Test them with:

```bash
# Run doctest tests
pytest test/test_doctest.py -v
```

### 6. Submit Documentation Changes

```bash
# Create a branch
git checkout -b docs/improve-fhirpath-guide

# Make your changes, then commit
git add docs/
git commit -m "docs: improve FHIRPath querying examples

- Add more complex query examples
- Clarify when to use different query methods
- Fix typos in code examples"

# Push and create PR
git push origin docs/improve-fhirpath-guide
```

---

## Pull Request Process

1. **Fork the repository** via GitHub UI

2. **Create a feature branch:**
    ```bash
    git checkout -b fix/descriptive-name
    ```

3. **Make your changes** following the guidelines above

4. **Test your changes:**
    - For code: Run `pytest` to ensure all tests pass
    - For docs: Run `mkdocs serve` to preview locally

5. **Commit with clear messages:**
    ```bash
    git commit -m "fix: descriptive message

    Detailed explanation if needed.
    
    Fixes #123"
    ```

6. **Push to your fork:**
    ```bash
    git push origin fix/descriptive-name
    ```

7. **Open a pull request** on GitHub with:
    - Clear description of changes
    - Reference to related issues
    - Screenshots (for UI/docs changes)
    - Test results confirmation

8. **Respond to feedback** from reviewers promptly

9. **Wait for CI checks** - All tests must pass:
    - Pytest suite runs on Python 3.10, 3.11, 3.12
    - Code quality checks

10. **Merge** - Once approved, maintainers will squash and merge

---

## Getting Help

- **Questions?** Open a [discussion](https://github.com/luisfabib/fhircraft/discussions)
- **Stuck?** Comment on your PR or issue
- **Need clarification?** Ask in the issue before starting work

---

## Release Process

*This section is for maintainers.*

To publish a new release:

1. **Create release branch:**
    ```bash
    git checkout -b release/vX.Y.Z
    ```

2. **Update version** in `pyproject.toml` following [semantic versioning](https://semver.org/)

3. **Update CHANGELOG.md** with release notes

4. **Open PR** to `main` with version bump

5. **Merge PR** after approval

6. **Create GitHub Release:**
    - Tag: `vX.Y.Z`
    - Copy changelog entries
    - Publish release

7. **CI/CD** automatically publishes to PyPI

8. **Verify** package on [PyPI](https://pypi.org/project/fhircraft/)

---

Thank you for contributing to Fhircraft! Your efforts help make healthcare interoperability more accessible to Python developers worldwide.
