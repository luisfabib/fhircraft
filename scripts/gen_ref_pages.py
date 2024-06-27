"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / ""  

for path in sorted(src.rglob("*.py")):  
    try:
        module_path = path.relative_to(src).with_suffix("")  
        doc_path = path.relative_to(src).with_suffix(".md")  
        full_doc_path = Path("API-reference", doc_path)  

        parts = tuple(module_path.parts)

        if parts[-1] == "__init__":  
            continue
        elif parts[-1] == "__main__" or parts[0] != "fhircraft":
            continue
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:  
            identifier = ".".join(parts)  
            print("::: " + identifier, file=fd)  
            mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))
    except: pass