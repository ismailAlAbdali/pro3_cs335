import cv2 
import numpy as np

from PyQt6.QtWidgets import QLabel, QMessageBox, QFileDialog, QSizePolicy, QRubberBand
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
from PyQt6.QtGui import QPixmap, QImage, QTransform, QColor
from statistics import median


# from PyQt6.QtGui import QImage, QPainter, QImageBlurFilter, QPen # for blurring
class EditorFunctions(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent 
        self.image = QImage()

        self.original_image = self.image

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)

        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setScaledContents(True)
        
        self.paintMode = False # if true, draw pen on image instead of rubber_band
        self.prevPaintLoc = None
        # Load image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def openImage(self):
        """Load a new image into the """
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
                "Unable to open image.", QMessageBox.StandardButton.Ok)
    
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
                    "Unable to save image.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Empty Image", 
                    "There is no image to save.", QMessageBox.StandardButton.Ok)

    def revertToOriginal(self):
        """Revert the image back to original image."""
        if self.image.isNull() == False:
            self.image = self.original_image
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()
        else:
            pass


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

    ## make image blurring

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
            QMessageBox.information(self, "Error", "No image to blur.", QMessageBox.StandardButton.Ok)

    # grayscale image trasformation
    def blackAndWhite_trans(self):
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

    #uses algorithm from https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
    def adjustContrast(self,contrast_level):
        if not self.image.isNull():
            contrastFactor = (259*(contrast_level + 255))/(255*(259 - contrast_level))
            for i in range(self.image.width()):
                for j in range(self.image.height()):
                    newColor = self.image.pixelColor(i,j)
                    newColor.setRed(int(round(median([0,(contrastFactor*(newColor.red() -128) + 128),255]),0)))
                    newColor.setBlue(int(round(median([0,(contrastFactor*(newColor.blue() -128) + 128),255]),0)))
                    newColor.setGreen(int(round(median([0,(contrastFactor*(newColor.green() -128) + 128),255]),0)))
                    self.image.setPixelColor(i,j,newColor)
            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()

    def paintPixels(self,origin,brush_size=3,color=QColor("black")):
        #store all pixels in set, then paint them to ensure no duplicates
        pixelsToPaint = set()
        #paint around origin in radius of brush_size
        for x in range(brush_size):
            for y in range(brush_size):
                pixelsToPaint.add(QPoint(origin.x() + x, origin.y() + y))
        #when mouse is held, draw a line between a point and the previous point from last call to function
        if self.prevPaintLoc != None and self.prevPaintLoc != origin:
            line_x = origin.x() - self.prevPaintLoc.x()
            line_y = origin.y() - self.prevPaintLoc.y()
            distance = (line_x**2 + line_y**2) ** (1/2)
            step_x = line_x/distance
            step_y = line_y/distance
            for i in range(int(round(distance))):
                for x in range(brush_size):
                    for y in range(brush_size):
                        pixelsToPaint.add(QPoint(self.prevPaintLoc.x() + x + int(round((i*step_x))), self.prevPaintLoc.y() + y + int(round((i*step_y))) ))
        for point in pixelsToPaint:
            self.image.setPixelColor(point,color)
        self.prevPaintLoc = origin
        self.setPixmap(QPixmap.fromImage(self.image))
        self.repaint()

    def togglePaintbrush(self):
        self.paintMode = not self.paintMode
        self.prevPaintLoc = None

    def mousePressEvent(self, event):   
        """Handle mouse press event."""
        self.origin = event.pos()
        if not self.paintMode:
            if not(self.rubber_band):
                self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        elif self.paintMode:
            self.paintPixels(self.origin)

        #print(self.rubber_band.height())
        print(self.rubber_band.x())

    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        if self.paintMode:
            self.paintPixels(event.pos())

    def mouseReleaseEvent(self, event):
        """Handle when the mouse is released."""
        self.rubber_band.hide()
        self.prevPaintLoc = None
