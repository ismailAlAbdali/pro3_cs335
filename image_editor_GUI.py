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
        
        self.scroll_area.setStyleSheet("background-color: #333333;")

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

        menu_bar.setStyleSheet("background-color: #ffffff;")

    def createToolBar(self):
    
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(50, 50))
        self.addToolBar(tool_bar)

        # Revert action
        self.revert_act = QAction(QIcon("./icons/revert.png"),"Revert to Original", self)
        self.revert_act.triggered.connect(lambda: self.image_canvas.revertToOriginal())
        self.revert_act.setEnabled(True)

        # Transformation actions
        self.rotate_right_act = QAction(QIcon("./icons/rotate_right.png"),'Rotate Right', self)
        self.rotate_right_act.triggered.connect(lambda: self.image_canvas.rotateImage90("cw"))

        self.rotate_left_act = QAction(QIcon("./icons/rotate_left.png"),'Rotate Left', self)
        self.rotate_left_act.triggered.connect(lambda: self.image_canvas.rotateImage90("ccw"))

        self.mirror_vertical = QAction(QIcon("./icons/mirror_x.png"), 'Mirror Vertical Axis', self)
        self.mirror_vertical.triggered.connect(lambda: self.image_canvas.mirrorImage('horizontal'))

        self.mirror_horizontal = QAction(QIcon("./icons/mirror_y.png"), 'Mirror Horizontal Axis', self)
        self.mirror_horizontal.triggered.connect(lambda: self.image_canvas.mirrorImage('vertical'))


        # Filter actions
        self.blur_act  = QAction(QIcon("./icons/blur.png"),"Blurring",self)
        self.blur_act.triggered.connect(lambda: self.applyBlur())
        self.blur_act.setEnabled(True) # disable until finishing the funcationlity
        
        self.convert_blackwhite_act = QAction(QIcon("./icons/black_and_white.png"),"Black and White",self)
        self.convert_blackwhite_act.triggered.connect(lambda: self.image_canvas.blackAndWhite_trans())

        self.pixelation_act = QAction(QIcon("./icons/pixelate.png"),"Pixelate",self)
        self.pixelation_act.triggered.connect(lambda: self.apply_pixelation()) # pixel_size 2 default value

        self.contrast_act = QAction(QIcon("./icons/contrast.png"),"Contrast",self)
        self.contrast_act.triggered.connect(lambda: self.apply_contrast())

        self.paintbrush_act = QAction(QIcon("./icons/brush.png"),"Toggle Paintbrush",self)
        self.paintbrush_act.triggered.connect(lambda: self.image_canvas.togglePaintbrush())
        self.paintbrush_act.setCheckable(True)

        self.sketch_act = QAction(QIcon("./icons/sketch.png"), "Sketch", self)
        self.sketch_act.triggered.connect(lambda: self.image_canvas.sketch_image())

        
        self.invert_act = QAction(QIcon("./icons/sketch.png"), "Sketch", self)
        self.invert_act.triggered.connect(lambda: self.image_canvas.invertColors())
        
        tool_bar.addActions([self.open_act,self.save_act])
        tool_bar.addSeparator()
        tool_bar.addActions([self.rotate_left_act, self.rotate_right_act, self.revert_act, self.mirror_horizontal,self.mirror_vertical,self.convert_blackwhite_act])
        tool_bar.addSeparator()
        tool_bar.addActions([self.blur_act,  self.pixelation_act, self.contrast_act, self.sketch_act])
        tool_bar.addSeparator()
        tool_bar.addActions([self.paintbrush_act])
        tool_bar.setStyleSheet("background-color: #555555;")


    def applyBlur(self):
        blur_strength, ok_pressed = QInputDialog.getInt(self, "Set Blur Strength", 
                                                        "Strength:", 5, 1, 50, 1)
        if ok_pressed:
            self.image_canvas.blurImageOpenCV(blur_strength) 

    def apply_pixelation(self):
        pixel_size, ok_pressed = QInputDialog.getInt(self, "Pixelate Image",
                                                     "Pixel Size", 10, 1, 100, 1)
        if ok_pressed:
            self.image_canvas.pixelateImage(pixel_size)

    def apply_contrast(self):
        contrast_level, ok_pressed = QInputDialog.getInt(self, "Adjust Contrast",
                                                         "Contrast Level:", 0, -255, 255, 1)
        if ok_pressed:
            self.image_canvas.adjustContrast(contrast_level)
    
   
# handling esacape key: and f1 key
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())