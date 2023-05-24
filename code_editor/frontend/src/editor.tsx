import { useEffect} from "react"
import AceEditor from "react-ace";
import ace from "ace-builds";

import "ace-builds/webpack-resolver";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/src-noconflict/ext-searchbox";
import "ace-builds/src-noconflict/ext-prompt";
import "ace-builds/src-noconflict/ext-modelist";
import "ace-builds/src-noconflict/ext-keybinding_menu";

export interface KeyBinding {
    bindkey: string | object,
    name: string
}

export interface EditorKeyBindings {
  commands?: KeyBinding[],
  completer?: KeyBinding[]
}

export type EditorProps = {
    code: string,
    lang: string,
    theme: string,
    shortcuts: string,
    props: any,
    editorRef: any,
    snippetString: string,
    commands: object[],
    keybindingString: string,
    onChange: (value: string, event?: any) => void 
  }
  
export const Editor = ({ lang, theme, shortcuts, props, snippetString, commands, keybindingString, editorRef, code, onChange }: EditorProps ) => {
    
  useEffect(() => {
    if(editorRef.current){

      // Add/remove keybindings
      ace.require('ace/autocomplete').Autocomplete.for(editorRef.current.editor);
      const keybindings = JSON.parse(keybindingString) as EditorKeyBindings;
      if(keybindings.commands && keybindings.commands.length > 0){
        // const bindkeySelector = editorRef.current.editor.commands.platform as string;
        keybindings.commands.forEach((binding) => {
            if(binding.name && typeof binding.name === "string"){
              if (JSON.stringify(editorRef.current.editor.commands.commands[binding.name].bindKey ?? "") !== JSON.stringify(binding.bindkey)) {
                const newCommand = {...editorRef.current.editor.commands.commands[binding.name]};
                newCommand.bindKey = binding.bindkey;
                editorRef.current.editor.commands.addCommand(newCommand);
                commands= [...commands, newCommand];
              }
            }
   
        });
      }
      if(keybindings.completer && keybindings.completer.length > 0){
        // const bindkeySelector = editorRef.current.editor.completer.keyboardHandler.platform as string;
        keybindings.completer.forEach((binding) => {
            if(binding.name && typeof binding.name === "string"){
              if (JSON.stringify(editorRef.current.editor.completer.keyboardHandler.commands[binding.name].bindKey ?? "") !== JSON.stringify(binding.bindkey)) {
                const newCommand = {...editorRef.current.editor.completer.keyboardHandler.commands[binding.name]};
                newCommand.bindKey = binding.bindkey;
                editorRef.current.editor.completer.keyboardHandler.addCommand(newCommand);
              }
            }
        });
      }

      // Add/remove snippets
      ace.require("ace/ext/keybinding_menu").init(editorRef.current.editor);
      const snippetManager = ace.require('ace/snippets').snippetManager;
      const snippets = JSON.parse(snippetString) as object;
      for (const [snippetsLang, snippetsAddRemove] of Object.entries(snippets)){
        if(snippetsAddRemove[0])
          snippetManager.register(snippetManager.parseSnippetFile(snippetsAddRemove[0], snippetsLang), snippetsLang)
        
        if(snippetsAddRemove[1])
          snippetManager.unregister(snippetManager.parseSnippetFile(snippetsAddRemove[1], snippetsLang), snippetsLang)
      }
    }
  }, [snippetString, keybindingString]);

  return (
          <AceEditor
           ref={editorRef}
           name="REACT_ACE_EDITOR"
           mode={lang}
           theme={theme}
           value={code}
           keyboardHandler={shortcuts}
           commands={commands}
           onChange={onChange}
           {...props}/>
  );
};