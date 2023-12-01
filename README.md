# Image Lab
_An Image Editor by ALI Media for CS 335 in Fall 2023_

## Features

- Opening and saving image files in various formats such as .jpg, .jpeg, and .png
- Image Processing techniques
  - Image transformations
  - Image filtering
- Drawing on a image

## Dependencies

This project uses several packages to render the user interface and the logic behind image processing:

- Python - general-purpose programming language used to build the program
- OpenCV - computer vision and image processing library that provides more sophisticated image processing tools
- PyQt6 - library to develop a desktop-based graphical user interface
- Numpy - scientific library that provides linear algebra tools necessary for image transformations

## Installing Dependencies

Packages and libaries can be installed individually in the environment the program will be located at by doing:
```sh
pip install opencv-python
pip install numpy
pip install PyQt6
```
Or you can install all dependencies in one command by doing:
```
pip install -r requirements.txt
```

## Running the Program

To run the program, ensure all dependencies have been installed and run the command in the directory the file is installed:
```
python image_editor_GUI.py
```
This will bring up a full screen application of the image editor

## Using the Editor

Opening and Saving an Image File:
- To open, click on 'File' on the menu bar, then select 'Open File'

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/8f68d1c2-6bdb-4b5b-a7c3-6dfb99da5247)

- Look for a location where you have images, filter image by types using the dialog, and select an image. Note: only the certain image file formats are supported as noted above
- To save, click on 'File' on the menu bar, then select 'Save File' then name the file and choose the desired format and click save on dialog.

Performing Image Transformations:
- Currently, there are 4 image transformations supported.
  - Rotation 90 degrees clockwise and counterclockwise
  - Mirror/Flipping with respect to x-axis and y-axis
- Hovering over the buttons indicates the type of transformation that can be applied, then simply click the desired option

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/f062306a-fd2c-456d-b214-7b0c03ec7648)

Performing Image Filtering:
- Currently there are 6 filters that can be applied to an image
  - Image blurring Note: clicking opens dialog to enter strength of blurring as an integer on the range 1 to 50 inclusive. 1 being
    low blur and 50 being maximum blur.
  - Black and White conversion
  - Pixelation Note: clicking opens dialog to enter pixel size as an integer on the range 1 to 100 inclusive. 1 being small pixel sizes
    and 100 being very large pixel sizes.
  - Contrast modification Note: clicking opens dialog to enter contrast level as an integer on the range -255 to 255 inclusive.
    Negative contrast level decreases difference between colors and positive contrast level increases difference.
  - Converting to pencil sketch
  - Inverting the image / negative effect
- Hovering over the buttons indicates the filter that can be applied, then simply click the desired option

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/e5037f87-98f5-46e4-b5ac-47344582eb75)

Drawing on the Image:
- To Draw on the image, it is necessary to first have an image open on the editor.
- Click on the paintbrush to toggle on or off.

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/a1b9d169-6d37-48c5-8e18-35ea561b3da7)

- You can also choose the color of the brush to draw on the image by clicking on the color buttons.

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/a118a392-26c4-4daa-8303-bbb1ca2cd91b)

- To draw on the image, toggle the paintbrush on and select a color. Then right-click and hold mouse/mousepad to draw on the image.

Reverting Edits:

- To revert filters, transformations, or drawings on an image, click on 'Edit' on the menu bar and then click on 'Revert'
- Note: Clicking 'Revert' reverts the image to the original version of image and every edit will be undone.

![image](https://github.com/ismailAlAbdali/pro3_cs335/assets/100641581/c4ff3f12-76e9-4e95-b0c3-7df7a56b398b)




