from code_editor import code_editor
import streamlit as st

class editor_output_parser:
    def __init__(self):
        self.last_id=None

    def __call__(self,output):
        content=output["text"]
        if 'id' in output and not output['id']==self.last_id:
            self.last_id=output['id']
            if not output["type"]=='':
                event=output["type"]
            else:
                event=None
        else:
            event=None
        return event,content


def editor(*args,**kwargs):

    buttons=[
        {
            "name": "Run",
            "feather": "Play",
            "primary": True,
            "hasText": False,
            "alwaysOn":True,
            "showWithIcon": True,
            "commands": [
                ["response","run"]
            ],
            "style": {
            "bottom": "0.44rem",
            "right": "0.4rem"
            }
        }
    ]


    params=dict(
        theme='default',
        buttons=buttons,
        options={
            "showLineNumbers":True
        },
        props={ 
            "enableBasicAutocompletion": False, 
            "enableLiveAutocompletion": False, 
            "enableSnippets": False
        }
    )

    params.update(**kwargs)

    output=code_editor(*args,**params)
    return output


response = editor("def add(a,b):\n    return a+b",allow_reset=True,height="500px")
st.write(response)