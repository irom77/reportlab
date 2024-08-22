import xml.etree.ElementTree as ET

def replace_xml_content(input_file, output_file, tags):
    # Parse the XML file
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(input_file, parser)
    root = tree.getroot()

    # Function to recursively process elements
    def process_element(element):
        tag = element.tag
        if tag in tags:
            if tags[tag] is None:
                # Preserve the tag but clear its content
                element.clear()
                element.text = None
            else:
                # Replace the content
                element.clear()
                element.text = str(tags[tag])
        for child in list(element):
            process_element(child)

    # Process the root and all its children
    process_element(root)

    # Write the modified XML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=False)
    
    # Pretty print the output
    xml_string = ET.tostring(root, encoding='unicode', method='xml')
    from xml.dom import minidom
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml[pretty_xml.index('\n')+1:])

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
