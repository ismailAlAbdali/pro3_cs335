# Import necessary modules
import os, sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QToolButton, QToolBar, QDockWidget, QMessageBox, QFileDialog, QGridLayout, 
    QScrollArea, QSizePolicy, QRubberBand)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QIcon, QPixmap, QImage, QTransform, QPalette, QAction

icon_path = "icons"

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
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.zoom_factor = 1

        self.createMainLabel()
        self.createEditingBar()
        self.createMenu()
        self.createToolBar()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        # Actions for Photo Editor menu
        about_act = QAction('About', self)
        about_act.triggered.connect(self.aboutDialog)

        self.exit_act = QAction(QIcon(os.path.join(icon_path, "exit.png")), 'Quit Photo Editor', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Actions for File menu
        self.new_act = QAction(QIcon(os.path.join(icon_path, "new.png")), 'New...')

        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.image_label.openImage)

        self.print_act = QAction(QIcon(os.path.join(icon_path, "print.png")), "Print...", self)
        self.print_act.setShortcut('Ctrl+P')
        #self.print_act.triggered.connect(self.printImage)
        self.print_act.setEnabled(False)

        self.save_act = QAction(QIcon(os.path.join(icon_path, "save.png")), "Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions for Edit menu
        self.revert_act = QAction("Revert to Original", self)
        self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions for Tools menu
        self.crop_act = QAction(QIcon(os.path.join(icon_path, "crop.png")), "Crop", self)
        self.crop_act.setShortcut('Shift+X')
        self.crop_act.triggered.connect(self.image_label.cropImage)

        self.resize_act = QAction(QIcon(os.path.join(icon_path, "resize.png")), "Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        self.resize_act.triggered.connect(self.image_label.resizeImage)

        self.rotate90_cw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_cw.png")),'Rotate 90º CW', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_ccw.png")),'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))

        self.flip_horizontal = QAction(QIcon(os.path.join(icon_path, "flip_horizontal.png")), 'Flip Horizontal', self)
        self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))

        self.flip_vertical = QAction(QIcon(os.path.join(icon_path, "flip_vertical.png")), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create Photo Editor menu and add actions
        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.print_act)

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.revert_act)

        tool_menu = menu_bar.addMenu('Tools')
        tool_menu.addAction(self.crop_act)
        tool_menu.addAction(self.resize_act)
        tool_menu.addSeparator()
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)

        views_menu = menu_bar.addMenu('Views')
        views_menu.addAction(self.tools_menu_act)

    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.print_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.crop_act)
        tool_bar.addAction(self.resize_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)


    ## we are going to edit this in order to make the Pen and Eraser
    def createEditingBar(self):
        """Create dock widget for editing tools."""
        #TODO: Add a tab widget for the different editing tools
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

        # Create editing tool buttons
        filters_label = QLabel("Filters")

        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "grayscale.png")))
        convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        convert_to_RGB = QToolButton()
        convert_to_RGB.setIcon(QIcon(os.path.join(icon_path, "rgb.png")))
        convert_to_RGB.clicked.connect(self.image_label.convertToRGB)

        # Set layout for dock widget
        editing_grid = QGridLayout()
        editing_grid.addWidget(convert_to_grayscale, 1, 0)
        editing_grid.addWidget(convert_to_RGB, 1, 1)
        
        editing_grid.setRowStretch(7, 10)

        container = QWidget()
        container.setLayout(editing_grid)

        self.editing_bar.setWidget(container)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.editing_bar)

        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def createMainLabel(self):
        """Create an instance of the imageLabel class and set it 
           as the main window's central widget."""
        self.image_label = imageLabel(self)
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
        
    
    def zoomOnImage(self, zoom_value):
        """Zoom in and zoom out."""
        self.zoom_factor *= zoom_value
        self.image_label.resize(self.zoom_factor * self.image_label.pixmap().size())

        self.adjustScrollBar(self.scroll_area.horizontalScrollBar(), zoom_value)
        self.adjustScrollBar(self.scroll_area.verticalScrollBar(), zoom_value)


    def normalSize(self):
        """View image with its normal dimensions."""
        self.image_label.adjustSize()
        self.zoom_factor = 1.0

    def adjustScrollBar(self, scroll_bar, value):
        """Adjust the scrollbar when zooming in or out."""
        scroll_bar.setValue(float(value * scroll_bar.value()) + ((value - 1) * scroll_bar.pageStep()/2))


# handling esacape key: and f1 key
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorGUI()
    sys.exit(app.exec())