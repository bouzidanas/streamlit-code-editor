import json
import streamlit as st
from code_editor import code_editor

# code editor config variables
height = [19, 22]
language="python"
theme="default"
shortcuts="vscode"
focus=False
wrap=True
editor_btns = [{
    "name": "Run",
    "feather": "Play",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    #"commands": html,
    "style": {"bottom": "0.44rem", "right": "0.4rem"}
  }]
code = '''# This is some sample code
a=2
if a > 1:
    print("The value is greater than 2")
'''

# code editor
response_dict = code_editor(code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap})

# show response dict
#if len(response_dict['id']) != 0 and ( response_dict['type'] == "selection" or response_dict['type'] == "submit" ):
    #st.write(response_dict)


html = f"""
    <html>
      <head>
        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
        <script defer src="https://pyscript.net/latest/pyscript.js"></script>
      </head>
      <body>
        <py-script>{code}</py-script>
      </body>
    </html>
    """

st.components.v1.html(html, height=365, scrolling=True)  # 365 ideal height
