import json
import streamlit as st
import requests
from code_editor import code_editor
import time
from openai import OpenAI

client = OpenAI(api_key="/", base_url="/")
formatted_code_text = ""





# code editor config variables
height = [19, 22]
#language = "python"
syntax_mapping = {
    'Ada': 'ada',
    'Assembler - GCC': 'assembly_x86',
    'Assembler - NASM': 'assembly_x86',
    'AWK': 'awk',
    'Bash Shell': 'sh',
    'BC': 'bc',
    'Befunge': 'befunge',
    'C': 'c_cpp',
    'C#': 'csharp',
    'C++': 'c_cpp',
    'COBOL': 'cobol',
    'Clojure': 'clojure',
    'CoffeeScript': 'coffee',
    'D': 'd',
    'Dart': 'dart',
    'Elixir': 'elixir',
    'Erlang': 'erlang',
    'Factor': 'factor',
    'F#': 'fsharp',
    'Falcon': 'falcon',
    'FASM': 'assembly_x86',
    'FORTRAN': 'fortran',
    'FREE BASIC': 'basic',
    'GO Lang': 'golang',
    'Groovy': 'groovy',
    'Haskell': 'haskell',
    'Hack': 'hack',
    'Icon': 'icon',
    'Intercal': 'intercal',
    'J Language': 'j',
    'Java': 'java',
    'Kotlin': 'kotlin',
    'LOLCODE': 'lolcode',
    'Lua': 'lua',
    'Nemerle': 'nemerle',
    'NodeJS': 'javascript',
    'Octave': 'matlab',
    'Objective C': 'objectivec',
    'Ocaml': 'ocaml',
    'OZ Mozart': 'mozart',
    'Pascal': 'pascal',
    'Perl': 'perl',
    'Picolisp': 'picolisp',
    'PHP': 'php',
    'Pike': 'pike',
    'Prolog': 'prolog',
    'Python': 'python',
    'R': 'r',
    'Racket': 'racket',
    'Rhino JS': 'javascript',
    'RUST': 'rust',
    'Ruby': 'ruby',
    'Scheme': 'scheme',
    'Scala': 'scala',
    'SmallTalk': 'smalltalk',
    'SpiderMonkey': 'javascript',
    'Swift': 'swift',
    'TCL': 'tcl',
    'Unlambda': 'unlambda',
    'VB.Net': 'vb',
    'VERILOG': 'verilog',
    'Whitespace': 'whitespace',
    'YaBasic': 'basic',
}

language_options = ['Ada',
                    'Assembler - GCC',
                    'Assembler - NASM',
                    'AWK',
                    'Bash Shell',
                    'BC',
                    'Befunge',
                    'C',
                    'C#',
                    'C++',
                    'COBOL',
                    'Clojure',
                    'CoffeeScript',
                    'D',
                    'Dart',
                    'Elixir',
                    'Erlang',
                    'Factor',
                    'F#',
                    'Falcon',
                    'FASM',
                    'FORTRAN',
                    'FREE BASIC',
                    'GO Lang',
                    'Groovy',
                    'Haskell',
                    'Hack',
                    'Icon',
                    'Intercal',
                    'J Language',
                    'Java',
                    'Kotlin',
                    'LOLCODE',
                    'Lua',
                    'Nemerle',
                    'NodeJS',
                    'Octave',
                    'Objective C',
                    'Ocaml',
                    'OZ Mozart',
                    'Pascal',
                    'Perl',
                    'Picolisp',
                    'PHP',
                    'Pike',
                    'Prolog',
                    'Python',
                    'R',
                    'Racket',
                    'Rhino JS',
                    'RUST',
                    'Ruby',
                    'Scheme',
                    'Scala',
                    'SmallTalk',
                    'SpiderMonkey',
                    'Swift',
                    'TCL',
                    'Unlambda',
                    'VB.Net',
                    'VERILOG',
                    'Whitespace',
                    'YaBasic']

