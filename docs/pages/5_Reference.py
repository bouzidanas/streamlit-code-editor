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
  max-width: 82rem;
}

table.doc .cell{
    width: 100%;
    border-collapse: collapse;
    border-top-width: 1px;
    --tw-border-opacity: 1;
    border-top-color: rgb(213 218 229/var(--tw-border-opacity));
    padding: 1rem;
}

table.doc .cell td {
    vertical-align: inherit;
    padding: 1rem;
}

table.doc .cell td p {
    margin-top: 1rem;
    margin-bottom: 1rem;
}

table.doc .cell td:first-child {
    width:25%
}

table.doc {
    font-family: Inter,ui-sans-serif,system-ui,Helvetica,Arial,sans-serif;
}

table.doc .bold {
    font-weight: 700;
}

table.doc .lbold {
    font-weight: 500;
}

table.doc .italic {
    font-style: italic;
}

table.doc ul {
    margin-left: 0.5rem;
}

table.doc .code {
    font-family: Source Code Pro,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;
}

table.doc .head-row{
    margin-bottom: 0;
    font-weight: 700;
    vertical-align: inherit;
    font-weight: bold;
    text-align: -internal-center;
    background-color: rgb(228 245 255/.5);
    --tw-text-opacity: 1;
    color: rgb(0 66 128/var(--tw-text-opacity));
}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

