import cv2 
import numpy as np

from PyQt6.QtWidgets import QLabel, QMessageBox, QFileDialog, QSizePolicy, QRubberBand
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPixmap, QImage, QTransform

class EditorFunctions(QLabel):
   
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
    
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        
        if image_file:
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
       
        if self.image.isNull() == False:
            self.image = self.original_image
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()
        else:
            pass


    def rotateImage90(self, direction):
        
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

   
    # Image blurring
    def blurImageOpenCV(self, blur_strength):
        if not self.image.isNull():
            # Ensure the image is in a format that uses 4 bytes per pixel
            image_format = QImage.Format.Format_ARGB32
            converted_image = self.image.convertToFormat(image_format)

            # Convert QImage to OpenCV format
            width = converted_image.width()
            height = converted_image.height()
            ptr = converted_image.bits()
            ptr.setsize(converted_image.sizeInBytes())
            arr = np.array(ptr).reshape((height, width, 4))

            # Apply blur using OpenCV
            # Ensure blur_strength is odd
            blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
            blurred = cv2.GaussianBlur(arr, (blur_strength, blur_strength), 0)

            # Convert back to QImage
            blurred_image = QImage(blurred.data, blurred.shape[1], blurred.shape[0], image_format)
            self.image = blurred_image
            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()

        else:
            QMessageBox.information(self, "Error", "No image to blur.", QMessageBox.standardButton.Ok)

    # grayscale image trasformation
    def convertBlackWhite(self):
        if self.image.isNull() == False:
            temp_converted_img = self.image.convertToFormat(QImage.Format.Format_Grayscale16)
            self.image = QImage(temp_converted_img)
            self.setPixmap(QPixmap().fromImage(temp_converted_img))
            self.repaint()

    # adding pixelation
    def pixelateImage(self, pixel_size):
        if not self.image.isNull() and pixel_size > 0:
            original_size = self.image.size()
            # Scale down the image to create the pixelated effect
            small = self.image.scaled(original_size.width() // pixel_size,
                                      original_size.height() // pixel_size,
                                      Qt.AspectRatioMode.IgnoreAspectRatio,
                                      Qt.TransformationMode.FastTransformation)
            # Scale it back up to its original size
            pixelated = small.scaled(original_size,
                                     Qt.AspectRatioMode.IgnoreAspectRatio,
                                     Qt.TransformationMode.FastTransformation)
            self.image = pixelated
            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()

    def mousePressEvent(self, event):   
    
        self.origin = event.pos()
        if not(self.rubber_band):
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

        print(self.rubber_band.x())

    def mouseMoveEvent(self, event):
        
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):

        self.rubber_band.hide()