language_mapping = {
    'Ada': 'ada',
    'Assembler - GCC': 'gccasm',
    'Assembler - NASM': 'nasm',
    'AWK': 'awk',
    'Bash Shell': 'bash',
    'BC': 'bc',
    'Befunge': 'befunge',
    'C': 'c',
    'C#': 'csharp',
    'C++': 'cpp17',
    'Clojure': 'clojure',
    'CoffeeScript': 'coffeescript',
    'COBOL': 'cobol',
    'D': 'd',
    'Dart': 'dart',
    'Elixir': 'elixir',
    'Erlang': 'erlang',
    'Factor': 'factor',
    'F#': 'fsharp',
    'Falcon': 'falcon',
    'FASM': 'fasm',
    'FORTRAN': 'fortran',
    'FREE BASIC': 'freebasic',
    'GO Lang': 'go',
    'Groovy': 'groovy',
    'Hack': 'hack',
    'Haskell': 'haskell',
    'Icon': 'icon',
    'Intercal': 'intercal',
    'J Language': 'jlang',
    'Java': 'java',
    'Kotlin': 'kotlin',
    'LOLCODE': 'lolcode',
    'Lua': 'lua',
    'Nemerle': 'nemerle',
    'NodeJS': 'nodejs',
    'Objective C': 'objc',
    'Octave': 'octave',
    'Ocaml': 'ocaml',
    'OZ Mozart': 'mozart',
    'Pascal': 'pascal',
    'Perl': 'perl',
    'Picolisp': 'picolisp',
    'PHP': 'php',
    'Pike': 'pike',
    'Prolog': 'prolog',
    'Python': 'python3',
    'R': 'r',
    'Racket': 'racket',
    'Rhino JS': 'rhino',
    'RUST': 'rust',
    'Ruby': 'ruby',
    'Scheme': 'scheme',
    'Scala': 'scala',
    'SmallTalk': 'smalltalk',
    'SpiderMonkey': 'spidermonkey',
    'Swift': 'swift',
    'TCL': 'tcl',
    'Unlambda': 'unlambda',
    'VB.Net': 'vbn',
    'VERILOG': 'verilog',
    'Whitespace': 'whitespace',
    'YaBasic': 'yabasic',
}


language = st.selectbox('Select a language', language_options)

theme = "default"
shortcuts = "vscode"
focus = False
wrap = True
editor_btns = [
    {
    "name": "Run",
    "feather": "Play",
    "primary": True,
    "hasText": True,
    "alwaysOn": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0.44rem", "right": "0.4rem"}
    },
    {
    "name": "Copy",
    "feather": "Copy",
    "primary": True,
    "hasText": False,
    "alwaysOn": True,
    "showWithIcon": True,
    "commands": ["copyAll"],
    "style": {"top": "0.46rem", "right": "0.4rem"}
    },
    {
    "name": "Debug",
    "feather": "StopCircle",
    "primary": True,
    "hasText": True,
    "alwaysOn": True,
    "showWithIcon": True,
    "commands": [["response","debug"]],
    "style": {"bottom": "3.5rem", "right": "0.4rem"}
    }
]





sample_python_code = '''# This is some sample code
a=2
if a > 1:
    print("The value is greater than 1")
'''

# code editor
response_dict = code_editor(sample_python_code, height=height, lang=syntax_mapping[language], theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": True, "showLineNumbers": True})
#st.subheader("Input")
#input_data = st.text_area('Enter input data here', height=100)

if len(response_dict['id']) != 0 and (response_dict['type'] == "selection" or response_dict['type'] == "submit"):
    # Capture the text part
    st.write(response_dict)
    code = response_dict["text"]
    code_text = f'Code "{response_dict["text"]}" and Programming Language "{response_dict["lang"]} make sure that the code matches the chosen programming language otherwise say so, then provide a detailed analysis of the code. Then suggest further improvements"'
    formatted_code_text = f'```\n{code_text}\n```'
    st.write(response_dict)


    # Apply button to run the code
    payload = {
        'clientId': '/',
        'clientSecret': '/',
        'script': code,  # Use the current value from the editor widget
        'language': language_mapping[language],
        'versionIndex': '0',
        #'stdin': input_data
    }

    # Show a loading spinner while the code is being executed
    with st.spinner('Executing code...'):
        try:
            response = requests.post('https://api.jdoodle.com/v1/execute', json=payload)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.exceptions.RequestException as err:
            st.error(f"Something went wrong: {err}")
        else:
            result = response.json()

            # Display output
            if 'output' in result:
                st.subheader("Output")
                st.code(result['output'], language="plaintext")
            else:
                st.error('The API response does not contain an output key.')


    message = [{"role": "user", "content": code_text}]
    response = client.chat.completions.create(
        model="/",
        messages=message
    )
    im_code = response.choices[0].message.content

    # Display the improved/debugged code gradually
    with st.chat_message("assistant"):
        placeholder = st.empty()
        growing_text = ""
        for char in im_code:
            growing_text += char
            placeholder.markdown(growing_text)
            time.sleep(0.015)  # Adjust the sleep time to control the speed of typing

        # Add model's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": im_code})

if len(response_dict['id']) != 0 and response_dict["type"] == "debug":
    st.write(response_dict)