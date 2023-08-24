import tomllib
import pathlib
import re
import os
from .custom_exceptions import ExtensionNotFound, TooManyExtensions, PathIsNotPosixPath

# Setup configs
with open('config.toml', 'rb') as config_toml:
    config = tomllib.load(config_toml)


class regex_expressions:
    """Implements all regex lookups"""
    def __init__(self):
        self.content_reg = r'(\S*)'  # initial setup
        self.replace_reg = r'\(\\S\*\)'  # for regex loopkups
        self.link = rf'<!--\${self.content_reg}-->'
        self.extend = rf'<!--@{self.content_reg}-->'
        self.constant = rf'<!--#{self.content_reg}-->'
        self.block = rf'<!--%(?!endblock){self.content_reg}-->((.|\n)*?)<!--%endblock-->'

    def link_gen(self, value):
        return re.sub(self.replace_reg, value, self.link)

    def constant_gen(self, value):
        return re.sub(self.replace_reg, value, self.constant)

    def extend_gen(self, value):
        return re.sub(self.replace_reg, value, self.extend)

    def block_gen(self, value):
        return re.sub(self.replace_reg, value, self.block)


regex = regex_expressions()


def environment(pwd: object):
    """Takes in a path of base directory.
    Checks whether all the files exist.
    """
    if not isinstance(pwd, pathlib.PosixPath):
        raise PathIsNotPosixPath('The path supplied to environemnt is not of type pathlib.PosixPath')
    if not os.path.exists(pwd/config['template_folder']):
        raise FileNotFoundError()


# Scan Template Folder
def scan_template_folder() -> dict:
    """Scan through all files and sub-dirs in the template
    folder.
    Returns dictionary of all files.
    """
    template_folder_content = {}
    for root, dirs, files in os.walk(config['template_folder']):
        for file in files:
            if template_folder_content.get(file):
                raise RuntimeError(f'The file "{file}" already exists at {os.path.join(root, file)}.')
            template_folder_content[
                file
            ] = os.path.join(root, file)
    return template_folder_content


# Generate complete HTML
def build_links(parent_file_location: str) -> str:
    """Takes in a file location.
    Recusively searches through all links and generates the file
    needed.
    Returns the completed page that was requested.
    """
    with open(parent_file_location) as file:
        parent_file_data = file.read()

    links_founds = re.findall(regex.link, parent_file_data)
    if links_founds:
        for link_name in links_founds:
            try:
                source_file = build_links(template_content[link_name])
                sub_link = regex.link_gen(link_name)
                # Clean data of blocks
                source_file = re.sub(regex.block, '', source_file)
                ###
                parent_file_data = re.sub(sub_link,
                                          source_file,
                                          parent_file_data)
            except KeyError:
                raise FileNotFoundError(f'"{link_name}" file was not found.')

    parent_file_data = parent_file_data.rstrip()
    return parent_file_data


def build_constants(parent_file_data: str) -> str:
    """Searches all constants defined on the file. Applies
    constants defined in the 'config.toml' file.
    Returns constants found subbed in with actual values.
    """
    try:
        config_constants = config['constants'][0]
        constants_found = re.findall(regex.constant, parent_file_data)
        for constant in constants_found:
            config_value = config_constants.get(constant)
            if config_value:
                sub_constant = regex.constant_gen(constant)
                config_value = str(config_value)
                try:
                    parent_file_data = re.sub(sub_constant, config_value, parent_file_data)
                except Exception as e:
                    print(e)
    except KeyError:
        print('Key Error encoutered in build_constants')
    finally:
        return parent_file_data


def validate_extensions(parent_file_data: str, *args) -> object:
    """Takes in a file and checks how many extensions exists.
    The function will also store blocks and remove blocks from the
    origin file.
    Returns an object with the cleaned content and block data.
    """
    class parent_file_class:
        def __init__(self, parent_file_data, content_block):
            self.parent_file_data = parent_file_data
            self.content_block = content_block

    extensions_found = re.findall(regex.extend, parent_file_data)
    if len(extensions_found) > 1:
        raise TooManyExtensions(f'Too many extensions found in "{args[0]}"')
    if extensions_found:
        try:
            template_content[extensions_found[0]]
        except KeyError:
            raise FileNotFoundError(f'"{extensions_found[0]}" file not found.')

    content_block = re.findall(regex.block, parent_file_data)
    if not content_block:
        parent = parent_file_class(parent_file_data, None)
        return parent

    if content_block and not extensions_found:
        pass
        # raise ExtensionNotFound("Block exists but nothing is imported.")

    # Clean up data
    parent_file_data = re.sub(regex.block, '<!--#DELETE_LINE#-->', parent_file_data)
    parent_file_array = parent_file_data.split('\n')
    parent_file_array_temp = []
    for element in parent_file_array:
        should_delete = re.findall(r'<!--#DELETE_LINE#-->', element)
        if not should_delete:
            parent_file_array_temp.append(element)
    parent_file_data = '\n'.join(parent_file_array_temp)
    content_block_array_temp = []
    for tuple_element in content_block:
        # Strip \n values
        local_content_block_array = []
        for element in tuple_element:
            if not element == '\n':
                element = element.strip()
                local_content_block_array.append(element)
        content_block_array_temp.append(tuple(local_content_block_array))
        local_content_block_array = []
    content_block = list(content_block_array_temp)
    ###
    content_block_dict = {}
    for content in content_block:
        content_block_dict[content[0]] = content[1:]
    parent = parent_file_class(parent_file_data, content_block_dict)
    return parent


def build_blocks(parent_file_object: object) -> str:
    extension_name = re.findall(regex.extend, parent_file_object.parent_file_data)
    if not extension_name:
        return parent_file_object.parent_file_data
    extension_name = extension_name[0]
    with open(template_content[extension_name]) as extended_file:
        extended_file_data = extended_file.read()
        extended_file_data = extended_file_data.strip()

    for block_name in parent_file_object.content_block:
        sub_block = regex.block_gen(block_name)
        extended_file_data = re.sub(sub_block,
                                    parent_file_object.content_block[block_name][0],
                                    extended_file_data)

        sub_extend = regex.extend_gen(extension_name)
        parent_file_object.parent_file_data = re.sub(sub_extend,
                                                     extended_file_data,
                                                     parent_file_object.parent_file_data)
    return parent_file_object.parent_file_data


def build_file(parent_file_location: str, **kwargs) -> str:
    """Takes in a file and applies build functions.
    Returns the filled in file.

    Build Order:
    1. Build Links
    2. Build Constants
    3. Validate Extensions
    4. Build Blocks
    """
    file = build_links(parent_file_location)
    file = build_constants(file)
    file_object = validate_extensions(file, kwargs['file_name'])
    file = build_blocks(file_object)
    return file


# Scan folder and construct files
template_content = scan_template_folder()


def main() -> dict:
    """Uses template_content to build all
    files in the template folder location.

    Returns a dictionary with the associated file name
    and HTML code for the file.
    """
    all_built_files = {}
    for _ in template_content:
        all_built_files[_] = build_file(template_content[_], file_name=_)
    return all_built_files
