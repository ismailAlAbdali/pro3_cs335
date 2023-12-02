from PyQt6.QtWidgets import QLabel, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QImage, QTransform, QColor
from statistics import median
import cv2 
import numpy as np

'''
This class represents the various functionalities of the image editor
Has three different categories of image editing features:
    * Transformations
    * Filters/Effects
    * Painting
'''
class EditorFunctions(QLabel):
   
    def __init__(self, parent, image=None):
        
        super().__init__(parent)
        self.parent = parent 
        self.image = QImage() # create image object to apply image processing techniques

        self.initial_image = self.image # store the initial version of the image for reverting purposes
        
        self.paint_mode = False # if true, draw pen on image instead of rubber_band
        self.prev_paint_loc = None # store location of last pixel painted

        self.paint_color = QColor("black") # setup paint color black as default

        # Load image onto canvas as a pixmap
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    '''
    This method allows the user to open an image file onto the image canvas
    Allows various file types in the dialog
    '''
    def open_image(self):
        # dialog to open file
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp)")
        
        # if an image file was selected
        if image_file:
            # Get image format
            self.image = QImage(image_file)
            self.initial_image = self.image.copy() # copy the initial image for reverting purposes

            # Set the image on the image canvas
            self.setPixmap(QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

        # if no image was selected
        elif image_file == "":
            # ignore
            pass
        # if an invalid file type or corrupted image
        else:
            self.errorMessage("Cannot open image.")
    
    '''
    This method allows the user to save the image they edited
    By default saves as .png but can save as other file types
    '''
    def save_image(self):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp)")

            # if there is an image on the canvas and we have an image to save
            if image_file and self.image.isNull() == False:
                self.image.save(image_file) # save the image
            # otherwise we cannot save
            else:
                self.errorMessage("Cannot save image.")
        # if there is no image on the canvas
        else:
            self.errorMessage("There is no image to save.",error="Save Not Needed")

    '''
    This method reverts the image on the canvas back to the original
    Acts as an undo button; replaces image on canvas with the initial image
    '''
    def revert_original(self):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            self.image = self.initial_image # replace image on canvas with original

            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()
        # there is no image to revert
        else:
            self.errorMessage("no image to revert")

    '''
    This method rotates the image by 90 degrees to the left or right
    Relative to the x-axis
    '''
    # concept drawn from reference: https://doc.qt.io/qt-6/qtransform.html
    def rotate_image(self, direction):
        # if there is an imagfe on the canvas
        if self.image.isNull() == False:
            if direction == "right": # rotate to the right
                rotate = QTransform().rotate(90)
            elif direction == "left": # rotate to the left
                rotate = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(rotate, mode=Qt.TransformationMode.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())
           
            self.image = QImage(rotated) 
        
            self.setPixmap(rotated.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)) # allows the image to fit in window after rotate
            self.repaint()
        # if there is no image on the canvas
        else:
            self.errorMessage("no image to rotate")
    
    '''
    This method mirrors or flips the image along a given axis
    Can be flipped over the x-axis or y-axis
    '''
    # code drawn from reference: https://stackoverflow.com/questions/28409248/how-to-flip-a-qimage
    def mirror_image(self, axis):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            if axis == "horizontal": # mirror the image over the x-axis
                mirror_horizontal = QTransform().scale(-1, 1)
                pixmap = QPixmap(self.image)
                mirrored = pixmap.transformed(mirror_horizontal)
            elif axis == "vertical": # mirror the image over the y-axis
                mirror_vertical = QTransform().scale(1, -1)
                pixmap = QPixmap(self.image)
                mirrored = pixmap.transformed(mirror_vertical)

            self.image = QImage(mirrored)
            
            self.setPixmap(mirrored)
            self.repaint()
        # if there is no image on the canvas
        else:
            self.errorMessage("no image to Mirror")

    '''
    This method applies blurring effect to the image
    Strength is obtained from a dilog with a specified range
    blur_strenth is of type (int)
    '''
    # conceptualization drawn from reference: https://datacarpentry.org/image-processing/06-blurring.html#gaussian-blur
    def blur_image(self, blur_strength):
        # if there is an image on the canvas
        if self.image.isNull() == False:
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
        # if there is no image on the canvas
        else:
           #ignore
           pass

    '''
    This method applies grayscale on an image to achieve black/white effect
    '''
    def black_white_image(self):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            temp_converted_img = self.image.convertToFormat(QImage.Format.Format_Grayscale8)
            self.image = QImage(temp_converted_img)
            
            self.setPixmap(QPixmap().fromImage(temp_converted_img))
            self.repaint()
        # if there is no image on the canvas
        else:
            self.errorMessage("no image to convert to grayscale")

    '''
    This method pixelates an image to achieve a mosaic effect
    Pixelation varies based on input from user in a dialog 
    pixel_size is of type (int)
    '''
    # reference for conceptualization: https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
    def pixelate_image(self, pixel_size):
        # if there is an image on the canvas and pixelation effect was desired
        if self.image.isNull() == False and pixel_size > 0:
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
        # if there is no image on the canvas or no pixelation effect was desired
        else:
            # ignore
            pass

    '''
    This method changes the contrast between colors in an image
    Contrast varies based on input from user in dialog
    contrast_level is of type (int)
    '''
    # uses algorithm from reference: https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
    def adjust_contrast_image(self, contrast_level):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            contrasted = self.image.copy()
            contrast_factor = (259*(contrast_level + 255))/(255*(259 - contrast_level))
            for i in range(self.image.width()):
                for j in range(self.image.height()):
                    new_color = contrasted.pixelColor(i,j) # get the original pixel colors
                    new_color.setRed(int(round(median([0,(contrast_factor*(new_color.red() -128) + 128),255]),0)))
                    new_color.setBlue(int(round(median([0,(contrast_factor*(new_color.blue() -128) + 128),255]),0)))
                    new_color.setGreen(int(round(median([0,(contrast_factor*(new_color.green() -128) + 128),255]),0)))
                    contrasted.setPixelColor(i,j,new_color) # set the new pixel colors
            
            self.image = contrasted
            
            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()
        # if there is no image
        else:
            # ignore
            pass

    '''
    This method allows painting to be applied to the image with a brush
    Default brush size of 3
    '''
    def paint_pixels_image(self, origin, brush_size=3):
        # store all pixels in set, then paint them to ensure no duplicates
        color = self.paint_color
        pixels_to_paint = set()
        
        # paint around origin in radius of brush_size
        for x in range(brush_size):
            for y in range(brush_size):
                pixels_to_paint.add(QPoint(origin.x() + x, origin.y() + y))
        
        #when mouse is held, draw a line between a point and the previous point from last call to function
        if self.prev_paint_loc != None and self.prev_paint_loc != origin:
            line_x = origin.x() - self.prev_paint_loc.x()
            line_y = origin.y() - self.prev_paint_loc.y()
            distance = (line_x**2 + line_y**2) ** (1/2)
            step_x = line_x/distance
            step_y = line_y/distance
            for i in range(int(round(distance))):
                for x in range(brush_size):
                    for y in range(brush_size):
                        pixels_to_paint.add(QPoint(self.prev_paint_loc.x() + x + int(round((i*step_x))), self.prev_paint_loc.y() + y + int(round((i*step_y))) ))
       
        image_clone = self.image.copy()
        for point in pixels_to_paint:
            image_clone.setPixelColor(point,color)
        
        self.image = image_clone
        self.prev_paint_loc = origin
        
        self.setPixmap(QPixmap.fromImage(self.image))
        self.repaint()

    '''
    This method applies a sketch/pencil drawing effect on the image
    '''

    # reference algorithm: https://www.askpython.com/python/examples/images-to-pencil-sketch
    def sketch_image(self):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            # Convert QImage to format (BGR)
            image = self.image.convertToFormat(QImage.Format.Format_RGB32)
            # Convert QImage to OpenCV format
            width = image.width()
            height = image.height()
            ptr = image.bits()
            ptr.setsize(image.sizeInBytes())
            arr = np.array(ptr).reshape((height, width, 4))

            # Convert RGB to grayscale
            gray_image = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

            #Invert the gray image
            inverted_gray = cv2.bitwise_not(gray_image)

            # Apply GaussianBlur to the grayscale image
            blurred_image = cv2.GaussianBlur(inverted_gray, (21, 21), 0)

            #Invert blurred image
            inverted_blur = cv2.bitwise_not(blurred_image)

            # Calculate the DodgeV2 operation
            pencil_sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)

            # Convert OpenCV image back to QImage
            height, width = pencil_sketch.shape[:2]
            bytes_per_line = width

            sketched = QImage(pencil_sketch.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

            sketch_to_rgb = sketched.convertToFormat(QImage.Format.Format_RGB32)
            self.image = sketch_to_rgb

            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()
        # if there is no image on the canvas
        else:
            self.errorMessage("no image to Sketch")

    '''
    This method inverts the colors of the image to achieve a "negative" effect
    '''
    def invert_colors_image(self):
        # if there is an image on the canvas
        if self.image.isNull() == False:
            # Convert QImage to format (BGR)
            image = self.image.convertToFormat(QImage.Format.Format_RGB32)
            # Convert QImage to OpenCV format
            width = image.width()
            height = image.height()
            ptr = image.bits()
            ptr.setsize(image.sizeInBytes())
            arr = np.array(ptr).reshape((height, width, 4))

            # Invert the colors
            inverted_image = cv2.bitwise_not(arr)

            # Convert back to QImage
            bytes_per_line = width * 4
            inverted_image_as_QImage = QImage(inverted_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB32)

            self.image = inverted_image_as_QImage
            self.setPixmap(QPixmap.fromImage(self.image))
            self.repaint()
        else:
            self.errorMessage("no image to invert")

    '''
    This method allows the paintbrush to be toggled on or off to allow drawing
    '''
    def togglePaintbrush(self):
        self.paint_mode = not self.paint_mode
        self.prev_paint_loc = None

    '''
    This method handles pressing the mouse when drawing on the image and handles make RubberBank when moving the mouse.
    - Another feature we where trying to add is cropping. we initily started making the rubber band
    '''
    def mousePressEvent(self, event):   
        self.origin = event.pos()
        # if paint brush is toggled on
        if self.paint_mode:
            self.paint_pixels_image(self.origin)
        # if paint brush is toggled off
        else:
            # ignore
            pass

    '''
    This method handles moving the mouse across the image when drawing
    '''
    def mouseMoveEvent(self, event):
        # if paintbrush is toggled on
        if self.paint_mode:
            self.paint_pixels_image(event.pos())
        # if paintbrush is toggled off
        else: 
            #ignore
            pass

    '''
    This method handles when the mouse is released
    '''
    def mouseReleaseEvent(self, event):
        self.prev_paint_loc = None # reset the location of last drawn point
        
    '''
    This method handles error messages
    '''
    def errorMessage(self,message,error = "Error"):
        QMessageBox.information(self, error, message, QMessageBox.StandardButton.Ok)
