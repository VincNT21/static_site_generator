import shutil
import os
from textnode import *
from MD_to_HTML import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

def main():
    path_static = '/home/vincnt/workspace/SSG/static_site_generator/static'
    path_public = '/home/vincnt/workspace/SSG/static_site_generator/public'
    path_content = '/home/vincnt/workspace/SSG/static_site_generator/content'
    path_content_index = '/home/vincnt/workspace/SSG/static_site_generator/content/index.md'
    path_public_index = '/home/vincnt/workspace/SSG/static_site_generator/public/index.html'
    path_template = '/home/vincnt/workspace/SSG/static_site_generator/template.html'
    copy_contents(path_static, path_public)
    generate_pages_recursive(path_content, path_template, path_public)

def copy_contents(from_path, to_path):
    if os.path.exists(to_path):
        try:
            shutil.rmtree(to_path)
        except PermissionError:
            print(f'Permission denied: Unable to delete {to_path}')
            return
        except Exception as e:
            print(f'Unexpected error while deleting {to_path}: {e}')
            return
    try:
        os.mkdir(to_path)
    except PermissionError:
        print(f'Permission denied: Unable to create directory {to_path}')
        return
    except Exception as e:
        print(f'Unexpected error while creating {to_path}: {e}')
        return
    for item in os.listdir(from_path):
        current_path = os.path.join(from_path, item)
        new_path = os.path.join(to_path, item)
        if os.path.isfile(current_path):
            try:
                print(f'Copying file from {current_path} to {new_path}')
                shutil.copy(current_path, new_path)
            except PermissionError:
                print(f'Permission denied: Unable to copy file {current_path}')
            except Exception as e:
                print(f'Unexpected error while copying {current_path}: {e}')
        else:
            try:
                print(f'Creating new folder : {new_path}')
                os.mkdir(new_path)
            except PermissionError:
                print(f'Permission denied: Unable to create folder {new_path}')
            except Exception as e:
                print(f'Unexpected error while creating folder {current_path}: {e}')
            copy_contents(current_path, new_path)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    try:
        with open(from_path, 'r') as md_file:
            md_content = md_file.read()
    except PermissionError:
        print(f'Permission denied: Unable to read {from_path}')
        return
    except Exception as e:
        print(f'Unexpected error while reading {from_path}: {e}')
        return
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except PermissionError:
        print(f'Permission denied: Unable to read {template_path}')
        return
    except Exception as e:
        print(f'Unexpected error while reading {template_path}: {e}')
        return
    HTML_string = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)
    template_content = template_content.replace('{{ Title }}', page_title)
    template_content = template_content.replace('{{ Content }}', HTML_string)
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    except PermissionError:
        print(f'Permission denied: Unable to create {dest_path}')
        return
    except Exception as e:
        print(f'Unexpected error while creating {dest_path}: {e}')
        return
    try:
        with open(dest_path, 'w') as file:
            file.write(template_content)
    except PermissionError:
        print(f'Permission denied: Unable to write {dest_path}')
        return
    except Exception as e:
        print(f'Unexpected error while writing {dest_path}: {e}')
        return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    md_files = searching_md_files(dir_path_content)
    for file in md_files:
        relative_path = os.path.relpath(file, dir_path_content)
        relative_path = relative_path.removesuffix('.md') + '.html'
        generate_page(file, template_path, os.path.join(dest_dir_path, relative_path))


def searching_md_files(dir_path):
    md_list = []
    for entry in os.listdir(dir_path):
        entry_path = os.path.join(dir_path, entry)
        if os.path.isfile(entry_path) and '.md' in entry:
            md_list.append(entry_path)
        if os.path.isfile(entry_path):
            continue
        else:
            md_list.extend(searching_md_files(entry_path))
    return md_list
    


main()