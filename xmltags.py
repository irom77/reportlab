import xml.etree.ElementTree as ET
import html
import re
import yaml
from xml.parsers.expat import ParserCreate

def escape_xml_content(text):
    return html.escape(text, quote=False)

def replace_xml_content(input_file, output_file, tags):
    # Read the original file to preserve formatting
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Function to recursively process elements
    def process_element(element):
        tag = element.tag
        if tag in tags:
            if tags[tag] is None:
                # Preserve the tag but clear its content
                element.text = None
                element[:] = []  # Remove all children
            else:
                # Replace the content without escaping
                element.text = str(tags[tag])
                element[:] = []  # Remove all children
        for child in list(element):
            process_element(child)

    # Process the root and all its children
    process_element(root)

    # Convert the modified tree to a string, preserving original formatting
    def element_to_string(elem, level=0):
        indent = '  ' * level
        result = f'{indent}<{elem.tag}'
        if elem.attrib:
            attributes = ' '.join(f'{k}="{v}"' for k, v in elem.attrib.items())
            result += f' {attributes}'
        if elem.text or len(elem):
            result += '>'
            if elem.text:
                result += escape_xml_content(elem.text.strip())
            if len(elem):
                result += '\n'
                for child in elem:
                    result += element_to_string(child, level + 1)
                result += indent
            result += f'</{elem.tag}>'
        else:
            result += '/>'
        result += '\n'
        return result

    modified_content = element_to_string(root)

    # Write the modified content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Preserve the XML declaration
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        f.write(xml_declaration)
        f.write(modified_content.strip())

    return tree

def create_conf(input_file, config_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Function to recursively process XML elements
    def process_element(element):
        if len(element) == 0:
            # Leaf node
            return process_text(element.text.strip() if element.text else '')
        else:
            # Non-leaf node
            result = {}
            for child in element:
                child_result = process_element(child)
                if isinstance(child_result, dict) and len(child_result) == 1 and child.tag in child_result:
                    result[child.tag] = child_result[child.tag]
                else:
                    result[child.tag] = child_result
            return result

    # Function to process text and identify variables
    def process_text(text):
        variables = re.findall(r'\{([^}]+)\}', text)
        if variables:
            return {var: '' for var in variables}
        return text

    # Process only direct children of root
    config_data = {}
    for child in root:
        config_data[child.tag] = process_element(child)

    # Write the config data to YAML file
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False)

def replace_fstr(input_file, output_file, vars):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_var(match):
        var_name = match.group(1)
        return str(vars.get(var_name, match.group(0)))

    modified_content = re.sub(r'\{(\w+)\}', replace_var, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)

def get_para_by_tag(file_path, tag):
    class XMLParser:
        def __init__(self):
            self.root = None
            self.current = None
            self.stack = []

        def start(self, tag, attrs):
            elem = ET.Element(tag, attrs)
            if self.root is None:
                self.root = elem
            if self.current is not None:
                self.current.append(elem)
            self.stack.append(elem)
            self.current = elem

        def end(self, tag):
            self.stack.pop()
            if self.stack:
                self.current = self.stack[-1]
            else:
                self.current = None

        def data(self, data):
            if self.current is not None:
                if self.current.text is None:
                    self.current.text = data
                else:
                    self.current.text += data

    parser = XMLParser()
    p = ParserCreate()
    p.StartElementHandler = parser.start
    p.EndElementHandler = parser.end
    p.CharacterDataHandler = parser.data
    with open(file_path, 'rb') as file:
        p.ParseFile(file)
    root = parser.root

    tag_path = tag.split('.')
    current_elements = [root]
    for t in tag_path[1:]:
        next_elements = []
        for elem in current_elements:
            next_elements.extend(elem.findall(t))
        if not next_elements:
            return None
        current_elements = next_elements

    def element_to_string(elem):
        parts = []
        parts.append(f'<{elem.tag}')
        if elem.attrib:
            attributes = ' '.join(f'{k}="{v}"' for k, v in elem.attrib.items())
            parts.append(f' {attributes}')
        parts.append('>')

        if elem.text:
            parts.append(elem.text)

        for child in elem:
            parts.append(element_to_string(child))
            if child.tail:
                parts.append(child.tail)

        parts.append(f'</{elem.tag}>')
        return ''.join(parts)

    def get_para_by_tag(file_path, tag):
        tree = ET.parse(file_path)
        root = tree.getroot()

        tag_path = tag.split('.')
        current_elements = [root]
        for t in tag_path[1:]:
            next_elements = []
            for elem in current_elements:
                next_elements.extend(elem.findall(t))
            if not next_elements:
                return None
            current_elements = next_elements

        if len(current_elements) == 1:
            elem = current_elements[0]
            if len(elem) == 0 and not elem.attrib:
                return elem.text.strip() if elem.text else ''
            else:
                return element_to_string(elem)
        else:
            return [element_to_string(elem) for elem in current_elements]

    if len(current_elements) == 1:
        elem = current_elements[0]
        if len(elem) == 0 and not elem.attrib:
            return elem.text.strip() if elem.text else ''
        else:
            return element_to_string(elem)
    else:
        return [element_to_string(elem) for elem in current_elements]

def replace_xml_fstr(input_file, output_file, vars):
    # Read the original file to preserve formatting
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Function to recursively process elements and their attributes
    def process_element(element):
        # Replace variables in element text
        if element.text:
            for var, value in vars.items():
                if value is not None:
                    element.text = element.text.replace(f'{{{var}}}', str(value))
        
        # Replace variables in element tail
        if element.tail:
            for var, value in vars.items():
                if value is not None:
                    element.tail = element.tail.replace(f'{{{var}}}', str(value))
        
        # Replace variables in attributes
        for attr, attr_value in element.attrib.items():
            for var, value in vars.items():
                if value is not None:
                    element.attrib[attr] = attr_value.replace(f'{{{var}}}', str(value))
        
        # Process child elements
        for child in element:
            process_element(child)

    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Process the root and all its children
    process_element(root)

    # Custom function to convert element tree to string
    def element_to_string(elem, level=0):
        indent = '  ' * level
        result = f'{indent}<{elem.tag}'
        if elem.attrib:
            attributes = ' '.join(f'{k}="{v}"' for k, v in elem.attrib.items())
            result += f' {attributes}'
        if elem.text or len(elem):
            result += '>'
            if elem.text:
                result += html.escape(elem.text)
            for child in elem:
                result += '\n' + element_to_string(child, level + 1)
            if len(elem):
                result += '\n' + indent
            result += f'</{elem.tag}>'
        else:
            result += '></{elem.tag}>'  # Use full closing tag for empty elements
        if elem.tail:
            result += html.escape(elem.tail)
        return result

    # Write the modified content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(element_to_string(root).rstrip() + '\n')

    return tree
