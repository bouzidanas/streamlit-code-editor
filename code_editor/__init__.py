import os
import json
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("code_editor"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "code_editor",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "code_editor", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def code_editor(code, lang='python', theme="default", shortcuts="vscode", height=30, focus=False, snippets=["", ""], keybindings={}, buttons=[], menu={}, info={}, key=None, options={}, props={}, editor_props={}, component_props={}):
    """Create a new instance of "code_editor".

    Parameters
    ----------
    code: str
        The code that goes in the editor
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        Contains the type of event and the code inside the editor when 
        event occured
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(code=code, lang=lang, theme=theme, key=key, height=height, focus=focus, shortcuts=shortcuts, snippets=snippets, keybindings=keybindings, buttons=buttons, options=options, props=props, editor_props=editor_props, component_props=component_props, menu=menu, info=info, default={"type": "", "text": "", "lang": ""})

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run code_editor/__init__.py`
if not _RELEASE:
    import streamlit as st

    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.

    new_code_input = \
    '''// store input numbers
const num1 = parseInt(prompt('Enter the first number '));
const num2 = parseInt(prompt('Enter the second number '));

//add two numbers
function add(a, b){
    return(num1 + num2);
}

// display the sum
console.log(str(add(num1, num2)));

//We just added two numbers and printed 
//the result to the console'''


    code_input = \
        '''#!/usr/local/bin/python

import string, sys

# If no arguments were given, print a helpful message
if len(sys.argv)==1:
    print 
    sys.exit(0)

# Loop over the arguments
for i in sys.argv[1:]:
    try:
        fahrenheit=float(string.atoi(i))
    except string.atoi_error:
        print repr(i), "not a numeric value"
    else:
        celsius=(fahrenheit-32)*5.0/9.0
        print 'Done' '''


    # Opening JSON file
    with open('./frontend/docs/example_custom_buttons_set.json') as json_button_file:
        customButtons = json.load(json_button_file)

    # Opening JSON file
    with open('./frontend/docs/example_info_bar.json') as json_info_file:
        infoBar = json.load(json_info_file)

    # Opening text file
    with open('./frontend/docs/code_editor.scss') as css_file:
        cssText = css_file.read()

    #comp_props = {"css": cssText, "globalCSS": "body > #root~div.ace-streamlit-dark.ace_editor.ace_autocomplete{\n    background-color: #111827;\n}\nbody > #root~div .ace_prompt_container {\n    background: #111827;\n}"}
    comp_props = {"css": cssText, "globalCSS": ":root {--streamlit-dark-background-color: #111827;}"}


    #st.header("This is a header")
    if 'focus' not in st.session_state:
        st.session_state['focus'] = False

    code_back = code_editor(code_input, lang="python", height=20, focus=st.session_state['focus'], snippets=[[{ "name": 'build', "code": 'console.log("build")' },{ "name": 'destroy', "code": 'console.log("destroy")' }],""], buttons=customButtons["buttons"], info=infoBar,component_props=comp_props, props={"scrollMargin": [31,15,0,0]}, options={"wrap": False}, key="editor2")
    if code_back['type'] == "submit" and len(code_back['text']) != 0:
        st.write("TYPE: ", code_back['type'])
        st.code(code_back['text'], language=code_back['lang'])

    st.text_area("Text area", height=5)