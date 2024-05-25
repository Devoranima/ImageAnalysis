import sys
from PyQt5.QtWidgets import QApplication
from controllers.mainWindowController import MainWindowController

class AppController(QApplication):
  def __init__(self):
    super(AppController, self).__init__([])
    self.mainWindow = MainWindowController()

  def start(self):
    self.mainWindow.show()
    sys.exit(self.exec())

if __name__ == "__main__":
  app = AppController()
  app.start()
