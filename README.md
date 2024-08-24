# reportlab
pdf generator related

## Prompts

- Add python function `replace_fstr(input_file, output_file, vars)` to `xmltags.py` which will read file 
`input_file` and replace curly braces and text within curly braces with value of variable with the name of text withing curly braces. All variables are included in dictionary `vars`. The result should be written to file `output_file` with the same extension as `input_file`. Add function `test_replace_fstr()` to test_xml.py which will assert if file `tests\input_fstr.xml` is equal to file `tests\expected_fstr.xml`
###
vars = {
        'var2': 'new var2 ',
        # 'var3': 'new var3',
        'var4': 'new var4',
    }