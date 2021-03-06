import cv2
import imutils
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\W10\AppData\Local\Programs\Tesseract-OCR\tesseract'

img = cv2.imread(r"C:\Users\W10\Desktop\bmw.jpg", cv2.IMREAD_COLOR)
img = cv2.resize(img, (800, 600))
cv2.imshow("res", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
cv2.waitKey(0)
gray = cv2.bilateralFilter(gray, 13, 15, 15)
cv2.imshow("bilateral", gray)
cv2.waitKey(0)

edged = cv2.Canny(gray, 30, 200)
cv2.imshow("canny", edged)
cv2.waitKey(0)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)

contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
cv2.imshow("all contours", img)
cv2.waitKey(0)

screenCnt = None

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)



mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
new_image = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("can", new_image)
cv2.waitKey(0)


(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("Tespit Edilen Araç Plakası:", text)
img = cv2.resize(img, (500, 300))
Cropped = cv2.resize(Cropped, (400, 200))
cv2.imshow('car', img)
cv2.imshow('Cropped', Cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()