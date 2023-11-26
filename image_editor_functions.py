from PyQt6.QtWidgets import QLabel, QMessageBox, QFileDialog, QSizePolicy, QRubberBand
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPixmap, QImage, QTransform

class ImageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent 
        self.image = QImage()

        self.original_image = self.image

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)

        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setScaledContents(True)

        # Load image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def openImage(self):
        """Load a new image into the """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        
        if image_file:
            # Reset values when opening an image
            self.parent.zoom_factor = 1
            #self.parent.scroll_area.setVisible(True)
            self.parent.print_act.setEnabled(True)
            self.parent.updateActions()

            # Reset all sliders
            self.parent.brightness_slider.setValue(0)

            # Get image format
            self.image = QImage(image_file)
            self.original_image = self.image.copy()

            self.setPixmap(QPixmap().fromImage(self.image))
          
            self.resize(self.pixmap().size())

        elif image_file == "":
            # User selected Cancel
            pass
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.standardButton.Ok)
    
    def saveImage(self):
        """Save the image displayed in the label."""
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                    GIF Files (*.gif)")

            if image_file and self.image.isNull() == False:
                self.image.save(image_file)
            else:
                QMessageBox.information(self, "Error", 
                    "Unable to save image.", QMessageBox.standardButton.Ok)
        else:
            QMessageBox.information(self, "Empty Image", 
                    "There is no image to save.", QMessageBox.standardButton.Ok)

    def revertToOriginal(self):
        """Revert the image back to original image."""
        self.image = self.original_image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()


    def resizeImage(self):
        """Resize image."""
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)

            pixmap = QPixmap(self.image)

            resized_image = pixmap.transformed(resize, mode=Qt.TransformationMode.SmoothTransformation)

            self.image = QImage(resized_image) 
            self.setPixmap(resized_image)
            
            self.setScaledContents(True)
            self.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def cropImage(self):
        """Crop selected portions in the image."""
        if self.image.isNull() == False:
            rect = QRect(10, 20, 400, 200)
            original_image = self.image
            cropped = original_image.copy(rect)

            self.image = QImage(cropped)
            self.setPixmap(QPixmap().fromImage(cropped))

    def rotateImage90(self, direction):
        """Rotate image 90º clockwise or counterclockwise."""
        if self.image.isNull() == False:
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)


            rotated = pixmap.transformed(transform90, mode=Qt.TransformationMode.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())
           
            self.image = QImage(rotated) 
        
            self.setPixmap(rotated.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            self.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def flipImage(self, axis):
        """
        Mirror the image across the horizontal axis.
        """
        if self.image.isNull() == False:
            if axis == "horizontal":
                flip_h = QTransform().scale(-1, 1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_h)
            elif axis == "vertical":
                flip_v = QTransform().scale(1, -1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_v)

            self.image = QImage(flipped)
            self.setPixmap(flipped)
            
            self.repaint()
        else:
            # No image to flip
            pass

    def convertToGray(self):
        """Convert image to grayscale."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format.Format_Grayscale16)
            
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToRGB(self):
        """Convert image to RGB format."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format.Format_RGB16)
           
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()
   

    def mousePressEvent(self, event):   
        """Handle mouse press event."""
        self.origin = event.pos()
        if not(self.rubber_band):
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

        #print(self.rubber_band.height())
        print(self.rubber_band.x())

    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        """Handle when the mouse is released."""
        self.rubber_band.hide()