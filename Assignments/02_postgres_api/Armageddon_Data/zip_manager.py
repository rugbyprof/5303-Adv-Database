"""
zip_manager.py — Zip and unzip data files in a directory.

Usage:
    python zip_manager.py zip [directory]
        Compress all .json, .geojson, and .csv files into individual .zip archives,
        then rename the originals to hidden dot-files (e.g. data.csv -> .data.csv)
        so they are excluded from git commits. Skips files already up to date.

    python zip_manager.py unzip [directory]
        Extract all .zip files into the same directory, restoring original filenames.
        Skips files whose extracted content already matches the zip.

    [directory] is optional and defaults to the current working directory.

Examples:
    python zip_manager.py zip
    python zip_manager.py zip /path/to/data
    python zip_manager.py unzip
    python zip_manager.py unzip /path/to/data

Workflow:
    1. Run `zip` to compress data files and hide the originals with a dot-prefix.
    2. Commit only the .zip files. Add the following to .gitignore to exclude originals:
           *.json
           *.geojson
           *.csv
    3. Collaborators run `unzip` after cloning/pulling to restore working files.
    4. To update a file: rename .filename.ext back to filename.ext, edit it,
       then run `zip` again.
"""

import argparse
import zlib
import zipfile
from pathlib import Path


# File extensions that will be compressed when running the 'zip' action
ZIPPABLE_EXTENSIONS = {".json", ".geojson", ".csv"}


def crc32_of_file(path: Path) -> int:
    """Compute the CRC32 checksum of a file's raw bytes."""
    return zlib.crc32(path.read_bytes()) & 0xFFFFFFFF


def zip_is_current(zip_path: Path, source: Path) -> bool:
    """Return True if zip_path exists and already contains an up-to-date copy of source."""
    if not zip_path.exists():
        return False
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            info = zf.getinfo(source.name)
            # Compare the CRC stored in the archive against the current file's CRC
            return info.CRC == crc32_of_file(source)
    except (KeyError, zipfile.BadZipFile):
        return False


def hidden_is_current(source: Path, hidden: Path) -> bool:
    """Return True if the hidden dot-file exists and has identical content to source."""
    if not hidden.exists():
        return False
    return source.read_bytes() == hidden.read_bytes()


def extracted_is_current(zip_info: zipfile.ZipInfo, out_path: Path) -> bool:
    """Return True if out_path already exists and its CRC matches what is stored in the zip."""
    if not out_path.exists():
        return False
    return crc32_of_file(out_path) == zip_info.CRC


def zip_files(directory: Path):
    """
    Zip each visible .json/.geojson/.csv file into its own .zip archive,
    write a hidden dot-prefixed copy of the original, then remove the original.
    Skips any file where both the zip and the dot-file are already current.
    """
    # Only target non-hidden files with a zippable extension
    targets = [
        f
        for f in directory.iterdir()
        if f.is_file()
        and not f.name.startswith(".")
        and f.suffix.lower() in ZIPPABLE_EXTENSIONS
    ]
    if not targets:
        print("No .json, .geojson, or .csv files found to zip.")
        return

    for f in targets:
        zip_path = f.with_suffix(".zip")
        hidden = f.parent / f".{f.name}"  # e.g. data.csv -> .data.csv

        zip_current = zip_is_current(zip_path, f)
        hidden_current = hidden_is_current(f, hidden)

        # Both already reflect the current file — nothing to do
        if zip_current and hidden_current:
            print(f"Skipped (unchanged): {f.name}")
            continue

        # (Re)create the zip archive if the stored content differs from the source
        if not zip_current:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(f, f.name)
            print(f"Zipped:  {f.name} -> {zip_path.name}")

        # Write (or overwrite) the hidden dot-file copy
        if not hidden_current:
            hidden.write_bytes(f.read_bytes())
            print(f"Hidden:  {f.name} -> {hidden.name}")

        # Remove the visible original so it stays out of git
        f.unlink()
        print(f"Removed: {f.name}")


def unzip_files(directory: Path):
    """
    Extract all .zip files into the same directory.
    Skips any member whose extracted file already matches the CRC stored in the zip.
    """
    targets = [
        f for f in directory.iterdir() if f.is_file() and f.suffix.lower() == ".zip"
    ]
    if not targets:
        print("No .zip files found to unzip.")
        return

    for zip_path in targets:
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for info in zf.infolist():
                    out_path = directory / info.filename
                    if extracted_is_current(info, out_path):
                        print(f"Skipped (unchanged): {info.filename}")
                        continue
                    zf.extract(info, directory)
                    print(f"Extracted: {zip_path.name} -> {info.filename}")
        except zipfile.BadZipFile:
            print(f"Error: {zip_path.name} is not a valid zip file, skipping.")


def main():
    parser = argparse.ArgumentParser(
        description="Zip or unzip data files (.json, .geojson, .csv).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("action", choices=["zip", "unzip"], help="Action to perform")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to operate on (default: current directory)",
    )
    args = parser.parse_args()
    directory = Path(args.directory).resolve()

    if not directory.is_dir():
        print(f"Error: {directory} is not a valid directory.")
        return

    if args.action == "zip":
        zip_files(directory)
    else:
        unzip_files(directory)


if __name__ == "__main__":
    main()