table_html_string = '''<table class="full-width doc">
    <thead>
        <tr >
            <th colspan="2" class="head-row cell">Function signature</th>
        </tr>
        <tr >
            <th colspan="2" class="cell">
                <p class="code"> ce.code_editor(code, lang='python', height=30, theme="default", shortcuts="vscode", focus=False, snippets=["", ""], keybindings={}, buttons=[], menu={}, info={}, component_props={}, props={}, editor_props={}, options={}, key=None)</p> 
            </th>
        </tr>
    </thead>
    <tbody>
        <tr >
            <td  colspan="2" class="head-row cell">Parameters</td>
        </tr>
        <tr class="cell">
            <td >
                <div>
                    <p class="">
                        <span class="bold">code</span>
                        <span class="italic code">(str)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>The text to be displayed and edited</p>
                </div>
            </td>
        </tr>
        <tr class="cell">
            <td >
                <div>
                    <p class="">
                        <span class="bold">lang</span>
                        <span class="italic code">(str)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>The mode (programming language). The editor will interpret, tokenize, and color the text accordingly.</p>
                </div>
            </td>
        </tr>
        <tr class="cell">
            <td >
                <div>
                    <p class="">
                        <span class="bold">height</span>
                        <span class="italic code">(str or int or list of two ints)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>The height of the code editor. Default value is 30. If a string is given, the css height property of the editor is set to the string. If a number is given, the `maxLines` property is set (to the number) instead. This means that the height will be adjusted to fit the number of lines in the code string upto but not exceeding the integer value given. In this case, the `minLines` attribute defaults to 1. If an array of two numbers is given, the first number will be used to set `minLines` and the second integer will be used to set `maxLines`.</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">theme</span>
                        <span class="italic code">("default" or "light" or "dark" or "contrast")</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>If 'light' or 'dark', the theme of the Ace Editor is set to 'streamlit-light' or 'streamlit-dark' respectively. If 'default', the theme is set to 'streamlit-light' if base="light" and 'streamlit-dark' if base="dark". If 'contrast', the theme is set to 'streamlit-dark' if base="light" and 'streamlit-light' if base="dark".</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">shortcuts</span>
                        <span class="italic code">("vscode" or "vim" or "emacs" or "sublime")</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>The keyboard handler to handle keyboard shortcuts and determines how the editor responds to certain keys. This argument defaults to "vscode".</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">focus</span>
                        <span class="italic code">(bool)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Default is False. If set to True, then set Focus to editor after first execution of the streamlit script and any later rerun where it was previously False.</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">snippets</span>
                        <span class="italic code">(list)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Add and/or remove snippets. Default is [ "" , "" ]. Provided list must have two elements. First element contains snippets to add in the form of a single string or a list of dictionaries. Second list element contains the snippets to remove provided in the form of a single string or a list of dictionaries</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">keybindings</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Add and or remove keybindings. Default is empty dictionary: {}.</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">buttons</span>
                        <span class="italic code">(list of dicts)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Add custom buttons. Default is empy list: []. To add a button, add a dictionary to the list with the following attributes:
                        <ul>
                            <li><span class="lbold">name</span> <span class="italic code">(str)</span>: name and text of the button</li>
                            <li><span class="lbold">feather</span> <span class="italic code">(str)</span>: name of the feather icon to be used (formatted as "IconName")</li>
                            <li><span class="lbold">iconSize</span> <span class="italic code">(int)</span>: size of the icon in pixels</li>
                            <li><span class="lbold">primary</span> <span class="italic code">(bool)</span>: if True, the button will be styled with the primary color</li>
                            <li><span class="lbold">hasText</span> <span class="italic code">(bool)</span>: if True, the button will have text. The text is the contents of the name attribute.</li>
                            <li><span class="lbold">showWithIcon</span> <span class="italic code">(bool)</span>: if True, the button will show the icon and the text. If False, the button will show only the icon.</li>
                            <li><span class="lbold">alwaysOn</span> <span class="italic code">(bool)</span>: if True, the button will always be visible. If False, the button will only be visible when the mouse hovers over the editor</li>
                            <li><span class="lbold">commands</span> <span class="italic code">(list)</span>: list of commands to be executed when the button is clicked</li>
                            <li><span class="lbold">toggledCommands</span> <span class="italic code">(list)</span>: list of commands to be executed when the button is clicked while the button is toggled</li>
                            <li><span class="lbold">class</span> <span class="italic code">(str)</span>: class name to be added to the button</li>
                            <li><span class="lbold">style</span> <span class="italic code">(dict)</span>: style properties to add to button</li>
                            <li><span class="lbold">theme</span> <span class="italic code">(dict)</span>: theme for button to use</li> 
                            <li><span class="lbold">classToggle</span> <span class="italic code">(str)</span>: class name to be added to the button when it is toggled</li>
                        </ul>
                    </p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">menu</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Add menu bar. Default is empty dictionary: {}</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">info</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Add info bar. Default is empty dictionary: {}. Attributes include: 
                        <ul>
                            <li><span class="lbold">name</span> <span class="italic code">(str)</span>: name of the info bar</li>
                            <li><span class="lbold">css</span> <span class="italic code">(str)</span>: css to be applied to the info bar</li>
                            <li><span class="lbold">style</span> <span class="italic code">(dict)</span>: style properties to be applied to the info bar</li>
                            <li><span class="lbold">info</span> <span class="italic code">(list)</span>: items/elements to add to the info bar. item dict attributes include
                                <ul>
                                    <li><span class="lbold">name</span> <span class="italic code">(str)</span>: name of the item and text to be displayed</li>
                                    <li><span class="lbold">class</span> <span class="italic code">(str)</span>: class name to be added to the item</li>
                                    <li><span class="lbold">style</span> <span class="italic code">(str)</span>: style properties to be applied to the item</li>
                                    <li><span class="lbold">theme</span> <span class="italic code">(str)</span>: theme for item to use</li>
                                </ul>
                            </li>
                        </ul>
                    </p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">component_props</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Argument that sets component properties. Default is empty dictionary, {}. Attributes include:
                        <ul> 
                            <li><span class="lbold">style</span> <span class="italic code">(dict)</span>: style properties</li>
                            <li><span class="lbold">css</span> <span class="italic code">(str)</span>: CSS to apply to Code Editor component. </li>
                            <li><span class="lbold">globalCSS</span> <span class="italic code">(str)</span>: global CSS that applies to document containing the Code Editor component</li>
                        </ul>
                    </p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">props</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Argument that sets Ace Editor's general properties. Default is empty dictionary, {}. Information on the general properties can be found at:<br/> <a href="https://github.com/securingsincity/react-ace/blob/master/docs/Ace.md#available-props">https://github.com/securingsincity/react-ace/blob/master/docs/Ace.md#available-props</a></p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">editor_props</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Argument that sets Ace Editor's editor properties. Default is empty dictionary, {}.</p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">options</span>
                        <span class="italic code">(dict)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>Argument that sets Ace Editor's options. Default is empty dictionary, {}. Information on the options available can be found at:<br/> <a href="https://github.com/ajaxorg/ace/wiki/Configuring-Ace">https://github.com/ajaxorg/ace/wiki/Configuring-Ace</a></p>
                </div>
            </td>
        </tr>
        <tr >
            <td >
                <div>
                    <p class="">
                        <span class="bold">key</span>
                        <span class="italic code">(str or int)</span>
                    </p>
                </div> 
            </td>
            <td >
                <div>
                    <p>An optional string or integer to use as the unique key for the editor. If this is omitted, a key will be generated. Multiple editors of the same type may not share the same key.</p>
                </div>
            </td>
        </tr>
    </tbody>
    <tfoot>
    </tfoot>
</table>'''

st.markdown(table_html_string, unsafe_allow_html=True)