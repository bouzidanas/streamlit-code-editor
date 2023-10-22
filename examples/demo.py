import json
import streamlit as st
from code_editor import code_editor

with open('streamlit-code-editor/examples/resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

# Load Info bar CSS from JSON file
with open('streamlit-code-editor/examples/resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('streamlit-code-editor/examples/resources/example_code_editor_css.scss') as css_file:
    css_text = css_file.read()

with open('streamlit-code-editor/examples/resources/example_python_code.py') as python_file:
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
response_dict = code_editor(demo_sample_python_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": wrap})

if response_dict['type'] == "submit" and len(response_dict['id']) != 0:
    st.write(response_dict)

# st.write("You can find more examples in the [docs]()")
