// import styled, { ThemeProvider, css } from "styled-components"
import { useRef, useState } from "react"
import styled, { ThemeProvider } from 'styled-components/macro'
import * as Icons from "react-feather"


export interface customInfoText {
  name: string,
  class?: string,
  style?: object,
  theme?: object
}

export interface infoBar {
  name?: string,
  css?: string,
  style?: object,
  info?: customInfoText[]
}

export interface customButton {
  name: string,
  feather?: string,
  iconSize?: number,
  primary?: boolean,
  hasText?: boolean,
  showWithIcon?: boolean,
  alwaysOn?: boolean,
  commands?: any[],
  toggledCommands?: any[],
  bindKey?: string | object,
  class?: string,
  style?: object,
  theme?: object, 
  classToggle?: string,
}

export interface buttonGroup {
  name: string,
  buttons: customButton[],
  style?: object,
  toggleOnlyOne?: boolean,
}

export interface menu {
  style?: object,
  css?: string,
  groups?: buttonGroup[]
}

export const StyledDiv = styled.div``;
export const StyledRegSpan = styled.span``;

export const StyledSpan = styled.span`
  height: 2.5rem;
  line-height: 2.5rem;
  margin: 0px 0.4rem 0.15rem 0.4rem;
  opacity: 0;
  transform: scale(0);
  transition: opacity 300ms 150ms, transform 300ms 150ms;
`;

export const StyledButton = styled.button<{primary?: boolean, themeProp: string, theme: object}>`
  border: none;
  border-radius: 5px;
  background: none;
  height: 2.5rem;
  line-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  position: absolute;
  transform: scale(0);
  transition: opacity 20ms 300ms, transform 20ms 300ms;
  z-index: 9994;
  :focus {
    outline: none;
  }
  span{
    color: ${props => props.themeProp === "streamlit_dark"? "rgba(250,250,250,0.6)": "rgba(0,0,0,0.5)"};
    transform: scale(0);
    transform-origin: right;
    transition: opacity 300ms 150ms, transform 300ms 150ms;
  }
  :hover span {
    color: ${props => props.primary? props.theme.primaryColor : props.themeProp === "streamlit_dark"? "rgb(250,250,250)" : "rgb(49, 51, 63)"};
    opacity: 1;
    transform: scale(1);
  }
  svg {
    stroke: ${props => props.themeProp === "streamlit_dark"? "rgba(250,250,250,0.6)": "rgba(0,0,0,0.5)"};
    transform: scale(0);
    transition: opacity 300ms 150ms, transform 300ms 150ms;
  }
  :hover svg {
    stroke: ${props => props.primary? props.theme.primaryColor : props.themeProp === "streamlit_dark"? "rgb(250,250,250)" : "rgb(49, 51, 63)"};
  }
`;

export type iconKey = keyof typeof Icons;

export const creatIcon = (name: iconKey, size = 16) => {
  const CustomIcon = Icons[name];
  return <CustomIcon size={`${size}`} />;
}

export type CustomInfoBar = {
  theme: object,
  info: infoBar,
  infoRef: any,
}

export const Info = ({info, theme, infoRef}: CustomInfoBar) => {

  return (
    <ThemeProvider theme={theme}>
      {(Object.keys(info).length === 0) ? `` : <StyledDiv key="info_bar" className={"custom_info_bar " + (info.name? info.name : "")} css={info.css} style={info.style}>
        {<StyledRegSpan ref={infoRef} key="code_editor_info_message" className="code_editor-info message">
          </StyledRegSpan>}
        {(info.info || []).map((info: customInfoText)=>(
          <StyledRegSpan key={"info_" + info.name} className={info.class} style={info.style}>
            {info.name}
          </StyledRegSpan>
        ))}
      </StyledDiv>}
    </ThemeProvider>);
}
  
export type CustomButtonType = {
  button: customButton, 
  theme: object, 
  themeProp: string, 
  executeAll: (ref: React.RefObject<HTMLButtonElement>, commands: any[]) => void
}
export const Button = ({button, theme, themeProp, executeAll}: CustomButtonType) => {
  const [toggle, setToggle] = useState(false);     //this toggle is currently not being used
  const ref = useRef<HTMLButtonElement>(null);

  const execute = (commands: any[], toggledCommands?: any[]) => {
    if(button.classToggle){
      setToggle(!toggle);
      if (ref.current){
        ref.current.classList.toggle(button.classToggle);
        if(ref.current.classList.contains(button.classToggle))
          executeAll(ref, commands);
        else
          executeAll(ref, toggledCommands ?? commands);
      }
      else 
        executeAll(ref, toggle? toggledCommands?? commands : commands);
    } 
    else 
      executeAll(ref, commands);
  }

  return (
    <StyledButton 
      ref={ref}
      primary={button.primary? button.primary : false} 
      className={(button.class? button.class: "" ) + (button.alwaysOn? " always-on" : "") + (button.showWithIcon? " with-icon" : "") }
      themeProp={themeProp}
      style={button.style} 
      theme={theme}
      onClick={() => execute(button.commands ?? [], button.toggledCommands)}>
        {(button.hasText && button.name)? <StyledSpan >{button.name}</StyledSpan> : ``}
        {button.feather? creatIcon(button.feather as iconKey || "X", button.iconSize) : ""}
    </StyledButton>
  )
}

export type CustomButtonSet = 
{
  theme: object,
  themeProp: string,
  buttonGroup: buttonGroup,
  executeAll: (commands: any[]) => void 
}
  
export const Set = ({buttonGroup, executeAll, theme, themeProp}: CustomButtonSet) => {

  const execute = (buttonRef: React.RefObject<HTMLButtonElement>, commands: any[]) => {
    // Do things here that depend on which button is clicked using buttonRef.current
    if(commands)
      executeAll(commands);
  }

  return (
      <ThemeProvider theme={theme}>
        {buttonGroup.buttons.map( (button) => (
        <Button 
          key={buttonGroup.name + "_" + button.name}
          button={button}
          themeProp={themeProp}
          theme={theme}
          executeAll={(ref, commands) => execute(ref, commands)}/>
      ))}
    </ThemeProvider>
  )
}
  
export type CustomMenu = 
{
  menu : menu,
  theme: object,
  themeProp: string,
  executeAll: (commands: any[]) => void
}
  
export const Menu = ({menu, executeAll, theme, themeProp}: CustomMenu) => {

  const execute = (buttonRef: React.RefObject<HTMLButtonElement>, commands: any[]) => {
    // Do things here that depend on which button is clicked using buttonRef.current
    if(commands)
      executeAll(commands);
  }
  
  return (
    <ThemeProvider theme={theme}>
      {(Object.keys(menu).length === 0 )? "" : <StyledDiv key="menu_bar" className="custom_menu" style={menu.style} css={menu.css}>
        {!menu.groups? `` : menu.groups.map((group: buttonGroup, index) => (
          <StyledDiv key={"group_" + group.name + index} className={"menu_group " + group.name} style={group.style} data-one-toggle-only={group.toggleOnlyOne} >
              {group.buttons.map((button: customButton,)=>(
                <Button 
                  key={group.name + "_" + button.name}
                  button={button}
                  themeProp={themeProp}
                  theme={theme}
                  executeAll={(ref, commands) => execute(ref, commands)}/>
              ))}
          </StyledDiv>
        ))}
      </StyledDiv>}
    </ThemeProvider>
  )
}