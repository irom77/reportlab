import xml.etree.ElementTree as ET
import html

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
                result += escape_xml_content(elem.text)
            for child in elem:
                result += element_to_string(child, level + 1)
            result += f'</{elem.tag}>'
        else:
            result += '/>'
        if level > 0:
            result = '\n' + result
        return result

    modified_content = element_to_string(root)

    # Write the modified content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(modified_content)

    return tree

def get_para_by_tag(file_path, tag):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Split the tag path
    tag_path = tag.split('.')

    # Navigate through the XML tree
    current_elements = [root]
    for t in tag_path[1:]:  # Skip 'root' as we start from root
        next_elements = []
        for elem in current_elements:
            next_elements.extend(elem.findall(t))
        if not next_elements:
            return None  # Tag not found
        current_elements = next_elements

    # Process the final elements
    if len(current_elements) == 1:
        # If there's only one element
        elem = current_elements[0]
        if len(elem) == 0 and not elem.attrib:
            # If it's a leaf node without attributes, return its text content
            return elem.text.strip() if elem.text else ''
        else:
            # If it has children or attributes, return its string representation
            return ET.tostring(elem, encoding='unicode', method='xml', short_empty_elements=False).strip()
    else:
        # If there are multiple elements, return a list
        return [ET.tostring(elem, encoding='unicode', method='xml', short_empty_elements=False).strip() for elem in current_elements]
