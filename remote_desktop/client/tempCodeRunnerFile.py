with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while not self.accepted or not self.connected:
                pass
            listener.join()
            while self.connected:  
                pass 
            listener.stop()