# https://www.javatpoint.com/dropdown-list-in-kivy
# Python Program for explaining how to create a drop-down in kivy   
# first we will import kivy module      
import kivy    
         
# the base Class of our Application is inherited from the App class.      
# app is alway used for refering to the instance of our application     
from kivy.app import App   
       
# this will restrict the kivy version that means we can not use   
# the application or software below this Version of Kivy     
kivy.require('1.9.0')   
       
# Now we will import the Drop-down from the module for using it in the program  
from kivy.uix.dropdown import DropDown  

# The Button will be a Label with associated actions which will be released when the button is clicked  
from kivy.uix.button import Button  
    
# the another way used for running the kivy application   
from kivy.base import runTouchApp  
    
# now we will create the dropdown with 15 buttons  
drop_down = DropDown()  
for index in range(15):  
    
    # now, Add the button in the drop down list  
    btton = Button(text ='List % d' % index, size_hint_y = None, height = 30)  
    
    # now we will bind the button for showing the text when it is selected  
    btton.bind(on_release = lambda btton: drop_down.select(btton.text))  
    
    # then we will add the button inside the drop_down list  
    drop_down.add_widget(btton)  
    
# now we will create the big main button  
main_button = Button(text ='MAIN', size_hint =(None, None), pos =(350, 300))  
    
# now, we will first show the drop_down menu when the main button will releases  
# we should note that all of the bind() function calls will pass the instance of the caller   
# as the first argument of the callback (in this program, the main_button instance)  
# now, dropdown.open.  
main_button.bind(on_release = drop_down.open)  
    
# now we have to do last thing, listen for the selection in the   
# dropdown list and assign the data to the button text.  
drop_down.bind(on_select = lambda instance, x: setattr(main_button, 'text', x))  
    
# runtouchApp:  
# If we pass only the widget in runtouchApp(), the Window will be  
# created and our widget will be added to that window as the root widget.  
runTouchApp(main_button)  