## Sample Python application demonstrating the
## working with images in Kivy using .kv file

##################################################
# import kivy module
import kivy
	
# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
from kivy.uix.boxlayout import BoxLayout

# to change the kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

# creating the root widget used in .kv file
class Imagekv(BoxLayout):
	'''
		no need to do anything here as
		we are building things in .kv file
	'''
	pass

# class in which name .kv file must be named My.kv.
class HelmetApp(App):
	# define build() function
	def build(self):
		# returning the instance of Imagekv class
		return Imagekv()

# run the App
if __name__ == '__main__':
	HelmetApp().run()
