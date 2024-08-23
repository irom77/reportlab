from  xmltags import replace_xml_content, get_para_by_tag, replace_xml_fstr
from xml.etree import ElementTree as ET

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
def test2_replace_xml_content():
    tags1={
        'between_dates': 'From July 1 to 30',
        'inbound_messages': '10',
        'blocked_messages': '5',
        'delivered_messages': '5'
    }

    replace_xml_content('tests/_input.xml', 'tests/_output.xml', tags1)
    
    # Read and compare the contents of _output.xml and _expected_output.xml
    with open('tests/_output.xml', 'r') as output_file, open('tests/_expected_output.xml', 'r') as expected_file:
        output_content = output_file.read()
        expected_content = expected_file.read()
    
    assert output_content == expected_content, "The generated _output.xml does not match _expected_output.xml"

def test_get_para_by_tag():    
    result=get_para_by_tag('tests/input.xml','root.content.para.tag4')
    assert result == 'qaz', "root.content.para.tag4 element not found"
    result=get_para_by_tag('tests/input.xml','root.content.tag5')
    assert result == 'Semicolon, inside', "root.content.tag5 element not found"
    result=get_para_by_tag('tests/input.xml','root.content.para')
    assert result == ['<para><tag1></tag1>qwerty</para>', '<para><tag4>qaz</tag4>asdfgh</para>']
    result=get_para_by_tag('tests/input.xml','root.content.sect')
    assert result == ['<sect><tag3>Original content 3</tag3></sect>', '<sect><tag5>Semicolon, inside</tag5></sect>']
