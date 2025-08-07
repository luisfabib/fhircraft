import os
from pathlib import Path
import mkdocs_gen_files 

root = Path(__file__).parent.parent
src = root / "" 

def print_file_contents(filename, file=None):
    if os.path.isfile(filename):
        print(f"--- {filename} ---")
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read(), file=file)
    else:
        print(f"{filename} not found.\n", file=file)


full_doc_path = Path("community", 'license.md')
with mkdocs_gen_files.open(full_doc_path, "w") as fd:  
    print_file_contents('LICENSE', file=fd) 

full_doc_path = Path("community", 'code_of_conduct.md')
with mkdocs_gen_files.open(full_doc_path, "w") as fd:  
    print_file_contents('CODE_OF_CONDUCT.md', file=fd) 