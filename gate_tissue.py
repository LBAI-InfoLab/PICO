import cv2 as cv
from PIL import Image, ImageEnhance
import imutils
import glob

def analysis_picture(filename) :
	###Function used to gate tissue on picure and do a frame around tissue
	###Saved croped picture to analyse the croped picture with PICO
	file_to_process = glob.glob(filename)
	for datas in file_to_process :
		line = datas.split("\\")
		line_in_array = line[-1].split(".")
		title = line_in_array[0]
		print (datas)
		img = cv.imread(datas)

		###Change the picture in binary code (not RGB code) and obtain
		###black pixels for colored area and white pixel for not colored area
		###this transformation is necessary to detect the edges of tissue
		imgray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
		ret,thresh = cv.threshold(imgray,250,255,0)
		blurred = cv.GaussianBlur(thresh, (5, 5), 0)
		thresh_1 = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY)[1]
		
		###part to visualize the transformation

		#cv.namedWindow('Resized Window', cv.WINDOW_NORMAL)
		#cv.resizeWindow('Resized Window', 500, 800)
		#cv.imshow('Resized Window', thresh_1)
		#cv.waitKey(0)
		#cv.destroyAllWindows()



		###Here it's the design of contours around tissue
		###x_min , x_max, y_min and y_max are coordinates to create the gate around tissue
		###20 pixels are added to be sure to have complete tissue
		X = []
		Y = []
		cnts = cv.findContours(thresh_1.copy(), cv.RETR_LIST , cv.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		for c in cnts :
			if 1436 < c[0][0][0] < 5052 and c[0][0][1] > 844 :
				for line in c :
					X.append(line[0][0])
					Y.append(line[0][1])
					
				x_min = min(X) - 20
				x_max = max(X) + 20
				y_min = min(Y) - 20
				y_max = max(Y) + 20

				### part to visualize countours around tissue 
				### do a green feature around each part of tissue
				### not an obligation to have final result -> gate with tissue
				
				#M = cv.moments(c)
				#if M["m00"] != 0 :
					#cX = int(M["m10"]/M["m00"])
					#cY = int(M["m01"]/M["m00"])
					#cv.drawContours(img, [c], -1, (0,255,0), thickness = 5)
			#cv.namedWindow('Resized Window', cv.WINDOW_NORMAL)
			#cv.resizeWindow('Resized Window', 500, 800)
			#cv.imshow('Resized Window', img)
			#cv.waitKey(0)
			#cv.destroyAllWindows()


		### Cut picture with coordinate of gate and obtain a final picture with tissue
		### im : open picture with PIL
		### cropped_image : picture cropped but with big dimension and with many pixel
		### so big time of calcul 
		im = Image.open(datas)
		#print("X min : " + str(x_min) + "// X max : " + str(x_max) + "// Y min : " + str(y_min) + "// Y max :"  + str(y_max))
		box = (x_min,y_min,x_max,y_max)
		cropped_image = im.crop(box)
		print (cropped_image.info)
		nx, ny = cropped_image.size
		### resize picture to reduce the number of pixel and reduce time of execution
		### this picutre is saved to run in PICO 'open_slide.py'

		#cropped_image.save("C:\\Users\\Immuno5\\Desktop\\SLIDE.bmp")
		size_gland = cropped_image.size
		x_resize = size_gland[0]/1.2
		y_resize = size_gland[1]/1.2
		im2 = cropped_image.resize((int(x_resize),int(y_resize)), Image.LANCZOS)

		#cropped_image.save("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\output\\" + str(title) + ".jpg")
		print title
		im2.save("Images\\output\\" + str(title) + ".bmp", dpi =(60000,60000))
analysis_picture("Images\\input\\*.bmp")

