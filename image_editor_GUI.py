# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QInputDialog, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QImage, QPalette, QAction
import image_editor_functions as img

## the Whole UI
class PhotoEditorGUI(QMainWindow):
    
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
        
         # Create menubar
        menu_bar = self.menuBar()
        
        # Actions for File menu
        self.open_act = QAction(QIcon("./icons/open.png"),'Open...', self)
        self.open_act.triggered.connect(self.image_canvas.openImage)

        self.save_act = QAction(QIcon("./icons/save.png"), "Save...", self)
        self.save_act.triggered.connect(self.image_canvas.saveImage)
        self.save_act.setEnabled(True)


        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        
        file_menu.addActions([self.open_act, self.save_act])


    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Revert action
        self.revert_act = QAction("Revert to Original", self)
        self.revert_act.triggered.connect(lambda: self.image_canvas.revertToOriginal())
        self.revert_act.setEnabled(True)

        # Transformation actions
        self.rotate90_cw_act = QAction(QIcon("./icons/rotate90_cw.png"),'Rotate 90º CW', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_canvas.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon("./icons/rotate90_ccw.png"),'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_canvas.rotateImage90("ccw"))

        self.flip_vertical = QAction(QIcon("./icons/flip_vertical.png"), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.image_canvas.flipImage('horizontal'))

        # Filter actions
        self.blur_act  = QAction(QIcon("./icons/blur.png"),"Blurring",self)
        self.blur_act.triggered.connect(lambda: self.applyBlur())
        self.blur_act.setEnabled(True) # disable until finishing the funcationlity
        
        self.convert_blackwhite_act = QAction(QIcon("./icons/grayscale.png"),"Black and White",self)
        self.convert_blackwhite_act.triggered.connect(lambda: self.image_canvas.blackAndWhite_trans())

        self.pixelation_act = QAction(QIcon("./icons/pixel.png"),"Pixelate",self)
        self.pixelation_act.triggered.connect(lambda: self.apply_pixelation()) # pixel_size 2 default value

        self.paintbrush_act = QAction("Toggle Paintbrush",self)
        self.paintbrush_act.triggered.connect(lambda: self.image_canvas.togglePaintbrush())
        
        tool_bar.addActions([self.open_act,self.save_act])
        tool_bar.addSeparator()
        tool_bar.addActions([self.rotate90_ccw_act, self.rotate90_cw_act, self.revert_act, self.flip_vertical, self.blur_act, self.convert_blackwhite_act, self.pixelation_act,
                             self.paintbrush_act])


    def applyBlur(self):
        blur_strength, ok_pressed = QInputDialog.getInt(self, "Set Blur Strength", 
                                                        "Strength:", 5, 1, 50, 1)
        if ok_pressed:
            self.image_canvas.blurImageOpenCV(blur_strength) 

    def apply_pixelation(self):
        pixel_size, ok_pressed = QInputDialog.getInt(self, "Pixelate Image",
                                                     "Pixel Size:", 10, 1, 100, 1)
        if ok_pressed:
            self.image_canvas.pixelateImage(pixel_size)

# handling esacape key: and f1 key
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())