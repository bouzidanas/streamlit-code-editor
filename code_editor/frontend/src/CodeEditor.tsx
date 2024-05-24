import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
  Theme,
} from "streamlit-component-lib"
import {v1} from 'uuid';
import styled, { createGlobalStyle } from "styled-components/macro"
import { useState, useRef, useEffect, useMemo } from "react"
import AceEditor from "react-ace";
import ace from "ace-builds";
import { Editor } from './editor';
import { Menu as ButtonMenu, Set as ButtonSet, customButton, buttonGroup, Info as InfoBar } from "./button-menu"

import "ace-builds/webpack-resolver";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/src-noconflict/ext-searchbox";
import "ace-builds/src-noconflict/ext-prompt";
import "ace-builds/src-noconflict/ext-modelist";

interface CodeEditorProps extends ComponentProps {
  args: any
  width: number
  disabled: boolean
  theme?: Theme
}

const defaultOptions = {
  fontFamily: '"Source Code Pro", monospace',
  cursorStyle: "smooth",
  displayIndentGuides: false,
  wrap: false,
  highlightActiveLine: true,
  showPrintMargin: false,
  showLineNumbers: false,
  foldStyle: "markbegin",
  autoScrollEditorIntoView: false,
  animatedScroll: true,
  fadeFoldWidgets: true,
}

const defaultEditorProps = {
  editorProps: {
    $blockScrolling: true
  }
}

const defaultProps = {
  cursorStart: 1,
  enableBasicAutocompletion: false,
  enableLiveAutocompletion: true,
  enableSnippets: true,
  focus: false,
  fontSize: 14,
  highlightActiveLine: true,
  navigateToFileEnd: true,
  placeholder: null,
  readOnly: false,
  scrollMargin: [15, 15, 0, 0],
  setOptions: defaultOptions,
  showGutter: true,
  showPrintMargin: false,
  style: {},
  tabSize: 4,
  width: "auto",
  debounceChangePeriod: 250,
}

const GlobalCSS = createGlobalStyle<{isDisabled?: boolean, inject: string}>`
  html {
    opacity: ${props => props.isDisabled? "0.5": "1"};
    cursor: ${props => props.isDisabled? "not-allowed": "auto"};
    pointer-events: ${props => props.isDisabled? "none": "auto"};
  }
  ${props => props.inject}
`
const StyledCodeEditor = styled.div`
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  :hover button {
    opacity: 1;
    transform: scale(1);
  }
  button.always-on {
    opacity: 1;
    transform: scale(1);
    transition: none;
  }
  :hover button svg {
        opacity: 1;
        transform: scale(1);
  }
  :hover button.with-icon span {
    opacity: 1;
    transform: scale(1);
  }
  button.always-on > span {
    opacity: 1;
    transform: scale(1);
    transition: none;
  }
  button.always-on > svg {
    opacity: 1;
    transform: scale(1);
    transition: none;
  }
  `;

