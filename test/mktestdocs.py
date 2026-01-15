# Adapted from mktestdocs by koaning licensed under the Apache License 2.0
# Original source: https://github.com/koaning/mktestdocs/blob/main/src/mktestdocs/__main__.py

import inspect
import pathlib
import subprocess
import textwrap
import traceback

_executors = {}


def register_executor(lang, executor):
    """Add a new executor for markdown code blocks

    lang should be the tag used after the opening ```
    executor should be a callable that takes one argument:
        the code block found
    """
    _executors[lang] = executor


def exec_bash(source):
    """Exec the bash source given in a new subshell

    Does not return anything, but if any command returns not-0 an error
    will be raised
    """
    command = ["bash", "-e", "-u", "-c", source]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print("Bash execution failed:")
        print("=" * 60)
        if e.stderr:
            print("Error output:")
            print(e.stderr)
        print("\nFailed command:")
        print(source)
        print("=" * 60)
        raise


register_executor("bash", exec_bash)


def exec_python(source):
    """Exec the python source given in a new module namespace

    Does not return anything, but exceptions raised by the source
    will propagate out unmodified

    Preprocessing: Converts print() statements followed by #> lines
    into assert statements for testing.
    """
    # Preprocess the source to convert print/expected output patterns to assertions
    source = preprocess_print_assertions(source)

    try:
        # Compile first so we get proper line numbers in tracebacks
        code = compile(source, filename="<doctest>", mode="exec")
        exec(code, {"__name__": "__main__"})
    except Exception as e:
        # Extract line number from traceback
        tb = traceback.extract_tb(e.__traceback__)
        error_line = None
        for frame in tb:
            if frame.filename == "<doctest>":
                error_line = frame.lineno
                break

        # Print only lines around the error
        if error_line:
            lines = source.split("\n")
            context = 3  # lines before and after
            start = max(1, error_line - context)
            end = min(len(lines), error_line + context)
            print(f"\nDoctest Source Code Error Location:")
            for i in range(start, end + 1):
                marker = ">>>" if i == error_line else "   "
                print(f"{marker} {i:4d}: {lines[i-1]}")
        else:
            print("\nFull source:")
            for i, line in enumerate(source.split("\n"), 1):
                print(f"{i:4d}: {line}")
        print("=" * 60)
        raise


def preprocess_print_assertions(source):
    """Convert print() statements followed by #> lines into assert statements"""
    import re

    lines = source.split("\n")
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Look for print() statements with proper parentheses matching
        print_start = line.find("print(")
        if print_start != -1 and i + 1 < len(lines):
            # Find the matching closing parenthesis
            paren_count = 0
            start_pos = print_start + 6  # Start after 'print('
            end_pos = None

            for j in range(start_pos, len(line)):
                if line[j] == "(":
                    paren_count += 1
                elif line[j] == ")":
                    if paren_count == 0:
                        end_pos = j
                        break
                    paren_count -= 1

            if end_pos is not None:
                next_line = lines[i + 1].strip()

                # Check if the next line starts with #>
                if next_line.startswith("#>"):
                    # Extract the print argument and expected value
                    print_arg = line[start_pos:end_pos].strip()
                    expected_value = next_line[2:].strip()  # Remove #> prefix

                    # Create the assertion
                    # Handle string values by adding quotes if not already present
                    if not (
                        expected_value.startswith('"')
                        or expected_value.startswith("'")
                        or expected_value.isdigit()
                        or expected_value in ["True", "False", "None"]
                        or expected_value.startswith("[")
                        or expected_value.startswith("{")
                    ):
                        expected_value = f'"{expected_value}"'

                    # Preserve indentation from the original print line
                    indent = len(line) - len(line.lstrip())
                    # Escape quotes in expected_value for the error message
                    escaped_expected = expected_value.replace('"', '\\"')

                    # Create assertion that handles quote differences gracefully
                    assertion = f'assert (test_value := str({print_arg})) == (expected_value := str({expected_value})), f"Expected {{expected_value}}, got {{test_value}}"'
                    new_line = " " * indent + assertion
                    new_lines.append(new_line)

                    # Skip both the print line and the #> line
                    i += 2
                    continue

        # If not a print/expected pattern, keep the original line
        new_lines.append(line)
        i += 1

    return "\n".join(new_lines)


register_executor("", exec_python)
register_executor("python", exec_python)


def get_codeblock_members(*classes, lang="python"):
    """
    Grabs the docstrings of any methods of any classes that are passed in.
    """
    results = []
    for cl in classes:
        if cl.__doc__:
            results.append(cl)
        for name, member in inspect.getmembers(cl):
            if member.__doc__:
                results.append(member)
    return [m for m in results if len(grab_code_blocks(m.__doc__, lang=lang)) > 0]


def check_codeblock(block, lang="python"):
    """
    Cleans the found codeblock and checks if the proglang is correct.

    Returns an empty string if the codeblock is deemed invalid.

    Arguments:
        block: the code block to analyse
        lang: if not None, the language that is assigned to the codeblock
    """
    first_line = block.split("\n")[0]
    if lang:
        if first_line.lstrip()[3:] != lang:
            return ""
    return "\n".join(block.split("\n")[1:])


def grab_code_blocks(docstring, lang="python"):
    """
    Given a docstring, grab all the markdown codeblocks found in docstring.

    Arguments:
        docstring: the docstring to analyse
        lang: if not None, the language that is assigned to the codeblock
    """
    docstring = format_docstring(docstring)
    docstring = textwrap.dedent(docstring)
    in_block = False
    block = ""
    codeblocks = []
    for idx, line in enumerate(docstring.split("\n")):
        if "```" in line:
            if in_block:
                codeblocks.append(check_codeblock(block, lang=lang))
                block = ""
            in_block = not in_block
        if in_block:
            block += line + "\n"
    return [textwrap.dedent(c) for c in codeblocks if c != ""]


def format_docstring(docstring):
    """Formats docstring to be able to successfully go through dedent."""
    if docstring[:1] != "\n":
        return f"\n    {docstring}"
    return docstring


def check_docstring(obj, lang=""):
    """
    Given a function, test the contents of the docstring.
    """
    if lang not in _executors:
        raise LookupError(
            f"{lang} is not a supported language to check\n"
            "\tHint: you can add support for any language by using register_executor"
        )
    executor = _executors[lang]
    for b in grab_code_blocks(obj.__doc__, lang=lang):
        executor(b)


def check_raw_string(raw, lang="python"):
    """
    Given a raw string, test the contents.
    """
    if lang not in _executors:
        raise LookupError(
            f"{lang} is not a supported language to check\n"
            "\tHint: you can add support for any language by using register_executor"
        )
    executor = _executors[lang]
    for b in grab_code_blocks(raw, lang=lang):
        executor(b)


def check_raw_file_full(raw, lang="python"):
    if lang not in _executors:
        raise LookupError(
            f"{lang} is not a supported language to check\n"
            "\tHint: you can add support for any language by using register_executor"
        )
    executor = _executors[lang]
    all_code = ""
    for b in grab_code_blocks(raw, lang=lang):
        all_code = f"{all_code}\n{b}"
    executor(all_code)


def check_md_file(fpath, memory=False, lang="python"):
    """
    Given a markdown file, parse the contents for python code blocks
    and check that each independent block does not cause an error.

    Arguments:
        fpath: path to markdown file
        memory: whether or not previous code-blocks should be remembered
    """
    text = pathlib.Path(fpath).read_text()
    if not memory:
        check_raw_string(text, lang=lang)
    else:
        check_raw_file_full(text, lang=lang)
