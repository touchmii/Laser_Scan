# coding: utf-8
#usr/bin/python3

import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import math

	
def img_processing(img):
	# 灰度化
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('gray.png', gray)
	ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
	# canny边缘检测
	edges = cv2.Canny(binary, 50, 150, apertureSize=3)
	cv2.imwrite('edges.png', edges)
	return edges

	
def line_detect(img):
	img = Image.open(img)
	img = ImageEnhance.Contrast(img).enhance(3)
	# img.show()
	img = np.array(img)
	result = img_processing(img)
	# 霍夫线检测
	lines = cv2.HoughLinesP(result, 1, 1 * np.pi/180, 10, minLineLength=50, maxLineGap=50)
	# print(lines)
	print("Line Num : ", len(lines))
	
	# 画出检测的线段
	for line in lines:
		for x1, y1, x2, y2 in line:
			cv2.line(img, (x1, y1), (x2, y2), (255, 106, 106), 5)
		pass
	cv2.imwrite('resut.png', img)
	img = Image.fromarray(img, 'RGB')
	# img.show('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	
if __name__ == "__main__":
	line_detect("Figure_1.png")
	
	
#	pass