from  xmltags import replace_xml_content, get_para_by_tag
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
        'tag1': None,
        'tag2': 'new tag2 <tag>qwerty qaz<tag/>',
        'tag4': 'new tag4',
    }

    replace_xml_content('tests/input.xml', 'tests/_output.xml', tags1)
    
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
