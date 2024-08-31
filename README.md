# reportlab
pdf generator related

## Prompts

- Add python function `replace_fstr(input_file, output_file, vars)` to `xmltags.py` which will read file 
`input_file` and replace curly braces and text within curly braces with value of variable with the name of text withing curly braces. All variables are included in dictionary `vars`. The result should be written to file `output_file` with the same extension as `input_file`. Add function `test_replace_fstr()` to test_xml.py which will assert if file `tests\input_fstr.xml` is equal to file `tests\expected_fstr.xml`
###
```
vars = {
        'var2': 'new var2 ',
        # 'var3': 'new var3',
        'var4': 'new var4',
    }
```
- Add python function `create_conf(input_file, config_file)` to `xmltags.py` which will read XML  file 
`input_file` and create file `config_file` of type YML. Direct children tags of <root> should be top-level keys in YML file, and text in curly braces should be variables. Add function `test_create_conf()` to test_xml.py which will assert if function `create_conf(input_file, config_file)` passes with file `input_file` of  `tests\config_input.xml` and  file `confif_file`of  `tests\config_expected.yml` as inputs

- Add python function `get_xml_by_tag(file_path, tag)` to `xmltags.py` which will read file_path and provide text of nested tag i.e. input sect.tag5 should return text of <sect><tag5>. Return list in case there are multiple matches for the tag. Function should pass the test `test_get_xml_by_tag` from `test_xml.py`

C:\Users\irekr\AppData\Local\Programs\Tesseract-OCR

    