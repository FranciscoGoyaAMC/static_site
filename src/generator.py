import os
from markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    """Gera um arquivo HTML a partir de um arquivo markdown e um template."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Lê o conteúdo do arquivo markdown
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # Lê o conteúdo do template
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extrai o título do markdown
    title = extract_title(markdown_content)

    # Substitui os espaços reservados no template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Substitui os links e fontes para usar o caminho base
    full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    # Certifica que o diretório de destino existe
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Escreve o conteúdo HTML no arquivo de destino
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(full_html)

    print(f"Page generated successfully at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Gera recursivamente páginas HTML a partir de arquivos markdown em um diretório."""
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Constrói os caminhos dos arquivos markdown e HTML
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")

                # Gera a página HTML
                generate_page(markdown_path, template_path, html_path, basepath)

