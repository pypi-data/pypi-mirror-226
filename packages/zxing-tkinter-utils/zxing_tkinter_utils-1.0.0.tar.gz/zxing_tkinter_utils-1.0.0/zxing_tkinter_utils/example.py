from tkinter import *

from zxing_tkinter_utils.core import App

class MyApp(App):
	def __init__(self):
		super().__init__("这是标题。", 400, 300)
	def UI(self, root):
		label = Label(root, text="这是一段文字。")
		label.pack()
MyApp()
