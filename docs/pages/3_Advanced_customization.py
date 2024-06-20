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
    st.markdown("## Advanced customization")
    st.markdown("In the previous section, there is an issue with the appearance of the info and menu bar examples. The top two corners of the editor component are rounded which does not allow for a seemless connection of the left and right edges with the edges of the info/menu bar. On top of this, you might want the bars to appear on the bottom or even on the sides of the editor instead of on top. This is where `css` and `style` attributes really come in to play. ")
    st.markdown("To get a better understanding of how to use these attributes, we need to go over the layout of the Code Editor component.")
    st.markdown("### Code Editor component layout")
    st.image("./pages/resources/code_editor_layout.png")
    st.markdown('On the left (in the diagram) is the layout of the Code Editor component in the HTML/DOM. As you can see, it is relatively flat. On the right is the physical layout of the Code Editor component in the Streamlit app. Here, there are somethings to note. By default, the Code Editor component has its CSS `display` property set to "flex" and its `flex-direction` property set to "column". This means that Code Editor will stack its inner components on top of one another in a column. Additionally, the Ace Editor component has its CSS `order` property set to "3". Altogether, this provides a default setup that allows for easy rearrangment of the stacking order of the components inside the Code Editor. For example, setting the `order` property of the info bar component to a value less than 3 will put it above the Ace Editor like in the examples in the previous section. Setting it to 3 or greater will put the info bar below.')
    st.markdown('''Custom buttons are not positioned like the Ace Editor, info bar, and menu bar components are. By default, they have their CSS `position` property set to "absolute" which makes it easier to position them anywhere within the iframe/document that contains the Code Editor component. ''')

    st.markdown("### Customizing the Ace Editor")
    st.markdown("The Ace Editor inside of Code Editor is highly configurable. There are so many configuration options in fact, that the decision was made to split them up into three groups: general properties, editor properties, editor options.")
    st.markdown("- Set general properties by passing a dictionary to the `props` argument of the `code_editor` function. You can find the list of the properties in this group [here](https://github.com/securingsincity/react-ace/blob/master/docs/Ace.md).")
    st.markdown("- Set editor properties by passing a dictionary to the `editor_props` argument of the `code_editor` function. You can find a list of the properties in this group [here](https://github.com/securingsincity/react-ace/blob/master/src/types.ts)")
    st.markdown("- Set editor options by passing a dictionary to the `options` argument of the `code_editor` function. You can find a list of the properties in this group [here](https://github.com/ajaxorg/ace/wiki/Configuring-Ace#editor-options)")
    st.info("**Note:** The general props group actually contains the other two groups as subgroups. The decision to use three different arguments (of `code_editor` function) is to allow you to set properties in each of the groups separately to simplify things, but you can just set everything via the `props` argument if you desire.")
    st.warning("**Warning:** Currently, Code Editor allows access to pretty much all of the Ace Editor's configuration options including the callback functions which can allow you to pass in code that will be executed on the frontend. **_This is not secure!!_** Some of these options might be removed in the future.")

    st.markdown("### Style and CSS")
    st.markdown("""Code Editor and the components inside (Ace Editor, Info/Menu bars, and buttons) all have a way to set their `style` property. With the exception of Ace Editor and outer containers (like Code Editor), this is done via the `style` attribute of the corresponding dictionary. For example, the `style` attribute of the info bar dictionary is used to set the `style` property of the info bar component. In contrast, Ace Editor's `style` property is set via the `style` attribute in the dictionary you give to the `props` argument of the `code_editor` function. The style attribute corresponding to the Code Editor (outermost container labeled "Code Editor" in the diagram) should be in the dictionary you give to the function's `component_props` argument/parameter""")

    code_setting_style = """# style dict for Ace Editor
ace_style = {"borderRadius": "0px 0px 8px 8px"}

# style dict for Code Editor
code_style = {"width": "100%"}

# set style of info bar dict from previous example
info_bar["style"] = {**info_bar["style"], "order": "1", "height": "2.0rem", "padding": "0rem 0.6rem", "padding-bottom": "0.2rem"}
response_dict = code_editor(your_code_string, height=20, info=info_bar, props={"style": ace_style}, component_props={"style": code_style})
"""
    info_bar["style"] = {**info_bar["style"], "order": "1", "height": "2.0rem", "padding": "0rem 0.6rem", "padding-bottom": "0.2rem"}
    response_info_ex_fixed = code_editor(code_setting_style, height=20, info=info_bar, props={"style": {"borderRadius": "0px 0px 8px 8px"}})
    st.markdown("What if you want to not only style the component but also the elements inside of it? This is where `css` attributes come into the picture. You can pass in CSS to be applied to the component and its children. The way this CSS string is added to the already existing CSS is by prepending the automatically generated class name (given to the component) to the selectors of all rule sets in the string and any property-value pairs that are not in a rule set are added to a general rule set with the generated class name as the selector. In the following example, a CSS string is passed to Code Editor's `css` property: ")
    code_setting_css = """# CSS string for Code Editor
css_string = '''
font-weight: 600;
&.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
&.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}
'''

# same as previous example but with CSS string
response_dict = code_editor(your_code_string, height=20, info=info_bar, props={"style": ace_style}, component_props={"style": code_style, "css": css_string})
"""
    css_string = '''
font-weight: 600;
&.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
&.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}
'''
    response_info_ex_fixed = code_editor(code_setting_css, height=20, info=info_bar, props={"style": {"borderRadius": "0px 0px 8px 8px"}}, component_props={"css": css_string})

    st.markdown("Passing in the `css_string` results in the following CSS:")

    css_result = """
.jBzdJR {
    font-weight: 500;
}
.jBzdJR.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
.jBzdJR.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}
"""
    st.code(css_result, language="css")
    st.markdown('''"jBzdJR" is one of the generated class names given to the outermost Code Editor component HTML element.''')
    st.info("**Note:** The ampersand ('&') in the CSS string is replaced with a class name that is generated when the component is first constructed. If a selector doesnt contain an ampersand, the generated class name is prepended and separated by a space. This means that you cannot select an element outside of the component. ")
    st.success("**Tip:** You can use the ampersand to make the css selector more specific which allows you to override existing CSS rules pertaining to the element you want to style. Take a look at the `css_string` in info bar example from the previous section for examples of how this is done.")
    st.markdown("The dictionaries used to add Info/Menu bars also have a `css` attribute which you can use to style the Info/Menu bar components and their children. ")
    st.info("**Note:** Since the Info/Menu bars and Custom buttons are inside (and thus children) of the Code Editor component, you can style all of them via Code Editor's `css` property. Reasons you might opt for using the `css` attribute of the Info/Menu bar dictionaries instead include better organization and improving integration with other Code Editors (reusability). Each of these dictionaries should have everything needed to fully setup a component.")

    st.markdown("#### Adding classes")
    st.markdown("You can add a class to a component you are adding using the `class` attribute of the dictionary you pass in to the `code_editor` function. This can make it easier to target a component and its children using CSS.")
    st.markdown("Furthermore, component dictionaries that have a `classToggle` attribute allow you to choose a class that you can toggle on the component via commands.")

    st.markdown("#### Global styles")
    st.markdown("What if you want to style the `body` element, the `html` document, or anything outside of the `CodeEditor` component? This can be done by adding global styles. You can add global styles by passing in a CSS string to the `globalCSS` attribute of the `component_props` dictionary.")
    st.success("**Tip:** You can change global CSS variables via the `globalCSS` attribute. This can be an easier and more efficient way to customize the two built-in themes ('streamlit-dark' and 'streamlit-light') which rely on several CSS variables. ")
    st.markdown("Unlike CSS you might add using `st.markdown`, the `globalCSS` attribute allows you to customize the styling of a specific Code Editor component without affecting other instances in the streamlit app.")

    st.markdown("#### Demo")
    code_styles_comp_demo = """# Load custom buttons from file
with open('example_custom_buttons_bar_adj.json') as json_button_file:
    custom_buttons = json.load(json_button_file)
# Load Info Bar from file
with open('example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)
# Load Code Editor CSS from file
with open('code_editor.scss') as css_file:
    css_text = css_file.read()
# construct component props dictionary (->Code Editor)
comp_props = {"css": css_text, "globalCSS": ":root {--streamlit-dark-background-color: #111827;}"}
# construct props dictionary (->Ace Editor)
ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
# add code editor component
response_dict = code_editor(your_code_string,  height = [19, 22], theme="contrast", buttons=custom_buttons, info=info_bar, component_props=comp_props, props=ace_props) 
# handle response to the Run button being clicked (command: submit)
if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.write("Response type: ", response_dict['type'])
    st.code(response_dict['text'], language=response_dict['lang'])
"""
    # construct component props dictionary (->Code Editor)
    comp_props = {"css": css_text, "globalCSS": ":root {--streamlit-dark-background-color: #111827;}"}

    # construct props dictionary (->Ace Editor)
    ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
    response_dict = code_editor(code_styles_comp_demo,  height = [19, 22], theme="contrast", buttons=custom_buttons_alt, info=info_bar, component_props=comp_props, props=ace_props)

    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        st.write("Response type: ", response_dict['type'])
        st.code(response_dict['text'], language=response_dict['lang'])

