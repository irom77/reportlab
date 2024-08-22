from  xmltags import replace_xml_content, get_para_by_tag
from xml.etree import ElementTree as ET

# input.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <root>
# <content>
#       <para><tag1></tag1>qwerty</para>
#       <para><tag4>qaz</tag4>asdfgh</para>
#       <tag2>Original content 2</tag2>
#       <sect><tag3>Original content 3</tag3></sect>
#       <tag3>Original content 3</tag3>
#       <tag5>Semicolon, inside</tag5>
#       <sect><tag5>Semicolon, inside</tag5></sect>
# </content>    
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
    assert root.find(".//tag2").text == "new tag2 <tag>qwerty qaz<tag/>", "Content of <tag2> does not match"
    assert root.find(".//tag1") is not None, "<tag1> element not found"

def test_get_para_by_tag():    
    result=get_para_by_tag('tests/input.xml','root.content.para.tag4')
    assert result == 'qaz', "root.content.para.tag4 element not found"
    result=get_para_by_tag('tests/input.xml','root.content.tag5')
    assert result == 'Semicolon, inside', "root.content.para.tag5 element not found"
    # result=get_para_by_tag('tests/input.xml','root.content.para')
    # assert result == ['<tag1></tag1>qwerty','<tag4>qaz</tag4>asdfgh']
    result=get_para_by_tag('tests/input.xml','root.content.sect')
    assert result == ['<tag3>Original content 3</tag3>','<tag5>Semicolon, inside</tag5>']
