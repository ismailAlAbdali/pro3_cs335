# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtCore import QFile
# from ui_mainwindow import Ui_Dialog

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.ui = Ui_Dialog()
#         self.ui.setupUi(self)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     window = MainWindow()
#     window.show()

#     sys.exit(app.exec())
    
    
    
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# from ui_mainwindow import Ui_Dialog  # Import the generated UI class

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         # Create an instance of the UI class
#         self.ui = Ui_Dialog()
#         self.ui.setupUi(self)

#         # Connect signals and slots or add custom functionality here

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
    
    
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow  # Import the generated UI class

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create an instance of the UI class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals and slots or add custom functionality here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
