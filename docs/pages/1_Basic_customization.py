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
  max-width: 80rem;
}  
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)


col1, col2 = st.columns([6,2])
with col1:
    st.markdown("## Basic customization")
    st.markdown("In this section, we will go over the `height`, `theme`, `shortcuts`, and `focus` properties.")
    st.markdown("### Height")
    st.markdown("The height of the code editor can be set with the `height` argument. The height argument takes one of three types of values: a string, an integer number, or an list of two integers.")
    st.code('''# set height of editor to 500 pixels\nresponse_dict = code_editor(your_code_string, height="500px")\n\n# set height to adjust to fit up to 20 lines (and scroll for more)\nresponse_dict = code_editor(your_code_string, height=20)\n\n# set height to display a minimum of 10 lines and a maximum of 20 lines\n# (and scroll for more)\nresponse_dict = code_editor(your_code_string, height=[10, 20])''')
    st.markdown("If a string is given, it will be used to set the css height property of the editor part of the code editor component. This means that height can be set with strings like '500px' or '20rem' for example.")
    st.markdown("If instead, `height` is set with an integer, it will be used to set the `maxLines` property of the editor. This means that the height will be adjusted to fit the number of lines in the code string upto but not exceeding the integer value given. It might be that you always want the editor to fit the code so that no scrolling is needed. In this case, you can set `height` to a large integer value like 1000.")
    st.markdown("As you might have guessed, the inner editor also has a `minLines` property. It is set to 1 by default. If you want to set the minimum number of lines, you can set `height` to an list of two integers. The first integer will be used to set `minLines` and the second integer will be used to set `maxLines`.")

    st.success("**Tip:** If you set both `minLines` and `maxLines` to the same value, the editor will fix its size to fit only that number of lines of text. This is useful if you want the editor to have a static size and you want to size it according to number of lines to show.")
    st.info("**Note:** The height property does not limit the contents of the editor. Content that exceeds the height will be scrollable.")

    st.markdown("### Theme")
    st.markdown("As mentioned earlier, the code editor component contains an inner editor component. This inner editor is an [Ace Editor](https://ace.c9.io/) which comes with 20 built in themes. These themes share certain characteristics in appearance that I feel clash with streamlit's modern look. For better integration with streamlit's look, I have created a two custom Ace Editor themes called 'streamlit-dark' and 'streamlit-light'. These two themes can be used as a starting point for further customization of appearence as we will see in later sections.")
    st.markdown("By default, the code editor chooses one of the two custom themes according to the `base` attribute of streamlit's theme section of config options (see [Advanced features - Theming](https://docs.streamlit.io/library/advanced-features/theming) for more details). For more control over which of the two is chosen, you can use the `theme` argument of Code Editor. The `theme` argument takes one of four string values: 'default', 'dark', 'light', 'contrast'.")
    response_theme_light = code_editor('''# set theme to 'streamlit-dark' if base is 'dark' and \n# 'streamlit-light' if base is 'light'\nresponse_dict = code_editor(your_code_string, theme="default")''', theme="default")
    response_theme_contrast = code_editor('''# set theme to 'streamlit-light' if base is 'dark' and \n# 'streamlit-dark' if base is 'light'\nresponse_dict = code_editor(your_code_string, theme="contrast")''', theme="contrast")
    st.markdown('''Values 'dark' and 'light' will select 'streamlit-dark' and 'streamlit-light' respectively. The 'default' value will choose the 'streamlit-light' theme if `base="light"` and 'streamlit-dark' if `base="dark"`. Finally, passing in 'contrast' will do the exact opposite of 'default'.''')

    st.markdown("### Shortcuts")
    st.markdown("Ace Editor comes with four keyboard handlers: 'vim', 'emacs', 'vscode', and 'sublime'. The keyboard handler dictates what keyboard keys and key combinations will do by default. You can select the handler to start the editor with using the `shortcuts` argument. The `shortcuts` argument takes one of four string values: 'vim', 'emacs', 'vscode', 'sublime'. The default value for `shortcuts` is 'vscode'.")
    response_shortcuts = code_editor('''# set keyboard handler to 'vim'\nresponse_dict = code_editor(your_code_string, shortcuts="vim")''', shortcuts="vim")

    st.markdown("### Focus")
    st.markdown("There maybe times when you want to focus the editor when it loads (to start or continue editing after script is run/re-run without having to click into the editor). You can do this by setting the `focus` argument to `True`. The default value for `focus` is `False`.")
    response_focus = code_editor('''# set focus to True\nresponse_dict = code_editor(your_code_string, focus=True)''', focus=True)
    st.markdown("There is one very important detail to note about the `focus` feature. Focus will be given to the editor only when the value of `focus` changes from `False` to `True`. This means that if you set `focus` to `True` in the first run of the script, it will not be given focus in subsequent runs. To give focus to the editor in subsequent runs, you will have to set `focus` to `False` and then `True` again. This is to avoid giving focus to the editor when it is not intended because streamlit script re-runs are not the only cause of component re-renders (resizing the browser window, for example, can also cause components to re-render) and each time the editor re-renders, it will respond to the value of the `focus` argument. ")

floating_side_bar = '''
<div class="floating-side-bar">
    <span class="flt-bar-hd"> CONTENTS </span>
    <a href="#basic-customization">Basic customization</a>
    <a class="l2" href="#height">Height</a>
    <a class="l2" href="#theme">Theme</a>
    <a class="l2" href="#shortcuts">Shortcuts</a>
    <a class="l2" href="#focus">Focus</a>
    <span class="flt-bar-hd"> LINKS </span>
    <a href="https://ace.c9.io/">Ace Editor</a>
    <a href="https://docs.streamlit.io/library/advanced-features/theming">Advanced features - Theming</a>
</div>
'''

with col2:
    st.markdown(floating_side_bar, unsafe_allow_html=True)