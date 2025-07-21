import json
import streamlit as st
from code_editor import code_editor

html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

# Opening JSON file
# You can also just use a dictionary but with files (JSON or text for example),
# its easier to transfer or use in multiple projects
with open('./pages/resources/example_custom_buttons_bar_adj.json') as json_button_file:
    custom_buttons_alt = json.load(json_button_file)

with open('./pages/resources/example_custom_buttons_set.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

# Load Info bar CSS from JSON file
with open('./pages/resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('./pages/resources/code_editor.scss') as css_file:
    css_text = css_file.read()

col1, col2 = st.columns([6,2])
with col1:
    st.markdown("## Getting Started")
    st.markdown("### Installation")
    st.markdown("Install [streamlit-code-editor](https://pypi.org/project/streamlit-code-editor/) with pip:")
    st.code("python -m pip install streamlit_code_editor")
    st.markdown("replacing `python` with the correct version of python for your setup (e.g. `python3` or `python3.8`). Or if you are certain the correct version of python will be used to run pip, you can install with just:")
    st.code("pip install streamlit_code_editor")
    st.markdown("Alternatively, you can download the source from the [download page](https://pypi.org/project/streamlit-code-editor/#files) or the [GitHub repository](https://github.com/bouzidanas/streamlit.io/tree/master/streamlit-code-editor) and after unzipping, install with:")
    st.code("python setup.py install")
    st.markdown("(for the above command to work, make sure you are in the same directory as 'setup.py' in the unzipped folder).")
    st.markdown("### Adding a Code Editor")
    st.markdown("After importing the module, you can call the `code_editor` function with just a string:")


    minimal_code = '''# All you need to add a code editor to your Streamlit app is an\n# import and a string containing your code.
from code_editor import code_editor

response_dict = code_editor(your_code_string)'''

    response_start = code_editor(minimal_code)

    st.markdown("Without specifying a language, the editor will default to `python`. You can also specify a language with the `lang` argument:")

    minimal_code_with_lang = '''# The default value for the lang argument is "python"\nresponse_dict = code_editor(your_code_string, lang="python")'''

    response_start_with_lang = code_editor(minimal_code_with_lang)

    st.markdown("The two blocks of code above are displayed in code editors. As the name of the component implies, you can edit the code. Try it out! ")
    st.markdown("By default, each code editor is styled like streamlit's code component. We will go over how to customize the styling in a later section.")

floating_side_bar = '''
<div class="floating-side-bar">
    <span class="flt-bar-hd"> CONTENTS </span>
    <a href="#getting-started">Getting started</a>
    <a class="l2" href="#installation">Installation</a>
    <a href="#adding-a-code-editor">Adding a Code Editor</a>
    <span class="flt-bar-hd"> LINKS </span>
    <a href="https://pypi.org/project/streamlit-code-editor/">streamlit-code-editor</a>
    <a href="https://pypi.org/project/streamlit-code-editor/#files">download page</a>
    <a href="https://github.com/bouzidanas/streamlit.io/tree/master/streamlit-code-editor">GitHub repository</a>
</div>
'''

with col2:
    st.markdown(floating_side_bar, unsafe_allow_html=True)