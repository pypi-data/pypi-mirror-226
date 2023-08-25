from tkinter import *

class App:
	def __init__(self, title, width, height):
		# 初始化窗口
		root = self.root = Tk()
		# 标题，不可变大小，大小，居中
		root.title(title)
		root.resizable(False, False)
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		x = (screen_width - width) // 2
		y = (screen_height - height) // 2
		root.geometry(f"{width}x{height}+{x}+{y}")
		# 创建UI组件
		self.UI(root)
		# 等待用户操作
		root.mainloop()
	def UI(self, root):
		pass
