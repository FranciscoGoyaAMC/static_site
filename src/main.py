import os
import shutil
import sys
from copy_directory import copy_directory
from generator import generate_pages_recursive

DOCS_DIR = "docs"
STATIC_DIR = "static"
CONTENT_DIR = "content"
TEMPLATE_FILE = "template.html"

def main():
    # Pegando o caminho base do argumento de linha de comando ou usando o padrão "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # 1. Removendo tudo do diretório docs se existir
    if os.path.exists(DOCS_DIR):
        print(f"Deleting {DOCS_DIR} directory...")
        shutil.rmtree(DOCS_DIR)

    # 2. Copiando arquivos estáticos para o diretório docs
    print(f"Copying files from {STATIC_DIR} to {DOCS_DIR}...")
    copy_directory(STATIC_DIR, DOCS_DIR)

    # 3. Gerando recursivamente páginas HTML a partir dos arquivos Markdown
    print(f"Generating pages from {CONTENT_DIR} to {DOCS_DIR} using {TEMPLATE_FILE}...")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, DOCS_DIR, basepath)

    print("Site generation complete!")

if __name__ == "__main__":
    main()
