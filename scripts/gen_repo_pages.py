import os
from pathlib import Path
import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / ""


def print_file_contents(filename, file=None, changes=None):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read() if not changes else changes(f.read())
            print(content, file=file)
    else:
        print(f"{filename} not found.\n", file=file)


full_doc_path = Path("community", "license.md")
with mkdocs_gen_files.open(full_doc_path, "w") as fd:
    print_file_contents("LICENSE", file=fd)

full_doc_path = Path("community", "code_of_conduct.md")
with mkdocs_gen_files.open(full_doc_path, "w") as fd:
    print_file_contents("CODE_OF_CONDUCT.md", file=fd)


def _prepare_changelog(content: str) -> str:
    header = """---
hide:
  - navigation
---"""
    content = header + content
    return (
        content.replace("# Changelog", "")
        .replace("[GitHub Release]", "[:material-github: GitHub Release]")
        .replace("[Full Changelog]", "[:material-code-json: Full Changelog]")
    )


full_doc_path = Path("changelog.md")
with mkdocs_gen_files.open(full_doc_path, "w") as fd:
    print_file_contents(
        "CHANGELOG.md",
        file=fd,
        changes=_prepare_changelog,
    )
