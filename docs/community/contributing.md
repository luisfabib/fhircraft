# Contributing

Thank you for your interest in contributing to this project! Your help is greatly appreciated. This guide will help you get started with contributing code, documentation, or reporting issues.

## How to Contribute

We welcome all types of contributions! Here’s how you can get involved:

- **Report Bugs:**  
    If you encounter a bug, please [open an issue](https://github.com/fhircraft/issues) with clear steps to reproduce, expected vs. actual behavior, and any relevant logs or screenshots.

- **Suggest Features or Improvements:**  
    Have an idea to make the project better? Open an issue or start a discussion to share your suggestions. Please describe the motivation and potential benefits.

- **Submit Pull Requests:**  
    If you’ve fixed a bug, added a feature, or improved documentation, feel free to submit a pull request. Make sure to follow the [Pull Request Process](#pull-request-process) outlined below.

- **Improve Documentation:**  
    Help us keep our documentation accurate and up to date by suggesting edits or clarifications.

- **Review and Discuss:**  
    Participate in code reviews, discussions, or help answer questions from other contributors.

No contribution is too small—thank you for helping us improve!

## Development Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/fhircraft.git
    cd fhircraft
    ```

2. **Install dependencies:**
    ```sh
    pip install -e .
    ```

3. **Run tests:**
    ```sh
    pytest
    ```
## Coding Guidelines

- **Code Style:** Adhere to [PEP 8](https://pep8.org/) for Python code. Formatting is handled automatically by [Black](https://black.readthedocs.io/en/stable/), so you do not need to worry about manual formatting.
- **Testing:**  
    - For new features, add or update tests as needed.
    - When refactoring or fixing bugs, ensure existing tests are updated or expanded—do not remove failing tests.
- **Documentation:**  
    - Document all public functions and classes with [Google-style Python docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- **Commits:**  
    - Write clear, descriptive commit messages that explain the purpose of your changes.

## Pull Request Process

1. **Fork the repository.**
2. **Create a feature branch from `main`:**
    ```sh
    git checkout -b fix/some-bugfix
    ```
3. **Make your changes:**  
   Ensure all tests pass locally before committing.
4. **Commit your changes with a clear message:**
    ```sh
    git commit -m "fix: resolve issue with [brief description]"
    ```
5. **Push your branch to your fork and open a pull request:**  
   - Provide a concise, descriptive summary of your changes.
   - Reference related issues if applicable (e.g., "Closes #123").
   - Wait for automated checks to complete.
6. **Respond to feedback:**  
   Address any requested changes from reviewers.
7. **Squash and merge:**  
   Once approved and all checks pass, squash and merge your changes into `main`.

Thank you for your contribution!

## Releases

To publish a new release, follow these steps:

1. **Create a release branch:**
    ```sh
    git checkout -b release/vX.Y.Z
    ```
2. **Update the version:**  
   Bump the version number in `pyproject.toml` according to [semantic versioning](https://semver.org/).
3. **Update the changelog:**  
   Add a summary of changes for this release in your changelog file (if available).
4. **Open a pull request:**  
   Submit a PR from your release branch to `main`. Ensure all tests pass and the PR includes the version and changelog updates.
5. **Merge the pull request:**  
   Once approved, squash and merge the PR into `main`.
6. **Create a GitHub Release:**  
   Go to the [GitHub Releases page](https://github.com/fhircraft/releases), click "Draft a new release", and:
   - Set the tag to the new version (e.g., `vX.Y.Z`)
   - Add release notes (copy from the changelog)
   - Publish the release
7. **Verify the package on PyPI:**  
   Wait for the CI/CD workflow to complete. Confirm the new version is available on [PyPI](https://pypi.org/project/fhircraft/).

If you encounter any issues during the release process, please open an issue for assistance.

## Questions?

If you have any questions, feel free to open an issue or join the discussion!

---

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.
