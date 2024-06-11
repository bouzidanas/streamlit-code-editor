import os
import json
import streamlit as st
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
def code_editor(code, lang='python', theme="default", shortcuts="vscode", height=30, focus=False, allow_reset=False, replace_completer=False, response_mode="default", ghost_text="", snippets=["", ""], completions=[], keybindings={}, buttons=[], menu={}, info={}, options={}, props={}, editor_props={}, component_props={}, key=None):
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
    component_value = _component_func(code=code, lang=lang, theme=theme, key=key, height=height, focus=focus, shortcuts=shortcuts, snippets=snippets, completions=completions, keybindings=keybindings, buttons=buttons, options=options, props=props, editor_props=editor_props, component_props=component_props, menu=menu, info=info, allow_reset=allow_reset, replace_completer=replace_completer, response_mode=response_mode, ghost_text=ghost_text, default={"id": "", "type": "", "lang": "", "text": "", "selected": "", "cursor": ""})

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run code_editor/__init__.py`
if not _RELEASE:

    with open('../examples/resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    # Load Info bar CSS from JSON file
    with open('../examples/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    # Load Code Editor CSS from file
    with open('../examples/resources/example_code_editor_css.scss') as css_file:
        css_text = css_file.read()

    with open('../examples/resources/example_python_code.py') as python_file:
        demo_sample_python_code = python_file.read()

    # construct component props dictionary (->Code Editor)
    comp_props = {"css": css_text, "globalCSS": ":root {\n  --streamlit-dark-font-family: monospace;\n}"}

    mode_list = ["abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "bibtex", "c9search", "c_cpp", "cirru", "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", "io", "ion", "jack", "jade", "java", "javascript", "jexl", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", "kotlin", "latex", "latte", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mips", "mixal", "mushcode", "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "partiql", "pascal", "perl", "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", "properties", "protobuf", "puppet", "python", "qml", "r", "raku", "razor", "rdoc", "red", "redshift", "rhtml", "robot", "rst", "ruby", "rust", "sac", "sass", "scad", "scala", "scheme", "scrypt", "scss", "sh", "sjs", "slim", "smarty", "smithy", "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml", "zeek"]

    btn_settings_editor_btns = [{
        "name": "copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll"],
        "style": {"top": "0rem", "right": "0.4rem"}
      },{
        "name": "update",
        "feather": "RefreshCw",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0rem", "right": "0.4rem"}
      }]

    height = [19, 22]
    language="python"
    theme="default"
    shortcuts="vscode"
    focus=False
    wrap=True
    btns = custom_buttons_alt

    st.markdown('<h1><a href="https://github.com/bouzidanas/streamlit.io/tree/master/streamlit-code-editor">Streamlit Code Editor</a> Demo</h1>', unsafe_allow_html=True)
    st.write("")
    with st.expander("Settings", expanded=True):
        col_a, col_b, col_c, col_cb = st.columns([6,11,3,3])
        col_c.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)
        col_cb.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)

        height_type = col_a.selectbox("height format:", ["css", "max lines", "min-max lines"], index=2)
        if height_type == "css":
            height = col_b.text_input("height (CSS):", "400px")
        elif height_type == "max lines":
            height = col_b.slider("max lines:", 1, 40, 22)
        elif height_type == "min-max lines":
            height = col_b.slider("min-max lines:", 1, 40, (19, 22))

        col_d, col_e, col_f = st.columns([1,1,1])
        language = col_d.selectbox("lang:", mode_list, index=mode_list.index("python"))
        theme = col_e.selectbox("theme:", ["default", "light", "dark", "contrast"])
        shortcuts = col_f.selectbox("shortcuts:", ["emacs", "vim", "vscode", "sublime"], index=2)
        focus = col_c.checkbox("focus", False)
        wrap = col_cb.checkbox("wrap", True)

    with st.expander("Components"):
        c_buttons = st.checkbox("custom buttons (JSON)", False)
        if c_buttons:
            response_dict_btns = code_editor(json.dumps(custom_buttons_alt, indent=2), lang="json", height = 8, buttons=btn_settings_editor_btns)

            if response_dict_btns['type'] == "submit" and len(response_dict_btns['text']) != 0:
                btns = json.loads(response_dict_btns['text'])
        else:
            btns = []

        i_bar = st.checkbox("info bar (JSON)", False)
        if i_bar:
            response_dict_info = code_editor(json.dumps(info_bar, indent=2), lang="json", height = 8, buttons=btn_settings_editor_btns)

            if response_dict_info['type'] == "submit" and len(response_dict_info['text']) != 0:
                info_bar = json.loads(response_dict_info['text'])
        else:
            info_bar = {}

    st.write("### Output:")
    # construct props dictionary (->Ace Editor)
    ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}

    input = st.text_area("Input:", demo_sample_python_code, height=200)
    response_dict = code_editor(input,  height = height, lang=language, theme=theme, shortcuts=shortcuts, completions=[{"caption": "AAA", "value": "BBB", "meta": "CCC", "name": "DDD", "score": 400}], focus=focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": wrap}, allow_reset=True, response_mode=["debounce", "blur"], key="code_editor_demo")

    st.write(response_dict)

    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        st.write("Response type: ", response_dict['type'])
        st.code(response_dict['text'], language=response_dict['lang'])
    st.write("### Code Editor:")
    st.code(input, language=language)
    # st.write("You can find more examples in the [docs]()")

    new_response = code_editor("print('Hello World!')", lang="python", height = 22, buttons=btn_settings_editor_btns, options={"wrap": wrap}, allow_reset=True, key="code_editor3", ghost_text="Type your code here...", response_mode="debounce")
    st.write(new_response)