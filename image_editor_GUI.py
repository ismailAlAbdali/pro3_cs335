# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QImage, QPalette, QAction
import image_editor_functions as img

## the Whole UI
class ImageLabGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()

        self.image = QImage()

    def initUI(self):

        self.setMinimumSize(500, 500)
        self.setWindowTitle("Image Lab")
        self.showMaximized()

        self.createImageCanvas()
        self.createMenuBar()
        self.createToolBar()

        self.show()

    def createImageCanvas(self):
       
        self.image_canvas = img.EditorFunctions(self)
        self.image_canvas.resize(self.image_canvas.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area.setWidget(self.image_canvas)
        self.setCentralWidget(self.scroll_area)


    def createMenuBar(self):

        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        # Create actions for menu bar
        self.open_action = QAction(QIcon("./icons/open.png"),'Open...', self)
        self.open_action.triggered.connect(self.image_canvas.openImage)

        self.save_action = QAction(QIcon("./icons/save.png"), "Save...", self)
        self.save_action.triggered.connect(self.image_canvas.saveImage)
        self.save_action.setEnabled(False)

        file_menu.addActions([self.open_action, self.save_action])

    def createToolBar(self):
        
        tool_bar = QToolBar("Toolbar")
        tool_bar.setIconSize(QSize(40, 40))
        self.addToolBar(tool_bar)

        self.rotate90_cw_act = QAction(QIcon("./icons/rotate90_cw.png"),'Rotate Right', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_canvas.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon("./icons/rotate90_ccw.png"),'Rotate Left', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_canvas.rotateImage90("ccw"))


        self.flip_vertical = QAction(QIcon("./icons/flip_vertical.png"), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.image_canvas.flipImage('vertical'))

        tool_bar.addActions([self.rotate90_ccw_act,self.rotate90_cw_act, self.flip_vertical])

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = ImageLabGUI()
    sys.exit(app.exec())