import os
import shutil
import sys
from copy_directory import copy_directory
from generator import generate_pages_recursive

DOCS_DIR = "docs/static_site"
STATIC_DIR = "static"
CONTENT_DIR = "content"
TEMPLATE_FILE = "template.html"

# Função para copiar arquivos estáticos
def copy_static_files():
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)  # Remove o diretório existente
    shutil.copytree(STATIC_DIR, DOCS_DIR)  # Copia o diretório static para docs/static_site

def main():
    # Pegando o caminho base do argumento de linha de comando ou usando o padrão "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copiar arquivos do diretório static para docs/static_site
    copy_static_files()

    # 3. Gerando recursivamente páginas HTML a partir dos arquivos Markdown
    print(f"Generating pages from {CONTENT_DIR} to {DOCS_DIR} using {TEMPLATE_FILE}...")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, DOCS_DIR, basepath)

    print("Site generation complete!")

if __name__ == "__main__":
    main()
