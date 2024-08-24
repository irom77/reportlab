from xmltags import replace_xml_content, get_para_by_tag, replace_xml_fstr, create_conf
from xml.etree import ElementTree as ET
import yaml
import pytest

# input.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <root>
#   <content>
#     <para><tag1></tag1>qwerty</para>
#     <para><tag4>qaz</tag4>asdfgh</para>
#     <tag2>Original content 2</tag2>
#     <sect><tag3>Original content 3</tag3></sect>
#     <tag3>Original content 3</tag3>
#     <tag5>Semicolon, inside</tag5>
#     <sect><tag5>Semicolon, inside</tag5></sect>
#   </content>
# </root>
@pytest.mark.skip(reason="This is no more used")
def test_replace_xml_content():
    tags1={
        'tag1': None,
        'tag2': 'new tag2 <tag>qwerty qaz<tag/>',
        # 'tag3': 'new tag3',
        'tag4': 'new tag4',
    }

    result_tree = replace_xml_content('tests/input.xml', 'tests/output.xml', tags1)
    result_tree = ET.parse('tests/output.xml')
    root = result_tree.getroot()
    assert root.find(".//tag3") is not None, "<tag3> element not found"
    assert root.find(".//tag3").text == "Original content 3", "Content of <tag3> does not match"
    assert root.find(".//tag2") is not None, "<tag2> element not found"
    tag2_element = root.find(".//tag2")
    assert tag2_element is not None, "<tag2> element not found"
    assert tag2_element.text == "new tag2 <tag>qwerty qaz<tag/>", f"Content of <tag2> does not match. Actual: {tag2_element.text}"
    assert root.find(".//tag1") is not None, "<tag1> element not found"
    assert root.find(".//tag4") is not None, "<tag4> element not found"
    assert root.find(".//tag4").text == "new tag4", "Content of <tag4> does not match"
    assert root.find(".//para/tag4").text == "new tag4", "Content of <para><tag4> does not match"
@pytest.mark.skip(reason="This is no more used")
def test_replace_xml_fstr():
    vars = {
        'var1': None,
        'var2': 'new var2 ',
        # 'var3': 'new var3',
        'var4': 'new var4',
    }
    
    replace_xml_fstr('tests/input_fstr.xml', 'tests/output_fstr.xml', vars)
    
    # Parse the output XML
    tree = ET.parse('tests/output_fstr.xml')
    root = tree.getroot()
    
    # Check if the variables are replaced correctly
    content = root.find('.//content')
    assert content is not None, "Content element not found"
    
    # Check if {var1} is not replaced (because its value is None)
    assert '{var1}' in ET.tostring(content, encoding='unicode'), "{var1} should not be replaced"
    
    # Check if {var2} is replaced
    assert 'new var2 ' in ET.tostring(content, encoding='unicode'), "{var2} should be replaced with 'new var2 '"
    
    # Check if {var3} is not replaced
    assert '{var3}' in ET.tostring(content, encoding='unicode'), "{var3} should not be replaced"
    
    # Check if {var4} is replaced
    assert 'new var4' in ET.tostring(content, encoding='unicode'), "{var4} should be replaced with 'new var4'"
    
    # Compare input and output files
    with open('tests/expected_fstr.xml', 'r') as input_file, open('tests/output_fstr.xml', 'r') as output_file:
        input_lines = input_file.readlines()
        output_lines = output_file.readlines()
        
        assert len(input_lines) == len(output_lines), "Input and output files have different number of lines"
        
        for i, (input_line, output_line) in enumerate(zip(input_lines, output_lines)):
            if input_line.strip() != output_line.strip():
                assert vars.get(input_line.strip('{}.')) is not None, f"Unexpected difference in line {i+1}"

# input.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <root>
#   <content>
#     <para><tag1></tag1>qwerty</para>
#     <para><tag4>qaz</tag4>asdfgh</para>
#     <tag2>Original content 2</tag2>
#     <sect><tag3>Original content 3</tag3></sect>
#     <tag3>Original content 3</tag3>
#     <tag5>Semicolon, inside</tag5>
#     <sect><tag5>Semicolon, inside</tag5></sect>
#   </content>
# </root>

def test_replace_fstr():
    from xmltags import replace_fstr
    
    vars = {
        'var2': 'new var2 ',
        'var4': 'new var4',
    }
    
    replace_fstr('tests/input_fstr.xml', 'tests/output_fstr.xml', vars)
    
    with open('tests/output_fstr.xml', 'r') as output_file, open('tests/expected_fstr.xml', 'r') as expected_file:
        output_content = output_file.read()
        expected_content = expected_file.read()
    
    assert output_content == expected_content, "The generated output_fstr.xml does not match expected_fstr.xml"

def test_create_conf():
    input_file = 'tests/config_input.xml'
    config_file = 'tests/config_output.yml'
    expected_file = 'tests/config_expected.yml'

    # Create the config file
    create_conf(input_file, config_file)

    # Read the generated config file
    with open(config_file, 'r') as f:
        generated_config = yaml.safe_load(f)

    # Read the expected config file
    with open(expected_file, 'r') as f:
        expected_config = yaml.safe_load(f)

    # Compare the generated config with the expected config
    assert generated_config == expected_config, "The generated config file does not match the expected config file"

    # Additional checks
    assert 'root' not in generated_config, "Root should not be a top-level key in the YAML file"
    
    # Check if only direct children of root are top-level keys
    tree = ET.parse(input_file)
    root = tree.getroot()
    direct_children = set(child.tag for child in root)
    assert set(generated_config.keys()) == direct_children, "Only direct children of root should be top-level keys"

    # Check if variables are correctly identified
    def check_variables(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and all(v == '' for v in value.values()):
                    # This is a variable dictionary
                    continue
                check_variables(value)
        elif isinstance(data, list):
            for item in data:
                check_variables(item)

    check_variables(generated_config)

def test_get_para_by_tag():    
    result=get_para_by_tag('tests/input.xml','root.content.para.tag4')
    assert result == 'qaz', "root.content.para.tag4 element not found"
    result=get_para_by_tag('tests/input.xml','root.content.tag5')
    assert result == 'Semicolon, inside', "root.content.tag5 element not found"
    result=get_para_by_tag('tests/input.xml','root.content.para')
    assert result == ['<para>qwerty<tag1></tag1></para>', '<para>asdfgh<tag4>qaz</tag4></para>']
    result=get_para_by_tag('tests/input.xml','root.content.sect')
    assert result == ['<sect><tag3>Original content 3</tag3></sect>', '<sect><tag5><bullet>&bull;</bullet>Semicolon, inside</tag5></sect>']
