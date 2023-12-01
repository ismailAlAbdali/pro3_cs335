import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar,QHBoxLayout, QLabel, QInputDialog, QScrollArea, QWidget, QToolButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QImage, QAction, QColor
import image_editor_functions as img

'''
This class represents the application window that is shown to the user
through QMainWindow object
'''
class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.init_UI() # initialize the user interface

        self.image = QImage() # create an image object for image processing

    '''
    This method creates the user interface of the application. 
    It sets the minimum size of the application
    This method also displays the image scroll area, menu and toolbars
    '''
    def init_UI(self):

        self.setMinimumSize(500, 500) # minimum dimensions when not full screen
        self.setWindowTitle("Image Lab") 
        self.showMaximized() # initially show the window in full screen
        
       
        self.create_image_canvas() # create the widget where the image will be displayed
        self.create_menu_bar() # create a menu bar for file options (opening, saving, reverting)
       
        self.create_tool_bar() # create a toolbar where editor features will be displayed

        self.show() # show the UI

    '''
    This method creates an area where the image will be displayed in the form of scroll area
    and a pixmap
    '''
    def create_image_canvas(self):
    
        self.image_canvas = img.EditorFunctions(self) # create instance of editing features to allow image manipulation
        self.image_canvas.resize(self.image_canvas.pixmap().size()) # create a pixmap the size of the image

        self.scroll_area = QScrollArea() # create a scroll area widget; if images are big then user can scroll 
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter) # set scroll area alignment to center of area
        
        self.scroll_area.setWidget(self.image_canvas) # set the image canvas as widget on the scroll area
        self.setCentralWidget(self.scroll_area) # make the canvas center of the window
        
        self.scroll_area.setStyleSheet("background-color: #A1B5C1;") 

    '''
    This method creates an menu bar on the window where file operation can be performed
    Options are File opening, saving, and reverting changes
    '''
    def create_menu_bar(self):

        menu = self.menuBar() # create a menu bar

        # create action for opening a file
        self.open_act = QAction(QIcon("./icons/open.png"),'Open File', self)
        self.open_act.triggered.connect(self.image_canvas.open_image)

        # create action for saving a file
        self.save_act = QAction(QIcon("./icons/save.png"), "Save File", self)
        self.save_act.triggered.connect(self.image_canvas.save_image)
       
        # create action for revering changes on an image
        self.revert_act = QAction(QIcon("./icons/revert.png"), "Revert", self)
        self.revert_act.triggered.connect(lambda: self.image_canvas.revert_original())
        self.revert_act.setEnabled(True)

        # create action for exting the application
        self.close_act = QAction(QIcon("./icons/close.png"), "Close", self)
        self.close_act.triggered.connect(lambda: self.close())

        # add options to file menu
        file_menu = menu.addMenu("File")
        file_menu.addActions([self.open_act, self.save_act, self.close_act])

        # add revert action to editing menu
        editing_menu = menu.addMenu("Edit")
        editing_menu.addAction(self.revert_act)

    '''
    This method creates a tool bar that contains actions for image processing
    Buttons exist for every feature that can be applied to the image
    '''
    def create_tool_bar(self):
        self.colors = []

        # Create toolbar and set icon sizes
        tool_bar = QToolBar("Tools")
        tool_bar.setIconSize(QSize(60, 60))
        self.addToolBar(tool_bar)   

        # Transformation actions
        transformation_label = QLabel("Transformations")
        transformation_layout = QHBoxLayout()
        transformation_layout.addWidget(transformation_label)

        # Create button for rotating right
        self.rotate_right_act = QToolButton()
        self.rotate_right_act.setIcon(QIcon("./icons/rotate_right.png"))
        self.rotate_right_act.setIconSize(QSize(30,30))
        self.rotate_right_act.setToolTip('Rotate Right')
        self.rotate_right_act.clicked.connect(lambda: self.image_canvas.rotate_image("right"))

        # Create button for rotating left
        self.rotate_left_act = QToolButton()
        self.rotate_left_act.setIcon(QIcon("./icons/rotate_left.png"))
        self.rotate_left_act.setIconSize(QSize(30,30))
        self.rotate_left_act.setToolTip('Rotate Left')
        self.rotate_left_act.clicked.connect(lambda: self.image_canvas.rotate_image("left"))

        # Create button for mirroring vertical
        self.mirror_vertical = QToolButton()
        self.mirror_vertical.setIcon(QIcon("./icons/mirror_x.png"))
        self.mirror_vertical.setIconSize(QSize(30,30))
        self.mirror_vertical.setToolTip('Mirror Vertical Axis')
        self.mirror_vertical.clicked.connect(lambda: self.image_canvas.mirror_image("horizontal"))

        # Create button for mirroring horizontal
        self.mirror_horizontal = QToolButton()
        self.mirror_horizontal.setIcon(QIcon("./icons/mirror_y.png"))
        self.mirror_horizontal.setIconSize(QSize(30,30))
        self.mirror_horizontal.setToolTip('Mirror Horizontal Axis')
        self.mirror_horizontal.clicked.connect(lambda: self.image_canvas.mirror_image("vertical"))

        # Add button widgets to tool bar
        transformation_layout.addWidget(self.rotate_left_act)
        transformation_layout.addWidget(self.rotate_right_act)
        transformation_layout.addWidget(self.mirror_horizontal)
        transformation_layout.addWidget(self.mirror_vertical)


        # Filter actions
        filter_label = QLabel("Filters")
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(filter_label)


        # Create button for blurring the image
        self.blur_act  = QToolButton()
        self.blur_act.setIcon(QIcon("./icons/blur.png"))
        self.blur_act.setIconSize(QSize(30,30))
        self.blur_act.setToolTip("Blurring")
        self.blur_act.clicked.connect(lambda: self.apply_blur_effect())
        self.blur_act.setEnabled(True)
        
        # Create button for converting image to black and white 
        self.convert_blackwhite_act = QToolButton()
        self.convert_blackwhite_act.setIcon(QIcon("./icons/black_and_white.png"))
        self.convert_blackwhite_act.setIconSize(QSize(30,30))
        self.convert_blackwhite_act.setToolTip("Black and White")
        self.convert_blackwhite_act.clicked.connect(lambda: self.image_canvas.black_white_image())
        
        # Create button for applying pixelation to the image
        self.pixelation_act = QToolButton()
        self.pixelation_act.setIcon(QIcon("./icons/pixelate.png"))
        self.pixelation_act.setIconSize(QSize(30,30))
        self.pixelation_act.setToolTip("Pixelate")
        self.pixelation_act.clicked.connect(lambda: self.apply_pixelation_effect())

        # Create button for modifying contrast of the image
        self.contrast_act = QToolButton()
        self.contrast_act.setIcon(QIcon("./icons/contrast.png"))
        self.contrast_act.setIconSize(QSize(30,30))
        self.contrast_act.setToolTip("Contrast")
        self.contrast_act.clicked.connect(lambda: self.apply_contrast_effect())
        
        # Create button for applying sketch filter to the image
        self.sketch_act = QToolButton()
        self.sketch_act.setIcon(QIcon("./icons/sketch.png"))
        self.sketch_act.setIconSize(QSize(30,30))
        self.sketch_act.setToolTip("Sketch")
        self.sketch_act.clicked.connect(lambda: self.image_canvas.sketch_image())
        
        # Create button for inverting the colors of the image
        self.invert_act = QToolButton()
        self.invert_act.setIcon(QIcon("./icons/invert.png"))
        self.invert_act.setIconSize(QSize(30,30))
        self.invert_act.setToolTip("Invert")
        self.invert_act.clicked.connect(lambda: self.image_canvas.invert_colors_image())
       
        # Add button widgets to toolbar
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

        # Create button for the paintbrush
        self.paintbrush_act = QToolButton()
        self.paintbrush_act.setIcon(QIcon("./icons/brush.png"))
        self.paintbrush_act.setIconSize(QSize(30,30))
        self.paintbrush_act.setToolTip("Toggle Paintbrush")
        self.paintbrush_act.clicked.connect(lambda: self.image_canvas.togglePaintbrush())
        self.paintbrush_act.setCheckable(True)

        # Create button for paintbrush color black
        self.color_black_act = QToolButton()
        self.color_black_act.setIcon(QIcon("./icons/color_black.png"))
        self.color_black_act.setIconSize(QSize(30,30))
        self.color_black_act.setToolTip("Black")
        self.color_black_act.clicked.connect(lambda: self.set_color("black"))
        self.color_black_act.setCheckable(True)
        self.color_black_act.setChecked(True)

        # Create button for paintbrush color white
        self.color_white_act = QToolButton()
        self.color_white_act.setIcon(QIcon("./icons/color_white.png"))
        self.color_white_act.setIconSize(QSize(30,30))
        self.color_white_act.setToolTip("White")
        self.color_white_act.clicked.connect(lambda: self.set_color("white"))
        self.color_white_act.setCheckable(True)
        
        # Create button for paintbrush color red
        self.color_red_act = QToolButton()
        self.color_red_act.setIcon(QIcon("./icons/color_red.png"))
        self.color_red_act.setIconSize(QSize(30,30))
        self.color_red_act.setToolTip("Red")
        self.color_red_act.clicked.connect(lambda: self.set_color("red"))
        self.color_red_act.setCheckable(True)
        
        # Create button for paintbrush color blue
        self.color_blue_act = QToolButton()
        self.color_blue_act.setIcon(QIcon("./icons/color_blue.png"))
        self.color_blue_act.setIconSize(QSize(30,30))
        self.color_blue_act.setToolTip("Blue")
        self.color_blue_act.clicked.connect(lambda: self.set_color("blue"))
        self.color_blue_act.setCheckable(True)

        # Create button for paintbrush color green
        self.color_green_act = QToolButton()
        self.color_green_act.setIcon(QIcon("./icons/color_green.png"))
        self.color_green_act.setIconSize(QSize(30,30))
        self.color_green_act.setToolTip("Black")
        self.color_green_act.clicked.connect(lambda: self.set_color("green"))
        self.color_green_act.setCheckable(True)

        # for fixing the coloring checking
        self.colors.extend([self.color_black_act,self.color_white_act,self.color_red_act,self.color_blue_act,self.color_green_act])

        # Add painting widgets to toolbar
        painting_layout.addWidget(self.paintbrush_act)
        painting_layout.addWidget(self.color_black_act)
        painting_layout.addWidget(self.color_white_act)
        painting_layout.addWidget(self.color_red_act)
        painting_layout.addWidget(self.color_blue_act)
        painting_layout.addWidget(self.color_green_act)

        # Create container widget to hold all toolbar layout
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addLayout(transformation_layout)
        container_layout.addLayout(filters_layout)
        container_layout.addLayout(painting_layout)

        tool_bar.addWidget(container)
        
        tool_bar.setStyleSheet("background-color: #EEEDF0;")

    '''
    This method creates a dialog button that allows the user to apply blurring
    Allows the strength to be set in a integer range between 1 and 50
    '''
    def apply_blur_effect(self):
        blur_strength, ok_pressed = QInputDialog.getInt(self, "Set Blur Strength", 
                                                        "Strength (min: 1 max: 50):", 5, 1, 50, 1)
        if ok_pressed:
            self.image_canvas.blur_image(blur_strength) 

    '''
    This method creates a dialog that allows the user to apply pixelation
    Allows the pixel size to be set in a integer range between 1 and 100
    '''
    def apply_pixelation_effect(self):
        pixel_size, ok_pressed = QInputDialog.getInt(self, "Pixelate Image",
                                                     "Pixel Size (min: 1 max: 100):", 10, 1, 100, 1)
        if ok_pressed:
            self.image_canvas.pixelate_image(pixel_size)

    '''
    This method creates a dialog that allows the user to apply contrast
    Allows the contrast level to be set in a integer range between -255 and 255
    '''
    def apply_contrast_effect(self):
        contrast_level, ok_pressed = QInputDialog.getInt(self, "Adjust Contrast",
                                                         "Contrast Level (min: -255 max: 255):", 0, -255, 255, 1)
        if ok_pressed:
            self.image_canvas.adjust_contrast_image(contrast_level)
    
    # adding colors acts
    def set_color(self,colorName):
        color = QColor(colorName)
        self.image_canvas.paint_color = color
        for coloract in self.colors:
            if str.lower(coloract.toolTip()) != colorName:
                coloract.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())