import PySimpleGUI as sg

sg.ChangeLookAndFeel('LightGreen')      
sg.SetOptions(element_padding=(0, 0))      

#------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Save', 'Exit'  ]],      
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
            ['Help', 'About...'], ]      

# menu_def = [['File', ['Open', 'Save', 'Exit'  ]],]  

# ------ GUI Defintion ------ #      
layout = [
    [sg.Menu(menu_def, tearoff=True)],   
       
    [sg.Output(size=(60, 20))]      
]      

window = sg.Window("Windows-like program", layout, default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=False,      
                    default_button_element_size=(12, 1))      

# ------ Loop & Process button menu choices ------ #      
while True:      
    event, values = window.read()      
    if event == sg.WIN_CLOSED or event == 'Exit':      
        break      
    print('Button = ', event)      
    # ------ Process menu choices ------ #      
    if event == 'About...':      
        sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')      
    elif event == 'Open':      
        filename = sg.popup_get_file('file to open', no_window=True)      
        print(filename)  