floating_side_bar = '''
<div class="floating-side-bar">
    <span class="flt-bar-hd"> CONTENTS </span>
    <a href="#advanced-customization">Advanced customization</a>
    <a class="l2" href="#code-editor-component-layout">Code Editor component layout</a>
    <a class="l2" href="#customizing-the-ace-editor">Customizing the Ace Editor</a>
    <a class="l2" href="#style-and-css">Style and CSS</a>
    <a class="l3" href="#adding-classes">Adding classes</a>
    <a class="l3" href="#global-styles">Global styles</a>
    <a class="l3" href="#demo">Demo</a>
    <span class="flt-bar-hd"> LINKS </span>
    <a href="https://github.com/securingsincity/react-ace/blob/master/docs/Ace.md">general properties</a>
    <a href="https://github.com/securingsincity/react-ace/blob/master/src/types.ts">editor properties</a>
    <a href="https://github.com/ajaxorg/ace/wiki/Configuring-Ace#editor-options">editor options</a>
</div>
'''

with col2:
    st.markdown(floating_side_bar, unsafe_allow_html=True)

st.markdown("### Custom completions")
st.markdown("If you want to turn off the autocompletion feature of the Ace Editor, you can do so by setting the `enableBasicAutocompletion`, `enableLiveAutocompletion`, and `enableSnippets` properties to `False` in the `props` dictionary. A simple example is shown below:")
st.code("""response_dict = code_editor(your_code_string, props={ "enableBasicAutocompletion": False, "enableLiveAutocompletion": False, "enableSnippets": False})""", language="python")
st.markdown("In some cases, you might want to provide your own completions for the Ace Editor. This can be done by passing in an array of completions to the `completions` argument of the `code_editor` function. Each completion in the array should be a dictionary with the following properties:")
st.code("""{
  "caption": "[trigger/label]",
  "value": "[code to insert]",
  "meta": "[type/scope]",
  "name": "[name]",
  "score": 400
}""", language="python")
st.markdown("The `caption` property is the text that will be displayed in the completion list. The `value` property is the code that will be inserted into the editor when the completion is selected. The `meta` property is the type or scope of the completion that appears next to the caption. The `name` property is the name of the completion. The `score` property is a number that orders different completions with the same caption. The following example shows how to add a completion to the Ace Editor:")
st.code("""response_dict = code_editor(code, lang=language, completions=[{"caption": "AAA", "value": "BBB", "meta": "CCC", "name": "DDD", "score": 400}], allow_reset=True)""", language="python")
st.markdown("In the example above, a single completion is added to the pre-existing default completions. The new completion will be displayed as 'AAA' in the completion list. When selected, the code 'BBB' will be inserted into the editor. The completion will have a type of 'CCC' and a name of 'DDD'.")
st.image("./pages/resources/completion.png")
st.markdown("To remove/replace the pre-existing completions loaded by default, you can set the `replace_completer` argument to `True` in the `code_editor` function. This will remove the default completions and only use the completions you provide.")
st.code("""response_dict = code_editor(your_code_string, completions=[{"caption": "AAA", "value": "BBB", "meta": "CCC", "name": "DDD", "score": 400}], replace_completer=True)""", language="python")