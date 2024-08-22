import xml.etree.ElementTree as ET

def replace_xml_content(input_file, output_file, tags):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Function to recursively process elements
    def process_element(element):
        tag = element.tag
        if tag in tags and tags[tag] is not None:
            element.text = str(tags[tag])
        for child in element:
            process_element(child)

    # Process the root and all its children
    process_element(root)

    # Write the modified XML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
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
        if len(elem) == 0:
            # If it's a leaf node, return its text content or string representation
            return elem.text.strip() if elem.text and elem.text.strip() else ET.tostring(elem, encoding='unicode').strip()
        else:
            # If it has children, return string representations of all child elements
            return ''.join([ET.tostring(child, encoding='unicode').strip() for child in elem])
    else:
        # If there are multiple elements, return a list
        result = []
        for elem in current_elements:
            if len(elem) == 0:
                # If it's a leaf node, add its text content or string representation
                result.append(elem.text.strip() if elem.text and elem.text.strip() else ET.tostring(elem, encoding='unicode').strip())
            else:
                # If it has children, add string representations of all child elements
                result.extend([ET.tostring(child, encoding='unicode').strip() for child in elem])
        return result