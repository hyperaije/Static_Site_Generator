import os
import shutil
from blockmarkdown import markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode

def copy_static_to_public(source_directory="./static", target_directory="./public", first_call=False):
    if first_call == True:
        if os.path.exists(target_directory):
            shutil.rmtree(target_directory)
        os.makedirs(target_directory, exist_ok=True)
    for item in os.listdir(source_directory):
        source_path = os.path.join(source_directory, item)
        target_path = os.path.join(target_directory, item)
        
        if os.path.isfile(source_path):
            #logs the copied file to the terminal before copying it
            print(f"Copying {source_path} to {target_path}")
            shutil.copy(source_path, target_path)
        elif os.path.isdir(source_path):
            #log directory creation
            print(f"Creating {target_path}")
            os.makedirs(target_path, exist_ok=True)
            copy_static_to_public(source_path, target_path)

def generate_pages_recursive(from_path, template_path, dest_path):
    for item in os.listdir(from_path):
        item_path = os.path.join(from_path, item)
        item_dest = os.path.join(dest_path, item)

        if os.path.isfile(item_path) and item.lower().endswith(".md"):
            item_dest = item_dest[:-3] + ".html"
            #logs the copy info into the terminal
            print(f"Generating page from {item_path} to {item_dest} using {template_path}")
            with open(item_path) as f:
                markdown = f.read()
            with open(template_path) as f2:
                template = f2.read()

            node = markdown_to_html_node(markdown)
            html_string = node.to_html()
            title = extract_title(markdown)

            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html_string)

            os.makedirs(os.path.dirname(item_dest), exist_ok=True)
            with open(item_dest, "w") as f3:
                f3.write(template)

        elif os.path.isdir(item_path):
            os.makedirs(item_dest, exist_ok=True)
            generate_pages_recursive(item_path, template_path, item_dest)

def main():
    if not os.path.exists("./static"):
        raise Exception("Error: No static directory found in this directory")
        
    if not os.path.exists("./content"):
        raise Exception("Error: No content directory found in this directory")

    os.makedirs("./public", exist_ok=True)

    copy_static_to_public(first_call=True)
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()