const CodeEditor = ({ args, width, disabled, theme }: CodeEditorProps) => {

  //sets code to the initial value every time the component is rendered
  //to set the initial value once, use a function instead of a value.
  const [code, setCode] = useState(args['code']);
  // const [keybindingAddRemove, setKeybindingAddRemove] = useState(["",""]);

  const aceEditor = useRef<AceEditor>(null);
  const infoTextRef = useRef<HTMLSpanElement>(null);
  const baseSession = useRef<ace.Ace.EditSession | null>(null);
  const keepFocus = useRef<boolean>(false);
  const reset = useRef<boolean>(false);

  var timeoutId: NodeJS.Timeout;

  /**
    * This function takes as input either a snippetText string that is expected
    * to be already formatted like the text in a SnippetFile or a dictionary or 
    * and array of dictionaries. For the first case, it just returns the input.
    * For the second and third case, a (SnippetFile format) string is constructed
    * from the dict(s) and returned. Learn more about snippets {@link  here}
    * @param snippetRaw snippets to be converted to a single snippetText string
    * @returns {string} snippetText
    */
  const createSnippets = (snippetRaw: string | object | [object]): string => {
    return (typeof snippetRaw === "string" ? snippetRaw : (Array.isArray(snippetRaw) ? snippetRaw : [snippetRaw]).map(({ name, code }) =>
    ([
      'snippet ' + name,
      code.split('\n')
        .map((c: string) => '\t' + c)
        .join('\n'),
    ].join('\n'))
    ).join('\n'))
  }
  const [snippetAddRemove, setSnippetAddRemove] = useState({[args['lang']] : [createSnippets(args["snippets"][0]), createSnippets(args["snippets"][1])]});
  const [keybindingAddRemove, setKeybindingAddRemove] = useState(args['keybindings']);


  useEffect(() => {
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    }
  }, []);

  useEffect(() => {
    if(aceEditor.current && keepFocus.current){
      aceEditor.current.editor.focus();
      keepFocus.current = false;
    }
  }, [keepFocus.current]);

  // To reasons for the useEffect here: 
  //   1. to set the focus on the editor only when the focus argument has changed to true.
  //   2. to set the focus on the editor after rendering the component at which point, the 
  //      editor should be ready.
  useEffect(() => {
    if(aceEditor.current && args.focus){
      aceEditor.current.editor.focus();
    }
  }, [args.focus]);

  const onChangeHandler = (newCode: string) => {
    setCode(newCode);

    const responseMode = typeof args["response_mode"] === "string" ? [args["response_mode"]] : args["response_mode"];
    if (responseMode.includes("debounce") && aceEditor.current && aceEditor.current.editor) {
      const editor = aceEditor.current.editor as any;
      const outgoingMode = editor.getSession().$modeId.split("/").pop();
      Streamlit.setComponentValue({id: v1().slice(0,8), type: "change", lang: outgoingMode, text: newCode, selected: editor.getSelectedText(), cursor: editor.getCursorPosition()});
    }
  }
  
  const onSelectionChangeHandler = (selectedText: any) => {
    const responseMode = typeof args["response_mode"] === "string" ? [args["response_mode"]] : args["response_mode"];
    if (responseMode.includes("select") && aceEditor.current && aceEditor.current.editor) {
      const editor = aceEditor.current.editor as any;
      const outgoingMode = editor.getSession().$modeId.split("/").pop();
      Streamlit.setComponentValue({id: v1().slice(0,8), type: "selection", lang: outgoingMode, text: code, selected: editor.getSelectedText(), cursor: editor.getCursorPosition()});
    }
  }

  const onEditorBlur = (event: any, editor: any) => {
    const responseMode = typeof args["response_mode"] === "string" ? [args["response_mode"]] : args["response_mode"];
    if (responseMode.includes("blur") && editor) {
      const outgoingMode = editor.getSession().$modeId.split("/").pop();
      setCode(editor.getValue());
      Streamlit.setComponentValue({id: v1().slice(0,8), type: "blur", lang: outgoingMode, text: editor.getValue(), selected: editor.getSelectedText(), cursor: editor.getCursorPosition()});
    }
  }

  // commands is an array of objects containing functions
  // that the editor can be triggered to call.
  const commands = { commands: [
    {
      name: 'submit', //name for the key binding.
      description: "Send 'submit' response", //description of the command
      bindKey: { win: 'Ctrl-Enter', mac: 'Command-Enter' }, //key combination used for the command.
      exec: (editor: any) => {
        const outgoingMode = editor.getSession().$modeId.split("/").pop();
        Streamlit.setComponentValue({id: v1().slice(0,8), type: "submit", lang: outgoingMode, text: editor.getValue(), selected: editor.getSelectedText(), cursor: editor.getCursorPosition()});
      }
    },
    {
      name: 'saveState',
      description: "Save state",
      bindKey: { win: 'Ctrl-Alt-S', mac: 'Command-Alt-S' },
      exec: (editor: ace.Ace.Editor) => {
        setCode(editor.getValue());
      }
    },
    {
      name: 'copyAll',
      description: "Copy all text to clipboard",
      exec: (editor: ace.Ace.Editor) => {
        unsecureCopyTextToClipboard(editor.getValue());
      }
    },
    {
      name: 'reset',
      exec: () => {
        resetEditor();
      }
    },
    {
      name: 'keepFocus',
      description: "Return cursor to editor",
      exec: () => {
        keepFocus.current = true;
      }
    },
    {
      name: "setMode",
      description: "Set language mode",
      exec: (editor: ace.Ace.Editor, lang: string) => {
          if(lang && typeof lang === "string")
            editor.getSession().setMode("ace/mode/" + lang);
      },
      readOnly: true
    },
    {
      name: "changeShortcuts",
      description: "Switch shortcuts",
      exec: (editor: any, shortcuts?: string) => {
        if(shortcuts && typeof shortcuts === "string")
          editor.setKeyboardHandler("ace/keyboard/" + shortcuts);
        else {
          //rotate through the available keyboard handlers
          const handlers = ["ace/keyboard/vim", "ace/keyboard/emacs", "ace/keyboard/sublime", "ace/keyboard/vscode"];
          const currentHandler = handlers[(handlers.indexOf(editor.$keybindingId) + 1) % 4];
          editor.setKeyboardHandler(currentHandler);
        }
      },
      readOnly: true
    },
    {
      name: 'toggleKeyboardShortcuts',
      exec: (editor: ace.Ace.Editor) => {
        if(!document.getElementById('kbshortcutmenu'))
          editor.execCommand('showKeyboardShortcuts');
        else 
          editor.execCommand('simulateKeyPress', {type:"keydown", keyCode: 27});
      }
    },
    {
      name: 'simulateKeyPress',
      exec: (editor: ace.Ace.Editor, args: {type: string, key?: string, keyCode?: number}) => {
        if(args.key)
          document.dispatchEvent(new KeyboardEvent(args.type,{'key': args.key})); 
        else if(args.keyCode)
          document.dispatchEvent(new KeyboardEvent(args.type,{'keyCode': args.keyCode})); 
      }
    },
    {
      name: 'infoMessage',
      description: "Display message in info bar",
      exec: (editor: ace.Ace.Editor, args: {text: string, timeout?: number, classToggle?: string, targetQueryString?: string} ) => {
        if(args.targetQueryString){
          const target = document.querySelector(args.targetQueryString) as HTMLElement;
          if(target){
            target.innerText = args.text;
            target.classList.add(args.classToggle || "")
            if(args.timeout){
              timeoutId = setTimeout(() => {
                target.classList.remove(args.classToggle || "");
              }, args.timeout);
            }
          }
        }
        else if(infoTextRef.current){
          infoTextRef.current.innerText = args.text;
          infoTextRef.current.classList.add(args.classToggle || "");
          if(args.timeout){
            timeoutId = setTimeout(() => {
              infoTextRef.current?.classList.remove(args.classToggle || "");
            }, args.timeout);
          }
        }
      }
    },
    {
      name: 'response', //name for the key binding.
      description: "Send custom response", //description of the command
      exec: (editor: any, responseType = "") => {
        const outgoingMode = editor.getSession().$modeId.split("/").pop();
        Streamlit.setComponentValue({id: v1().slice(0,8), type: responseType, lang: outgoingMode, text: editor.getValue(), selected: editor.getSelectedText(), cursor: editor.getCursorPosition()});
      }
    },
    {
      name: 'returnSelection', //name for the key binding.
      description: "Send selected text to Streamlit", //description of the command
      exec: (editor: any) => {
        const outgoingMode = editor.getSession().$modeId.split("/").pop();
        Streamlit.setComponentValue({id: v1().slice(0,8), type: "selection", lang: outgoingMode, text: editor.getSelectedText(), cursor: editor.getCursorPosition()});
      }
    },
    {
      name: 'editSnippets',
      description: "Edit snippets",
      bindKey: { win: 'Ctrl-Alt-N', mac: 'Command-Alt-M' },
      exec: (editor: any) => {
        const snippetManager = ace.require('ace/snippets').snippetManager;
        if(baseSession.current){
          const outgoingMode = editor.getSession().$modeId.split("/").pop();
          if(outgoingMode === "snippets"){
            const snippetText = editor.getSession().getValue();
            editor.setSession(baseSession.current);
            baseSession.current = null;
            setCode(editor.getSession().getValue());
            if(outgoingMode === "snippets"){}
            try{
              const snippetsPlusMinus = snippetText.split("###~~~")[1];
              const [snippetsPlus, snippetsMinus] = snippetsPlusMinus.split("###---");
              const snippetsToAdd = snippetsPlus.split("###+++")[1];
              const snippetsToRemove = snippetsMinus;
              const langMode = editor.getSession().$modeId.split("/").pop();
              setSnippetAddRemove({[langMode] : [snippetAddRemove[langMode][0] + snippetsToAdd, snippetAddRemove[langMode][1] + snippetsToRemove]});
            } catch (error) {
              editor.execCommand("infoMessage",{text: "error parsing file, restoring original file", timeout: 2000, classToggle: "show"});
            }
          }
        } else {
          const langMode = editor.getSession().$modeId.split("/").pop()
          const snippetConcatText = `\n###~~~#(DO NOT EDIT THIS LINE)
# Commented out above are all the snippets that are currently
# registered for ${args['lang']} mode.
\n\n###+++#(DO NOT EDIT THIS LINE) \n# Put the snippets you want to add below this line.\n\n\n\n
\n\n\n###---#(DO NOT EDIT THIS LINE) \n# Put the snippets you want to remove below this line.\n\n\n\n\n\n\n`;
          const snippetText = "#" + createSnippets(snippetManager.snippetMap[langMode].map((snip: any) => ({name: snip.name, code: snip.content}))).replace(/\n/g, "\n#") + snippetConcatText;
          // snippetManager.files[editor.getSession().$modeId].snippetText
          const lineCount = (snippetText.match(/\n/g) || []).length;
          baseSession.current = editor.getSession();
          const snippetsSession = ace.createEditSession(snippetText, "ace/mode/snippets");
          editor.setSession(snippetsSession);
          const cursorPos = {row: (lineCount - 15)>0? lineCount - 15 : 0, column: 0};
          editor.moveCursorTo(cursorPos.row, cursorPos.column);
          editor.renderer.scrollCursorIntoView(cursorPos, 0.5);
        }
      }
    },
    {
      name: 'editKeyBindings',
      description: "Edit keybindings",
      bindKey: { win: 'Ctrl-Alt-B', mac: 'Command-Alt-B' },
      exec: (editor: any) => {
        ace.require('ace/autocomplete').Autocomplete.for(editor);
        if(baseSession.current){
          const outgoingMode = editor.getSession().$modeId.split("/").pop();
          if(outgoingMode === "json"){
            const keybindingsJSON = editor.getSession().getValue();
            editor.setSession(baseSession.current);
            baseSession.current = null;
            setCode(editor.getSession().getValue());
            try{
              setKeybindingAddRemove(JSON.parse(keybindingsJSON));
            } catch (error) {
              editor.execCommand("infoMessage",{text: "error parsing file, restoring original file", timeout: 2000, classToggle: "show"});
            }
          }
        } else {
          const keybindings = {commands: {}, completer: {}};
          if(editor.completer && editor.completer.keyboardHandler.commands){
            keybindings.completer = Object.keys(editor.completer.keyboardHandler.commands).map((key: any) => ({bindkey: editor.completer.keyboardHandler.commands[key].bindKey ?? "", name: editor.completer.keyboardHandler.commands[key].name}));
          }
          if(editor.commands.commands){
            keybindings.commands = Object.keys(editor.commands.commands).map((key: any) => ({bindkey: editor.commands.commands[key].bindKey ?? "", name: editor.commands.commands[key].name}));
          }
          const keybindingsJSON = JSON.stringify(keybindings, undefined, 2);
          baseSession.current = editor.getSession();
          const keybindingsSession = ace.createEditSession(keybindingsJSON, "ace/mode/json");
          editor.setSession(keybindingsSession);
        }
      }
    },
    {
      name: 'exitSession', //name for the key binding.
      bindKey: { win: 'Esc', mac: 'Esc' },
      description: "Return to main session (keep changes)", //description of the command
      exec: (editor: any) => {
        if(baseSession.current){
          const mode = editor.getSession().$modeId.split("/").pop();
          if (mode === "snippets")
            editor.execCommand("editSnippets");
          else if (mode === "json")
            editor.execCommand("editKeyBindings");
        }
      }
    },
    {
      name: 'abandonSession', //name for the key binding.
      bindKey: { win: 'Ctrl-Alt-Esc', mac: 'Command-Alt-Esc' },
      description: "Return to main session (discard changes)", //description of the command
      exec: (editor: any) => {
        if(baseSession.current){
          editor.setSession(baseSession.current);
          baseSession.current = null;
          setCode(editor.getSession().getValue());
        }
      }
    },
    {
      name: 'classART', //name for the key binding.
      description: "Add/Remove/Toggle class for element", //description of the command
      exec: (editor: any, args: {targetQueryString: string, type: string, class: string}) => {
        if(args.targetQueryString && args.type && args.class){
          switch(args.type){
            case "add":
              document.querySelectorAll(args.targetQueryString)?.forEach((el: any) => el.classList.add(args.class));
              break;
            case "remove":
              document.querySelectorAll(args.targetQueryString)?.forEach((el: any) => el.classList.remove(args.class));
              break;
            case "toggle":
              document.querySelectorAll(args.targetQueryString)?.forEach((el: any) => el.classList.toggle(args.class));
              break;
            default:
              break;
          }
        }
      }
    },
    {
      name: 'conditionalExecute', //name for the key binding.
      description: "Execute command if element exists", //description of the command
      exec: (editor: any, args: {targetQueryString: string, command: any[], condition?: boolean}) => {
        if(args.targetQueryString && args.command && Array.isArray(args.command)){
          if(!(args.condition ?? true) === !document.querySelector(args.targetQueryString)){
            typeof args.command[0] === "string" ? execute(args.command[0], args.command[1]) : console.warn("Editor command - conditionalExecute: improper command format! Command array must contain name of command as first element and arguments as second element.");
          }
        }
      }
    },
    {
      name: 'delayedExecute', //name for the key binding.
      description: "Execute command after a period of time", //description of the command
      exec: (editor: any, args: { command: string | any[], timeout?: number}) => {
        if(args.command){
          if(Array.isArray(args.command) && args.command.length === 2){
            typeof args.command[0] === "string" ? setTimeout(() => {execute(args.command[0], args.command[1])}, args.timeout ?? defaultProps.debounceChangePeriod) : console.warn("Editor command - conditionalExecute: improper command format! Command array must contain name of command as first element and arguments as second element.");
          }
          else if(typeof args.command === "string"){
            setTimeout(() => {
              execute(args.command as string);
            }, args.timeout ?? defaultProps.debounceChangePeriod);
          }
        }
      }
    }
  ]};

  const execute = (command: string, args: any = "") => {
    const editor = aceEditor.current?.editor;
    if (editor) {
      if (!args) {
        editor.execCommand(command)
      }
      else if (typeof args === "number" || typeof args === "string") {
        editor.execCommand(command, args);
      }
      else if (typeof args === "object" && !Array.isArray(args)) {
        var containsNumsStr = true;
        Object.keys(args).forEach((key: any) => {
          containsNumsStr = typeof args[key] === "string" || typeof args[key] === "number" || Array.isArray(args[key]);
        });
        if (Object.keys(args).length < 4 && containsNumsStr) {
          editor.execCommand(command, args);
        }
      }
      else {
        console.warn(`Function - execute: failed to parse/execute "${command}" command!`);
      }
    }
  }

  const executeAll = (commands: any[]) => {
    commands.forEach(singleCommand => {
      if (Array.isArray(singleCommand)) {
        typeof singleCommand[0] === "string" ? execute(singleCommand[0], singleCommand[1]) : console.warn("Function - executeAll: improper command format! Singular commands must contain name of command as first element and arguments as second element.");
      } else if (typeof singleCommand === "string") {
        execute(singleCommand);
      } else {
        console.warn("Function - executeAll: failed to parse/execute command(s)!");
      }
    });
  }

  const resetEditor = () => {
    setCode(args['code']);
  }

  const unsecureCopyTextToClipboard = (text: string) => {
    const textField = document.createElement('textarea');
    textField.value = text;
    document.body.appendChild(textField);
    textField.select();
    document.execCommand('copy');
    textField.remove();
  }

  /**
   * resizeObserver observes changes in elements its given to observe and is used here
   * to communicate to streamlit the height of the component that has changed
   * so that streamlit can adjust the iframe containing the component accordingly.
   */
  const resizeObserver = new ResizeObserver((entries: any) => {
    // If we know that the body will always fully contain our component (without cutting it off)
    // then we can use docuemnt.body height instead
    Streamlit.setFrameHeight((entries[0].contentBoxSize.blockSize ?? entries[0].contentRect.height)); 
  })

  const observe = (divElem: any) => {
    divElem ? resizeObserver.observe(divElem as HTMLDivElement) : resizeObserver.disconnect();
  }

  // This useEffect is used to reset the editor when the code argument changes and
  // the allow_reset argument is true. The allow_reset argument only impacts the
  // behavior of the component when the component has a fixed key argument because
  // changing the key argument results in the creation of a new component instance.
  // Everything would be reset anyways.
  useEffect(() => {
    if (args['allow_reset'] === true && args['code'] !== code) {
      reset.current = !reset.current;
      resetEditor();
    }
  }, [args['code']]);

  /**
   * This could also be memoized but I don't think it would be necessary because its not expensive.
   */
  const themeChoice = () => {
    const isDarkTheme = theme? theme.base === "dark" : true;
    switch (args['theme']) {
      case "contrast":
        return isDarkTheme? "streamlit_light" : "streamlit_dark";
      case "light":
        return "streamlit_light";
      case "dark":
        return "streamlit_dark";
      case "default":
        return isDarkTheme? "streamlit_dark" : "streamlit_light";
      default:
        return isDarkTheme? "streamlit_dark" : "streamlit_light";
    }
  }

  const themeProp = themeChoice();
  const componentContainerProps = args["component_props"];

  const {info: infoArg, menu: menuArg, focus: focusArg, code: codeArg, ...rest} = args;
  const editorArgsString = JSON.stringify(rest);
  const menuArgsString = JSON.stringify(menuArg);
  const infoArgsString = JSON.stringify(infoArg);
  const buttonArgsString = JSON.stringify(args['buttons']);
  const themeString = JSON.stringify(theme);
  const snippets = JSON.stringify(snippetAddRemove);

  /**
   * This section contains the main sub-components (child components). These components are wrapped in useMemos
   * in order to prevent unnecessary re-rendering of the components. This is listed as one of its use cases in the
   * React docs ({@link https://beta.reactjs.org/reference/react/useMemo#skipping-re-rendering-of-components Skipping re-rendering of components})
   *
   * This component is the editor component that is rendered. It is only re-rendered when
   * certain properties change. This is important because we should account for the possibility that the editor 
   * is being used at any given moment. Unnecessary and frequent re-rendering of the editor (for outside reasons
   * especially) can impact user experience and responsiveness.
   */
  const editor = useMemo(() => {
    const keybindings = JSON.stringify(keybindingAddRemove);
    const revertedArgs = JSON.parse(editorArgsString);

    // Create commands for each button
    if(revertedArgs['buttons'].length > 0) {
      revertedArgs['buttons'].forEach((button: any) => {
          commands.commands = [...commands.commands, {
            name: (button.name as string).trim().replace(/\s+/g, '_') + '_button',
            bindKey: button.bindKey,
            description: "Execute '" + button.name + "' button command(s)",
            exec: () => {
            executeAll(button.commands);
          }}];
      });
    }

    let heightProps = {};
    if(typeof revertedArgs['height'] === "number") 
      heightProps = {minLines: 1, maxLines: revertedArgs['height']};
    else if(typeof revertedArgs['height'] === "string") 
      heightProps = {height: revertedArgs['height']};
    else if(Array.isArray(revertedArgs['height']) && revertedArgs['height'].length === 2) 
      heightProps = {minLines: revertedArgs['height'][0], maxLines: revertedArgs['height'][1]};

    const aceEditorProps = { ...defaultEditorProps, ...revertedArgs['editorProps'] };
    const aceOptions = { ...defaultOptions, ...revertedArgs['options'] };
    const partProps = { setOptions: aceOptions, editorProps: aceEditorProps };
    const aceProps = { ...defaultProps, ...partProps,...heightProps, ...revertedArgs['props'] };

    /**
     * TODO: Remove props from aceProps that we don't want to allow user access to.
     */
    return (
        <Editor
         editorRef={aceEditor}
         code={code} 
         lang={revertedArgs['lang']} 
         theme={themeProp} 
         shortcuts={revertedArgs['shortcuts']} 
         snippetString={snippets} 
         commands={commands.commands} 
         keybindingString={keybindings} 
         props={aceProps} 
         onChange={onChangeHandler}
         onSelectionChange={onSelectionChangeHandler}
         onBlur={onEditorBlur}  
        />
      );
  }, [editorArgsString, themeProp, snippets, keybindingAddRemove, reset.current]);

  const buttons = useMemo(() => {
    const revertedButtons = JSON.parse(buttonArgsString);
    const revertedTheme = JSON.parse(themeString);
    const customButtonTheme = revertedTheme ?? {};
    const customButtons = {buttons: (revertedButtons ?? []) as customButton[], name: "customButtons"} as buttonGroup;
    return (
      < ButtonSet
       buttonGroup={customButtons} 
       theme={customButtonTheme} 
       themeProp={themeProp} 
       executeAll={(commands) => executeAll(commands)} />
    );
  }, [buttonArgsString, themeString, themeProp]);

  const menu = useMemo(() => {
    const revertedMenu = JSON.parse(menuArgsString);
    const revertedTheme = JSON.parse(themeString);
    const menuTheme = revertedTheme ?? {};
    return (
      <ButtonMenu
       menu={revertedMenu} 
       theme={menuTheme} 
       themeProp={themeProp} 
       executeAll={(commands) => executeAll(commands)} />
    );
  }, [menuArgsString, themeString, themeProp]);

  const info = useMemo(() => {
    const revertedInfo = JSON.parse(infoArgsString);
    const revertedTheme = JSON.parse(themeString);
    const infoTheme = revertedTheme ?? {};
    return (
      <InfoBar
       infoRef={infoTextRef} 
       info={revertedInfo} 
       theme={infoTheme} />
    );
  }, [infoArgsString, themeString]);

  const globalCSS = useMemo(() => {
    return (
      <GlobalCSS isDisabled={disabled} inject={componentContainerProps.globalCSS} />
    );
  }, [componentContainerProps.globalCSS, disabled]);

  return (
    <StyledCodeEditor ref={observe} style={componentContainerProps.style} css={componentContainerProps.css} className={"streamlit_code-editor " + theme?.base ?? "" } >
      {globalCSS}
      {editor}
      {buttons}
      {menu}
      {info}
    </StyledCodeEditor>
  )
}

export default withStreamlitConnection(CodeEditor)
