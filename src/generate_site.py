import os
from generate_page import generate_page


def generate_site(basepath: str, from_path: str, template_path: str, dest_path: str):
    if not os.path.exists(from_path):
        raise Exception("Error: Invalid source directory file path")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    _generate_pages_recursive(basepath, from_path, template_path, dest_path)
    
    return

def _generate_pages_recursive(basepath: str, from_path: str, template_path: str, dest_path:str):
    from_items = os.listdir(from_path)
    for item in from_items:
        item_path = os.path.join(from_path, item)
        if os.path.isfile(item_path):
            item_dest_path = os.path.join(dest_path, md_to_html_file_name_converter(item))
            generate_page(basepath, item_path, template_path, item_dest_path)
        else:
            item_dest_path = os.path.join(dest_path, item)
            os.makedirs(item_dest_path)
            _generate_pages_recursive(basepath, item_path, template_path, item_dest_path)
    
    return

def md_to_html_file_name_converter(file_name: str):
    if file_name.endswith(".md"):
        return file_name[:-3] + ".html"
    elif file_name.find(".") >= 0:
        return file_name + "html"
    else:
        raise Exception("Error: files must be in markdown format")
