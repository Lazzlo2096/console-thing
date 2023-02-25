import sys
import subprocess
from PySide6 import QtWidgets, QtGui


##------
import sys
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
##------


import win32gui
import win32api
import win32process
import time


from pywinauto import Desktop

import os
import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE

# TODOs:
# record macros
# many menus
# do thing by one key (shortcuts) !

# сделать граф интерфейс для торг бота!

from macro_recorder import MacroRecorder

# ================================

class Automation:

	def __init__(self):

		self.desktop = Desktop(backend="uia")  # backend="win32"

		self.list_of_commands = [
			"git status",
			"git add -u",
			"gitk --all", # не в консоли вообще? А путь как брать?
			"git commit",
			"git commit --amend",
			]
		
		#self.selected_win_name = None
		self.selected_win_handle = None
		#self.selected_win_id = None

	def run_command(self, command):
		print(f"run {command}")
		self.selected_win_handle.set_focus()
		self.selected_win_handle.type_keys(f'{command}\n', with_spaces=True, with_newlines=True)


	def highlight_window(self, win_name):

		for window in self.desktop.windows():
			if window.window_text() == win_name:
				#window.highlight(colour='red', delay=2)
				window.set_focus()

	def get_all_windows(self):
		pass

class GitCommandsWindow(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		
		# -----------------------
		self.am = Automation()
		
		self.mr = MacroRecorder()
		self.mr.start()
		# -----------------------

		self.setWindowTitle("Git Commands")
		self.setFixedSize(500, 500)

		# ---------------------------------

		self.output_label = QtWidgets.QLabel()

		# ---------------------------------

		self.layout = QtWidgets.QVBoxLayout()
		
		for command in self.am.list_of_commands:
			self.construct_button_and_to_layout(command, self.run_command)
		
		self.construct_button_and_to_layout("select window",          self.select_window)
		self.construct_button_and_to_layout("new console and select", self.new_console_and_select_v2) # это от гуи? или от Аутамато? # Создавать отдельный класс пока нет смысла!
		
		self.construct_button_and_to_layout("start_recording", self.mr.record)
		self.construct_button_and_to_layout("stop_recording", self.mr.stop_record)
		self.construct_button_and_to_layout("play_recorded_clicks", self.mr.play)

		self.layout.addWidget(self.output_label)
		self.setLayout(self.layout)
		
		# ---------------------------------



	def construct_button_and_to_layout(self, button_name, button_function):
		button = QtWidgets.QPushButton( button_name )
		button.clicked.connect( button_function )
		
		self.layout.addWidget( button )

	def run_command(self):
		button_name_command = self.sender().text() # лайфхак!
		
		# если w не инициирован, то создать консоль и запустить в ней
		if self.am.selected_win_handle == None :
			#self.am.new_console_and_select()
			self.am.selected_win_handle = self.new_console_and_select_v2()
		
		self.am.run_command( button_name_command )
			

	def highlight_window(self, item):
		win_name = item.text()
		self.am.highlight_window(win_name)


	


	def new_console(self): 
		script_dir = os.path.dirname(os.path.abspath(__file__))
		#subprocess.Popen("powershell.exe", cwd=r".")
		#subprocess.Popen('cmd', creationflags=CREATE_NEW_CONSOLE)
		#subprocess.Popen(f'powershell.exe {script_dir}', creationflags=CREATE_NEW_CONSOLE)
		process = subprocess.Popen(f"""powershell.exe -noexit -command "cd '{script_dir}'" """, creationflags=CREATE_NEW_CONSOLE)
		
		return process

	def autoselect_any_console(self):
		self.am.selected_win_handle = self.am.desktop.window(title="Windows PowerShell")
		self.am.selected_win_handle.set_focus()
		# TODO: создать консоль, если не найдено ни одной!

	def new_console_and_select_v2(self):
		process = self.new_console()
		self.autoselect_any_console()

	def get_descr_win_of_descr_pid(self, pid_):
		print( pid_ )
		# Получить идентификатор процесса PowerShell
		_, pid = win32process.GetWindowThreadProcessId(pid_)
		print( pid )

		# Функция для проверки каждого окна на рабочем столе
		def enum_windows_callback(hwnd, _):
			# Получить идентификатор процесса, связанный с окном
			_, window_pid = win32process.GetWindowThreadProcessId(hwnd)
			# Если идентификатор процесса соответствует идентификатору процесса PowerShell,
			# то это окно, которое мы ищем
			if window_pid == pid:
				return hwnd

		# Перечислить все окна и найти окно, связанное с процессом PowerShell
		hwnd = win32gui.EnumWindows(enum_windows_callback, None)
			
		print( hwnd )

		# Получить заголовок окна
		title = win32gui.GetWindowText(hwnd)
		print(title)

	def new_console_and_select(self): # нужно в некий стек консолей сделать лол # Склонировать консоль с тем же путём лол
	
		process = self.new_console()

		self.am.w = self.get_descr_win_of_descr_pid( process._handle )
		
		return

		print( "descr proc", process._handle )
		time.sleep(2)
		title = win32gui.GetWindowText( process._handle )
		print( "title",  title )
		


		# Получить дескриптор окна
		hwnd2 = win32gui.FindWindow(None, "Windows PowerShell")
		print(hwnd2) # верно
		# Получить заголовок окна
		title = win32gui.GetWindowText(hwnd2)
		print( "title", title)# верно
		
		# -------------------------
		
		# Получить дескриптор потока и идентификатор процесса PowerShell
		hwnd = None
		while hwnd is None:
			_, pid = win32process.GetWindowThreadProcessId(process._handle)
			print( pid )
			hwnd = win32gui.FindWindow(None, f"Windows PowerShell - {pid}")

		print( hwnd )
		# Получить заголовок окна
		title = win32gui.GetWindowText(hwnd)
		print( "title", title)
		
		return hwnd

	def select_window(self):

		dialog = QtWidgets.QDialog(self)
		dialog.setWindowTitle("Select Window")
		#dialog.setFixedSize(400, 300)
		dialog.resize(600, 300)

		list_widget = QtWidgets.QListWidget()

		list_widget.itemClicked.connect(self.highlight_window)

		"""
		Число 32 в данном коде является флагом для функции SetWindowPos.
		Функция SetWindowPos используется для изменения позиции и размера окна, а также для изменения его Z-порядка (порядка наложения) и стилей.
		В данном случае, флаг SWP_SHOWWINDOW со значением 0x00000040 (32 в десятичной системе) указывает на то, что при изменении позиции окна, оно должно быть видимым (показано на экране).
		"""

		#-------------- лол, тут тоже смоежное
		for w in self.am.desktop.windows():
			win_name = w.window_text()
			win_handle = w.handle
			item = QtWidgets.QListWidgetItem(f"{win_handle}\t{win_name}")
			#item = QtWidgets.QListWidgetItem(win_name)
			print(win_name)
			item.setData(32, win_handle)  # сохраняем handle окна
			list_widget.addItem(item)
		#--------------
		
		
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
				self.am.selected_win_handle = self.am.desktop.window(handle=handle)
				
				selected_win_name = item.text()
				self.output_label.setText(f"Selected Window: {selected_win_name}")
				
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
