import os
from markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    """Generates an HTML page from a markdown file using a template."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML file
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(full_html)

    print(f"Page generated successfully at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Recursively generates HTML pages for all markdown files in the content directory."""
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Construct paths
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")

                # Generate the page
                generate_page(markdown_path, template_path, html_path)

