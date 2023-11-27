# Import necessary modules
import os, sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QToolButton, QToolBar, QDockWidget, QGridLayout, 
    QScrollArea)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QIcon, QImage, QPalette, QAction

import image_editor_functions as img

icon_path = "./icons"

# TODO: Handle png images with no background
# TODO:  paint event
# TODO: handling pen and eraser and handling drawing in the image

## the Whole UI
class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initializeUI()

        self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Image Lab")
        self.showMaximized()

        self.zoom_factor = 1

        self.createMainLabel()
        self.createMenu()
        self.createToolBar()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        # Actions for File menu
        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.triggered.connect(self.image_label.openImage)

        self.save_act = QAction(QIcon(os.path.join(icon_path, "save.png")), "Save...", self)
        self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions for Edit menu
        self.revert_act = QAction("Revert to Original", self)
        self.revert_act.triggered.connect(lambda: self.image_label.revertToOriginal())
        self.revert_act.setEnabled(True)


        self.rotate90_cw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_cw.png")),'Rotate 90º CW', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_ccw.png")),'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))


        self.flip_vertical = QAction(QIcon(os.path.join(icon_path, "flip_vertical.png")), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))

        # filteration

        self.blur_act  = QAction(QIcon(os.path.join(icon_path,"blur.png")),"Blurring",self)
        self.blur_act.triggered.connect(lambda: self.image_label.blurImage(radius=1))
        self.blur_act.setEnabled(False) # disable until finishing the funcationlity
        
        self.convert_grayscale_act = QAction(QIcon(os.path.join(icon_path,"grayscale.png")),"Black and White",self)
        self.convert_grayscale_act.triggered.connect(lambda: self.image_label.convertGrayscale())

        self.pixelation_act = QAction(QIcon(os.path.join(icon_path,"pixel.png")),"Pixelate",self)
        self.pixelation_act.triggered.connect(lambda: self.image_label.pixelateImage(pixel_size=2))
        self.blur_act.setEnabled(True)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create Photo Editor menu and add actions
        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addSeparator()

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        

        tool_menu = menu_bar.addMenu('Tools')
       
        tool_menu.addSeparator()
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_vertical)
        tool_menu.addSeparator()
        tool_menu.addAction(self.revert_act)

        trans_menu = menu_bar.addMenu("Tranformations")
        trans_menu.addAction(self.blur_act)
        trans_menu.addAction(self.convert_grayscale_act)
        trans_menu.addAction(self.pixelation_act)


    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
       
        tool_bar.addSeparator()
        
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.flip_vertical)


    def createMainLabel(self):
        """Create an instance of the imageLabel class and set it 
           as the main window's central widget."""
        self.image_label = img.ImageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)

    def updateActions(self):
        """Update the values of menu and toolbar items when an image 
        is loaded."""
        self.save_act.setEnabled(True)
        self.revert_act.setEnabled(True)


# handling esacape key: and f1 key
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())