import os
import urllib.request
import zipfile
import shutil
import sys

# URL for Poppler for Windows (Release 24.02.0-0)
POPPLER_URL = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip"
POPPLER_ZIP = "poppler.zip"
EXTRACT_DIR = "poppler_temp"
TARGET_DIR = "poppler"

def install_poppler():
    if os.path.exists(TARGET_DIR):
        print(f"'{TARGET_DIR}' directory already exists. Skipping download.")
        return

    print(f"Downloading Poppler from {POPPLER_URL}...")
    try:
        urllib.request.urlretrieve(POPPLER_URL, POPPLER_ZIP)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download: {e}")
        return

    print("Extracting...")
    with zipfile.ZipFile(POPPLER_ZIP, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # Move the inner directory to the final target
    # The zip usually contains a folder like 'Release-24.02.0-0', we want the 'poppler-xx/bin' structure or just the root.
    # Let's see what's inside. Usually it has a 'Library' or 'bin' folder or a versioned folder.
    
    # Check structure
    items = os.listdir(EXTRACT_DIR)
    if len(items) == 1 and os.path.isdir(os.path.join(EXTRACT_DIR, items[0])):
        # It's inside a subdirectory
        source_inner = os.path.join(EXTRACT_DIR, items[0])
        # We want to move contents of source_inner to TARGET_DIR
        shutil.move(source_inner, TARGET_DIR)
    else:
        # It's direct
        shutil.move(EXTRACT_DIR, TARGET_DIR)

    # Cleanup
    if os.path.exists(POPPLER_ZIP):
        os.remove(POPPLER_ZIP)
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)

    print(f"Poppler installed to '{os.path.abspath(TARGET_DIR)}'")
    
    # Verify bin path
    bin_path = os.path.join(TARGET_DIR, "Library", "bin")
    if not os.path.exists(bin_path):
         # Try alternative structure
         bin_path = os.path.join(TARGET_DIR, "bin")

    if os.path.exists(bin_path):
        print(f"Binaries found at: {bin_path}")
    else:
        print("Warning: Could not locate 'bin' directory inside poppler.")

if __name__ == "__main__":
    install_poppler()
