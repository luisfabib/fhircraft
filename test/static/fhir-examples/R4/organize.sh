#!/usr/bin/env bash
# ------------------------------------------------------------
# Purpose: From the current directory, copy ONE file for each
#          distinct prefix (text before the first hyphen) into
#          a fresh directory called “unique‑prefixes”.
# ------------------------------------------------------------

# 1️⃣ Destination folder – change the name if you like
dest="unique-prefixes"
mkdir -p "$dest"

# 2️⃣ Declare an associative array to remember seen prefixes
declare -A seen

# 3️⃣ Iterate over *all* regular files in the current directory
#    (handles spaces, newlines, etc. safely)
while IFS= read -r -d '' file; do
    # Strip the leading "./" that find adds
    base="${file#./}"

    # Extract the prefix – text before the first hyphen
    # If there is no hyphen, the whole name becomes the prefix
    prefix="${base%%-*}"

    # If we haven’t copied a file with this prefix yet …
    if [[ -z "${seen[$prefix]}" ]]; then
        # … copy it to the destination directory
        cp -- "$base" "$dest/"

        # Mark this prefix as “handled”
        seen[$prefix]=1
    fi
done < <(find . -maxdepth 1 -type f -print0)

# -----------------------------------------------------------------
# 4️⃣ Cleanup: remove any “*.profile.json” files from the output dir
# -----------------------------------------------------------------
shopt -s nullglob                     # avoid errors if no matches
for prof in "$dest"/*.profile.json; do
    rm -f -- "$prof"
done
shopt -u nullglob

echo "Done. Unique‑prefix files are in ./$dest"
echo "Any *.profile.json files have been removed."
