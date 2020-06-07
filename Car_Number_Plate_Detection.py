import cv2
import pytesseract
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "YOUR PATH TO TESSERACT"
MEDIA_FOLDER = "./test_images"


def process_text(text, image):
    height, width, channel = image.shape
    new_img = cv2.resize(image.copy(), (width, int(height * 1.25)))
    height, width, channel = new_img.shape
    new_img1 = new_img[:height // 2, width // 4:3 * width // 4]
    new_img2 = new_img[height // 2:, width // 4:]
    top_text = pytesseract.image_to_string(new_img1, lang="eng")
    bot_text = pytesseract.image_to_string(new_img2, lang="eng")
    two_line_text = top_text + bot_text
    if len(text) < 6:
        text = two_line_text
    if text == "":
        text = two_line_text
    if text == "":
        new_img = cv2.resize(image, (image.shape[1], int(image.shape[0] * 0.4)))
        text = str(pytesseract.image_to_string(new_img, lang="eng"))
    return "RESULT: " + text.replace("\n", " ")


def main():
    h1 = 256
    w1 = 768
    try:
        os.remove("./test_images/delete_this_after.png")
    except FileNotFoundError:
        pass

    for file in os.listdir("test_images"):
        print(file)
        image = cv2.imread(os.path.join(MEDIA_FOLDER, file))
        image = cv2.resize(image, (w1, h1))

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

        edged = cv2.Canny(blurred, 170, 200)
        cv2.imshow("Edged", edged)

        contours, new = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                PLATE = approx.copy()
                fx = [PLATE[i][0][1] for i in range(4)]
                fy = [PLATE[j][0][0] for j in range(4)]
                left1 = fx.index(min(fx))
                fx[left1], fx[0] = fx[0], fx[left1]
                fy[left1], fy[0] = fy[0], fy[left1]

                left2 = fx.index(min(fx[1:]))
                fx[left2], fx[1] = fx[1], fx[left2]
                fy[left2], fy[1] = fy[1], fy[left2]

                if fy[0] < fy[1]:
                    TOP_LEFT = [fy[0], fx[0]]
                    BOT_LEFT = [fy[1], fx[1]]
                else:
                    BOT_LEFT = [fy[0], fx[0]]
                    TOP_LEFT = [fy[1], fx[1]]

                if fy[2] < fy[3]:
                    TOP_RIGHT = [fy[2], fx[2]]
                    BOT_RIGHT = [fy[3], fx[3]]
                else:
                    BOT_RIGHT = [fy[2], fx[2]]
                    TOP_RIGHT = [fy[3], fx[3]]

                pts1 = np.float32([TOP_LEFT, TOP_RIGHT, BOT_RIGHT, BOT_LEFT])
                pts2 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]])

                matrix1 = cv2.getPerspectiveTransform(pts1, pts2)
                result1 = cv2.warpPerspective(image, matrix1, (w1, h1), flags=cv2.INTER_LINEAR)

                cv2.imshow("CROP", result1)
                cropped_img_loc1 = os.path.join(MEDIA_FOLDER, "delete_this_after.png")
                cv2.imwrite(cropped_img_loc1, result1)

                text = str(pytesseract.image_to_string(cropped_img_loc1, lang="eng"))
                res = process_text(text, result1)
                print(res)
                cv2.waitKey(0)
                break


if __name__ == "__main__":
    if pytesseract.pytesseract.tesseract_cmd == "YOUR PATH TO TESSERACT":
        raise FileNotFoundError("\nPlease tell the program your path to the file 'tesseract.exe'\nThe variable is "
                                "'pytesseract.pytesseract.tesseract_cmd'"
                                "If you don't have Tesseract-OCR, please refer to https://tesseract-ocr.github.io/")
    else:
        main()
