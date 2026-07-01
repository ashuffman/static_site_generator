from markdown_to_html import markdown_to_html_node, markdown_to_blocks
import os

def generate_page(basepath: str, from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_md = get_file_contents(from_path)
    template_html = get_file_contents(template_path)
    content = markdown_to_html(from_md)
    title = extract_title(from_md)
    html = customize_template(basepath, template_html, title, content)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(html)

def extract_title(markdown: str)-> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("Error: no title detected")

def get_file_contents(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()
    
def markdown_to_html(markdown: str) -> str:
    node = markdown_to_html_node(markdown)
    return node.to_html()

def customize_template(basepath: str, template_html: str, title: str, content: str):
    html_title = template_html.replace("{{ Title }}", title)
    html_content = html_title.replace("{{ Content }}", content)
    html_href = html_content.replace('href="/',f'href="{basepath}')
    html = html_href.replace('src="/', f'src="{basepath}')
    return html

