
menubar_ss = """
QMenuBar {
    background-color: lightgray;
}
QMenuBar::item:selected {    
    background-color: #646464;
    color: rgb(255,255,255);
}
QMenuBar::item:pressed {
    background: #646464;
}
QMenu {
    background-color: lightgray;   
    border: 1px solid black;
    margin: 2px;
    border-radius: 5px;
}
QMenu::item {
    background-color: transparent;
}
QMenu::item:selected { 
    background-color: #646464;
    color: rgb(255,255,255);
}
"""

qss = """
QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 lightgray, stop:1 darkgray);
}
QMenuBar::item {
    spacing: 3px;           
    padding: 2px 10px;
    background-color: rgb(210,105,30);
    color: rgb(255,255,255);  
    border-radius: 5px;
}
QMenuBar::item:selected {    
    background-color: rgb(244,164,96);
}
QMenuBar::item:pressed {
    background: rgb(128,0,0);
}

/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  

QMenu {
    background-color: #ABABAB;   
    border: 1px solid black;
    margin: 2px;
}
QMenu::item {
    background-color: transparent;
}
QMenu::item:selected { 
    background-color: #654321;
    color: rgb(255,255,255);
}
"""