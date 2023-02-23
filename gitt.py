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

		self.status_button = QtWidgets.QPushButton("git status")
		self.status_button.clicked.connect(self.run_git_status)

		self.add_button = QtWidgets.QPushButton("git add -u")
		self.add_button.clicked.connect(self.run_git_add_u)
		
		self.select_window_button = QtWidgets.QPushButton("select window")
		self.select_window_button.clicked.connect(self.select_window)

		self.output_label = QtWidgets.QLabel()

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.status_button)
		layout.addWidget(self.add_button)
		layout.addWidget(self.select_window_button)
		layout.addWidget(self.output_label)
		self.setLayout(layout)
		
		# ---------------------------------
		
		self.desktop = Desktop(backend="uia") 
		
		self.list_of_commands = [
			"git status",
			"git add -u",
			"gitk --all"
			]
		

	def run_git_status(self):
		self.w.set_focus()
		#self.w.type_keys('clear\n', with_spaces=True, with_newlines=True)
		self.w.type_keys('git status\n', with_spaces=True, with_newlines=True)

	def run_git_add_u(self):
		self.w.set_focus()
		self.w.type_keys('git status\n', with_spaces=True, with_newlines=True)


	def run_git_commit(self):
		self.w.set_focus()
		self.w.type_keys('git commit\n', with_spaces=True, with_newlines=True)



	def run_gitk_all(self):
		self.w.set_focus()
		self.w.type_keys('gitk --all\n', with_spaces=True, with_newlines=True)

	def highlight_w(self, item):
		select_win_name = item.text()

		for window in self.desktop.windows():
			if window.window_text() == select_win_name:
				#window.highlight(colour='red', delay=2)
				window.set_focus()

	def on_item_clicked_old(self, item):
		window_title = item.text()
		hwnd = win32gui.FindWindow(None, window_title)
		if hwnd:
			win32gui.SetForegroundWindow(hwnd)
			win32gui.ShowWindow(hwnd, win32gui.ILD_NORMAL)
			QtGui.QGuiApplication.primaryScreen().grabWindow(hwnd).highlight()

	def select_window(self):

		script_dir = os.path.dirname(os.path.abspath(__file__))
		#subprocess.Popen("powershell.exe", cwd=r".")
		#subprocess.Popen('cmd', creationflags=CREATE_NEW_CONSOLE)
		#subprocess.Popen(f'powershell.exe {script_dir}', creationflags=CREATE_NEW_CONSOLE)
		subprocess.Popen(f"""powershell.exe -noexit -command "cd '{script_dir}'" """, creationflags=CREATE_NEW_CONSOLE)

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

	def select_window_old(self):
		
		result = ""
		
		# Выводм все окна
		for w in self.desktop.windows():
			win_name = w.window_text()
			print( win_name, w.is_visible(), w.handle )
			result += f"{win_name}, {w.is_visible()}, {w.handle}\n"
		
		self.output_label.setText(result)
		
		#select_win_name = "Windows PowerShell"
		select_win_name = "*Безымянный – Блокнот"
		self.w = self.desktop.window(title=select_win_name) # Выбираем окно по имени



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = GitCommandsWindow()
	window.show()
	sys.exit(app.exec())
