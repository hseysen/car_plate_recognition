# Car Plate Recognition with Python
### Summary
This repository features a simple project that I have made as part of my research that I carried out for the conference "Process Automation and Information Security - 2020", dedicated to the 97th anniversary of the national leader Heydar Aliyev of Azerbaijan, organized by the Baku Higher Oil School.

The main goal of this project is to simulate the behavior of a Car Plate Recognition (CPR) system. I originally made this project, so that it could take input from a camera, but it was highly unstable, and the result could depend on the hardware of the camera used. Therefore, I decided to keep the project simple, and upload here a more general version of the project - which is responsible for the image processing section. I want to say that this project is in no way perfect or 100% accurate.


The idea is that there would be a camera that feeds some images to this image processing script. This script would then take that image, process it, and prepare it by flattening before sending to OCR. In this project I used Tesseract-OCR.

I mainly used the OpenCV module for image processing task. Below is briefly what the program does:
1. Read the images located at "./test_images" folder one by one
2. Resize the image, and apply a set of filters (grayscale, gaussian blur, canny) whose parameters can be tuned for higher accuracy
3. Detect the edges with _cv2.findContours()_, try to approximate a polygon with 4 sides, and pick the largest possible one
4. Then flatten this 4 sided polygon by using _cv2.warpPerspective()_, attempt to restore it to the flat rectangular shape
5. First, try to extract the text from the flattened image with _pytesseract_, and then send the extracted text and the flattened image to the _process_text()_ function
6. Since there are two main types of number plates in Azerbaijan (one as *./test_images/test1.jpg*, and the other as *./test_images/test2.jpg*), the _process_text()_ function tries to extract the text from the image in both ways (it divides the image into two parts in case the plate is similar to *test1.jpg*, and makes it shorter for another test, in case the images like *test2.jpg* were accidentally made taller during flattening (I don't have an example image for that))
7. Finally there are some arbitrary tests and comparisons on the texts which have a lot of room for improvement.

This simple version of CPR gave me accurate results on 3 types of test images, which is quite sufficient for me, but if anyone would like to improve it, or work on it, I encourage you to fork the repository, and improve the code.

### Tesseract-OCR
You need Tesseract-OCR installed on your computer to run this. Read more about it here: https://tesseract-ocr.github.io/

After installing Tesseract-OCR, on the 6th line of my code, I have set the path to the Tesseract-OCR to a string saying "YOUR PATH TO TESSERACT", make sure to change it to the appropriate path to _tesseract.exe_ file.

### Needed packages
Here is the list of packages that you need to run this:
* opencv-python
* Pillow
* numpy
* pytesseract
