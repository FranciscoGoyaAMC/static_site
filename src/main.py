import os
import shutil
from copy_directory import copy_directory
from generator import generate_pages_recursive

PUBLIC_DIR = "public"
STATIC_DIR = "static"
CONTENT_DIR = "content"
TEMPLATE_FILE = "template.html"

def main():
    # 1. Remove tudo de public/
    if os.path.exists(PUBLIC_DIR):
        print(f"Deleting {PUBLIC_DIR} directory...")
        shutil.rmtree(PUBLIC_DIR)

    # 2. Copia os arquivos de static/ para public/
    print(f"Copying files from {STATIC_DIR} to {PUBLIC_DIR}...")
    copy_directory(STATIC_DIR, PUBLIC_DIR)

    # 3. Gera páginas HTML recursivamente
    print(f"Generating pages from {CONTENT_DIR} to {PUBLIC_DIR} using {TEMPLATE_FILE}...")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, PUBLIC_DIR)

    print("Site generation complete!")

if __name__ == "__main__":
    main()
