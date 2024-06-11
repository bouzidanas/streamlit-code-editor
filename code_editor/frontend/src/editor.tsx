import { useEffect, useRef} from "react"
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
    ghostText: string,
    commands: object[],
    completions: object[],
    keybindingString: string,
    replaceCompleter: boolean,
    onChange: (value: string, event?: any) => void,
    onSelectionChange: (value: any, event?: any) => void,
    onBlur: (event: any, editor?: any) => void,
    onInput: ((event?: any) => void)
  }
  
export const Editor = ({ lang, theme, shortcuts, props, snippetString, commands, completions, ghostText, keybindingString, editorRef, code, replaceCompleter, onChange, onSelectionChange, onBlur, onInput }: EditorProps ) => {
  
  const preventGhostText = useRef<boolean>(false);

  preventGhostText.current = false;

  let commandsList = useRef<object[]>(commands);
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
                commandsList.current= [...commandsList.current, newCommand];
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

      // Add completions
      if (completions.length > 0) {
        const customCompleter = {
          getCompletions: (
              editor: ace.Ace.Editor,
              session: ace.Ace.EditSession,
              pos: ace.Ace.Point,
              prefix: string,
              callback: ace.Ace.CompleterCallback
          ): void => {
              callback(
                  null,
                  (completions as ace.Ace.Completion[])
              );
            },
          };
        if(replaceCompleter) {
          editorRef.current.editor.completers.pop();
        }
        ace.require("ace/ext/language_tools").addCompleter(customCompleter);
      }
    }
  }, [snippetString, keybindingString]);

  useEffect(() => {
    if(editorRef.current){
      console.log("cursor @ useEffect", editorRef.current.editor.getCursorPosition())
      if (ghostText === "") {
        // editorRef.current.editor.removeGhostText();
      }
      else if (!preventGhostText.current) {
        // editorRef.current.editor.setGhostText(ghostText, undefined);
        // Can also use editorRef.current.editor.addGhostText();
        // However, adding ghost text directly using the editor skips important 
        // checks for config flags that could disable ghost text.
        const aceInline = ace.require("ace/autocomplete/inline").AceInline;
        const inline = new aceInline();
        const testCompletion: ace.Ace.Completion = {
          snippet: ghostText,
        }
        const result = inline.show(editorRef.current.editor, testCompletion, "");
        !result && inline.hide() && console.log("failed to show ghost text");
      }
    }
  }, [ghostText, editorRef]);

  return (
          <AceEditor
           ref={editorRef}
           name="REACT_ACE_EDITOR"
           mode={lang}
           theme={theme}
           value={code}
           keyboardHandler={shortcuts}
           commands={commandsList.current}
           onChange={onChange}
           onSelectionChange={onSelectionChange}
           onBlur={onBlur}
           onCursorChange={(value, event) => {
              
           }}
           onInput={onInput}
           {...props}/>
  );
};