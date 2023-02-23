import sys
import subprocess
from PySide6 import QtWidgets, QtGui


##------
import sys
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
##------


#import win32gui


from pywinauto import Desktop

import os
import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE


# ================================

class GitCommandsWindow(QtWidgets.QWidget):



	def __init__(self):
		super().__init__()

		self.setWindowTitle("Git Commands")
		self.setFixedSize(500, 500)

		# ---------------------------------

		list_of_commands = [
			"git status",
			"git add -u",
			"gitk --all", # не в консоли вообще? А путь как брать?
			"git commit",
			"git commit --amend",
			]

		self.output_label = QtWidgets.QLabel()

		# ---------------------------------

		self.layout = QtWidgets.QVBoxLayout()
		
		for command in list_of_commands:
			self.construct_button_and_to_layout(command, self.run)
			
		self.construct_button_and_to_layout("select window",          self.select_window)
		self.construct_button_and_to_layout("new console and select", self.new_console_and_select)

		self.layout.addWidget(self.output_label)
		self.setLayout(self.layout)
		
		# ---------------------------------
		
		self.desktop = Desktop(backend="uia") 


	def construct_button_and_to_layout(self, button_name, button_function):
		button = QtWidgets.QPushButton( button_name )
		button.clicked.connect( button_function )
		
		self.layout.addWidget( button )

	def run(self):
		button_name = self.sender().text() # лайфхак!
		print(f"run {button_name}")
		self.w.set_focus()
		self.w.type_keys(f'{button_name}\n', with_spaces=True, with_newlines=True)
			# если w не инициирован, то создать консоль и запустить в ней лол




	def highlight_w(self, item):
		select_win_name = item.text()

		for window in self.desktop.windows():
			if window.window_text() == select_win_name:
				#window.highlight(colour='red', delay=2)
				window.set_focus()

	def autoselect_console(self):
		pass

	def new_console_and_select(self): # нужно в некий стек консолей сделать лол # Склонировать консоль с тем же путём лол
		script_dir = os.path.dirname(os.path.abspath(__file__))
		#subprocess.Popen("powershell.exe", cwd=r".")
		#subprocess.Popen('cmd', creationflags=CREATE_NEW_CONSOLE)
		#subprocess.Popen(f'powershell.exe {script_dir}', creationflags=CREATE_NEW_CONSOLE)
		subprocess.Popen(f"""powershell.exe -noexit -command "cd '{script_dir}'" """, creationflags=CREATE_NEW_CONSOLE)

	def select_window(self):

		dialog = QtWidgets.QDialog(self)
		dialog.setWindowTitle("Select Window")
		#dialog.setFixedSize(400, 300)
		dialog.resize(600, 300)

		list_widget = QtWidgets.QListWidget()

		list_widget.itemClicked.connect(self.highlight_w)

		"""
		Число 32 в данном коде является флагом для функции SetWindowPos.
		Функция SetWindowPos используется для изменения позиции и размера окна, а также для изменения его Z-порядка (порядка наложения) и стилей.
		В данном случае, флаг SWP_SHOWWINDOW со значением 0x00000040 (32 в десятичной системе) указывает на то, что при изменении позиции окна, оно должно быть видимым (показано на экране).
		"""

		for w in self.desktop.windows():
			win_name = w.window_text()
			win_handle = w.handle
			#item = QtWidgets.QListWidgetItem(f"{win_handle}\t{win_name}")
			item = QtWidgets.QListWidgetItem(win_name)
			item.setData(32, win_handle)  # сохраняем handle окна
			list_widget.addItem(item)
		
		
		# Устанавливаем размер диалога по размеру элементов списка
		#dialog.resize(list_widget.sizeHint())
		#dialog.resize( list_widget.sizeHintForColumn(0), 200 )
		#dialog.setFixedSize(list_widget.sizeHintForColumn(0), 300)

		layout = QtWidgets.QVBoxLayout(dialog)
		layout.addWidget(list_widget)
		#dialog.setLayout(layout)

		def on_ok():
			item = list_widget.currentItem()
			if item is not None:
				
				handle = item.data(32)
				self.w = self.desktop.window(handle=handle)
				
				select_win_name = item.text()
				self.output_label.setText(f"Selected Window: {select_win_name}")
				
				dialog.accept()
			else:
				dialog.reject()

		button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
		button_box.accepted.connect(on_ok)
		button_box.rejected.connect(dialog.reject)

		layout.addWidget(button_box)

		dialog.exec()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = GitCommandsWindow()
	window.show()
	sys.exit(app.exec())
