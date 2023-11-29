import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar,QVBoxLayout,QHBoxLayout, QLabel, QInputDialog, QScrollArea, QWidget, QToolButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QImage, QAction, QColor
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
        self.create_menu_bar()
       
        self.createToolBar()

        self.show()

    def createImageCanvas(self):
    
        self.image_canvas = img.EditorFunctions(self)
        self.image_canvas.resize(self.image_canvas.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area.setWidget(self.image_canvas)
        self.setCentralWidget(self.scroll_area)
        
        self.scroll_area.setStyleSheet("background-color: #A1B5C1;")

    def create_menu_bar(self):

        menu = self.menuBar()

        self.open_act = QAction(QIcon("./icons/open.png"),'Open File', self)
        self.open_act.triggered.connect(self.image_canvas.openImage)

        self.save_act = QAction(QIcon("./icons/save.png"), "Save File", self)
        self.save_act.triggered.connect(self.image_canvas.saveImage)
        # Revert action
        self.revert_act = QAction(QIcon("./icons/revert.png"), "Undo", self)
        self.revert_act.triggered.connect(lambda: self.image_canvas.revertToOriginal())
        self.revert_act.setEnabled(True)

        file_menu = menu.addMenu("File")
        file_menu.addActions([self.open_act, self.save_act])

        undo_menu = menu.addMenu("Undo")
        undo_menu.addAction(self.revert_act)

    
    def createToolBar(self):
    
        tool_bar = QToolBar("Tools")
        tool_bar.setIconSize(QSize(60, 60))
        self.addToolBar(tool_bar)   

        # Transformation actions
        transformation_label = QLabel("Transformations")
        transformation_layout = QHBoxLayout()
        transformation_layout.addWidget(transformation_label)

        
        self.rotate_right_act = QToolButton()
        self.rotate_right_act.setIcon(QIcon("./icons/rotate_right.png"))
        self.rotate_right_act.setIconSize(QSize(30,30))
        self.rotate_right_act.setToolTip('Rotate Right')
        self.rotate_right_act.clicked.connect(lambda: self.image_canvas.rotateImage90("cw"))

        self.rotate_left_act = QToolButton()
        self.rotate_left_act.setIcon(QIcon("./icons/rotate_left.png"))
        self.rotate_left_act.setIconSize(QSize(30,30))
        self.rotate_left_act.setToolTip('Rotate Leftt')
        self.rotate_left_act.clicked.connect(lambda: self.image_canvas.rotateImage90("cw"))

    
        self.mirror_vertical = QToolButton()
        self.mirror_vertical.setIcon(QIcon("./icons/mirror_x.png"))
        self.mirror_vertical.setIconSize(QSize(30,30))
        self.mirror_vertical.setToolTip('Mirror Vertical Axis')
        self.mirror_vertical.clicked.connect(lambda: self.image_canvas.mirrorImage('horizontal'))

        self.mirror_horizontal = QToolButton()
        self.mirror_horizontal.setIcon(QIcon("./icons/mirror_y.png"))
        self.mirror_horizontal.setIconSize(QSize(30,30))
        self.mirror_horizontal.setToolTip('Mirror Horizontal Axis')
        self.mirror_horizontal.clicked.connect(lambda: self.image_canvas.mirrorImage('vertical'))

        
        transformation_layout.addWidget(self.rotate_left_act)
        transformation_layout.addWidget(self.rotate_right_act)
        transformation_layout.addWidget(self.mirror_horizontal)
        transformation_layout.addWidget(self.mirror_vertical)

        # Filter actions
        filter_label = QLabel("Filters")
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(filter_label)


        self.blur_act  = QToolButton()
        self.blur_act.setIcon(QIcon("./icons/blur.png"))
        self.blur_act.setIconSize(QSize(30,30))
        self.blur_act.setToolTip("Blurring")
        self.blur_act.clicked.connect(lambda: self.applyBlur())
        self.blur_act.setEnabled(True) # disable until finishing the funcationlity
        
        self.convert_blackwhite_act = QToolButton()
        self.convert_blackwhite_act.setIcon(QIcon("./icons/black_and_white.png"))
        self.convert_blackwhite_act.setIconSize(QSize(30,30))
        self.convert_blackwhite_act.setToolTip("Black and White")
        self.convert_blackwhite_act.clicked.connect(lambda: self.image_canvas.blackAndWhite_trans())
        
        self.pixelation_act = QToolButton()
        self.pixelation_act.setIcon(QIcon("./icons/pixelate.png"))
        self.pixelation_act.setIconSize(QSize(30,30))
        self.pixelation_act.setToolTip("Pixelate")
        self.pixelation_act.clicked.connect(lambda: self.image_canvas.pixelateImage())

        self.contrast_act = QToolButton()
        self.contrast_act.setIcon(QIcon("./icons/contrast.png"))
        self.contrast_act.setIconSize(QSize(30,30))
        self.contrast_act.setToolTip("Contrast")
        self.contrast_act.clicked.connect(lambda: self.apply_contrast())

        self.sketch_act = QToolButton()
        self.sketch_act.setIcon(QIcon("./icons/sketch.png"))
        self.sketch_act.setIconSize(QSize(30,30))
        self.sketch_act.setToolTip("Sketch")
        self.sketch_act.clicked.connect(lambda: self.image_canvas.sketch_image())
        

        self.invert_act = QToolButton()
        self.invert_act.setIcon(QIcon("./icons/invert.png"))
        self.invert_act.setIconSize(QSize(30,30))
        self.invert_act.setToolTip("Invert")
        self.invert_act.clicked.connect(lambda: self.image_canvas.invertColors())
       
        filters_layout.addWidget(self.blur_act)
        filters_layout.addWidget(self.convert_blackwhite_act)
        filters_layout.addWidget(self.pixelation_act)
        filters_layout.addWidget(self.contrast_act)
        filters_layout.addWidget(self.sketch_act)
        filters_layout.addWidget(self.invert_act)


        # Painting actions
        painting_label = QLabel("Painting")
        painting_layout = QHBoxLayout()
        painting_layout.addWidget(painting_label)

        self.paintbrush_act = QToolButton()
        self.paintbrush_act.setIcon(QIcon("./icons/brush.png"))
        self.paintbrush_act.setIconSize(QSize(30,30))
        self.paintbrush_act.setToolTip("Toggle Paintbrush")
        self.paintbrush_act.clicked.connect(lambda: self.image_canvas.togglePaintbrush())
        self.paintbrush_act.setCheckable(True)

        self.color_black_act = QToolButton()
        self.color_black_act.setIcon(QIcon("./icons/color_black.png"))
        self.color_black_act.setIconSize(QSize(30,30))
        self.color_black_act.setToolTip("Black")
        self.color_black_act.clicked.connect(lambda: self.set_color("black"))
        self.color_black_act.setCheckable(True)
        self.color_black_act.setChecked(True)

        self.color_white_act = QToolButton()
        self.color_white_act.setIcon(QIcon("./icons/color_white.png"))
        self.color_white_act.setIconSize(QSize(30,30))
        self.color_white_act.setToolTip("White")
        self.color_white_act.clicked.connect(lambda: self.set_color("white"))
        self.color_white_act.setCheckable(True)
        
        self.color_red_act = QToolButton()
        self.color_red_act.setIcon(QIcon("./icons/color_red.png"))
        self.color_red_act.setIconSize(QSize(30,30))
        self.color_red_act.setToolTip("Red")
        self.color_red_act.clicked.connect(lambda: self.set_color("red"))
        self.color_red_act.setCheckable(True)
        
        self.color_blue_act = QToolButton()
        self.color_blue_act.setIcon(QIcon("./icons/color_blue.png"))
        self.color_blue_act.setIconSize(QSize(30,30))
        self.color_blue_act.setToolTip("Blue")
        self.color_blue_act.clicked.connect(lambda: self.set_color("blue"))
        self.color_blue_act.setCheckable(True)

        self.color_green_act = QToolButton()
        self.color_green_act.setIcon(QIcon("./icons/color_green.png"))
        self.color_green_act.setIconSize(QSize(30,30))
        self.color_green_act.setToolTip("Black")
        self.color_green_act.clicked.connect(lambda: self.set_color("green"))
        self.color_green_act.setCheckable(True)

        painting_layout.addWidget(self.paintbrush_act)
        painting_layout.addWidget(self.color_black_act)
        painting_layout.addWidget(self.color_white_act)
        painting_layout.addWidget(self.color_red_act)
        painting_layout.addWidget(self.color_blue_act)
        painting_layout.addWidget(self.color_green_act)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addLayout(transformation_layout)
        container_layout.addLayout(filters_layout)
        container_layout.addLayout(painting_layout)

        tool_bar.addWidget(container)
        
        tool_bar.setStyleSheet("background-color: #EEEDF0;")


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
    
    def set_color(self,colorName):
        color = QColor(colorName)
        self.image_canvas.paintColor = color
        for coloract in self.colors:
            if coloract.iconText().lower() != colorName:
                coloract.setChecked(False)
   
# handling esacape key: and f1 key
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())