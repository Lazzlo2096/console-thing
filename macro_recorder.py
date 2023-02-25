from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key


class MacroRecorder:
	def __init__(self):

		self.clicks = []

		self.is_record = False

		def on_press(key):
			#print("Key pressed: {0}".format(key))
			
			#if key == Key.esc:
			#	self.stop()
			#if key == Key.f2:
			#	self.record()
			#if key == Key.f3:
			#	self.stop_record()
			#if key == Key.f4:
			#	self.play()
			
			pass

		def on_release(key):
			#print("Key released: {0}".format(key))
			pass

		def on_move(x, y):
			#print("Mouse moved to ({0}, {1})".format(x, y))
			pass

		def on_click(x, y, button, pressed):
		
			if self.is_record :
				self.clicks.append((x, y, button, pressed))
				
				if pressed:
					print('Mouse clicked at ({0}, {1}) with {2} {3}'.format(x, y, button, pressed))
				else:
					print('Mouse released at ({0}, {1}) with {2} {3}'.format(x, y, button, pressed))

		def on_scroll(x, y, dx, dy):
			#print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
			pass

		self.keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
		self.mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

	def record(self):
		print("record clicks")
		self.clicks = []
		self.is_record = True

	def stop_record(self):
		print("stop record clicks")
		self.is_record = False

	def play(self):
		print("play clicks")
		for x, y, button, pressed in self.clicks:
			print( (x, y, button, pressed) )
			#mouse.Controller().position = pos
			#mouse.Controller().click(mouse.Button.left, 1)
			#time.sleep(0.1)

	def start(self):
		# Start the threads and join them so the script doesn't end early
		self.keyboard_listener.start()
		self.mouse_listener.start()

		#self.keyboard_listener.join() # лол а как?
		#self.mouse_listener.join()

	def stop(self):
		print("stop")
		self.keyboard_listener.stop()
		self.mouse_listener.stop()


if __name__ == "__main__":
	mr = MacroRecorder()
	mr.start()

