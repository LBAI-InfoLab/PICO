"""
Project : slides CD3-CD20
Count pixel in file
"""

"""
TO DO LIST :
Faire une barre de progression

"""
from decimal import Decimal
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
import glob
import numpy as np
import matplotlib.pyplot as plt
import image_slicer


file_to_process = glob.glob("C:\\Users\\Immuno5\\Documents\\calibration\\*.jpg")

print len(file_to_process)

"""
Open picture with PIL and calculate the size of picture
"""

for file in file_to_process :
	im = Image.open(file)
	pixelMap = im.load()
	#lame = plt.imshow(im)
	#plt.show(lame)
	#plt.close()

	#im.show()
	(largeur, hauteur) = im.size
	number_of_pixel = int(largeur)*int(hauteur)
	print file
	print "[+] Number of pixel : " + str(number_of_pixel)

	"""
	Define variables, red_pixel are CD20 and brown_pixel are CD3 ; rgb_def_red and rgb_def_brown are lists for tuple corresponding of pixels basedata
	"""

	red_pixel = 0
	brown_pixel = 0
	others_pixels = 0


	rgb_def_red = []
	rgb_def_brown = []
	rgb_def_blue = []

	"""
	Open file and read basedata pixel
	"""

	file = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\red_color.csv","r")
	data = file.readlines()
	file.close()

	for line in data : 
		line = line.replace("\n","")
		line = line.replace("(","")
		line = line.replace(")","")
				
		line_in_array = line.split(",")

		red = int(line_in_array[0])
		green = int(line_in_array[1])
		blue = int(line_in_array[2])

		if ((red,green,blue) not in rgb_def_red):
			rgb_def_red.append((red,green,blue))

	file_brown = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\brown_color.csv","r")
	data_brown = file_brown.readlines()
	file_brown.close()

	for line in data_brown : 
		line = line.replace("\n","")
		line = line.replace("(","")
		line = line.replace(")","")
				
		line_in_array = line.split(",")

		brown_red = int(line_in_array[0])
		brown_green = int(line_in_array[1])
		brown_blue = int(line_in_array[2])

		if ((brown_red,brown_green,brown_blue) not in rgb_def_brown):
			rgb_def_brown.append((brown_red,brown_green,brown_blue))
	
	file_blue = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\other_pixel.csv","r")
	data_blue = file_blue.readlines()
	file_blue.close()

	for line in data_blue : 
		line = line.replace("\n","")
		line = line.replace("(","")
		line = line.replace(")","")
				
		line_in_array = line.split(",")

		brown_red = int(line_in_array[0])
		brown_green = int(line_in_array[1])
		brown_blue = int(line_in_array[2])

		if ((brown_red,brown_green,brown_blue) not in rgb_def_blue):
			rgb_def_blue.append((brown_red,brown_green,brown_blue))


	###Found correspondance between basedata and pixel of picture for red_pixels

	cmpt = 0
	for x in range(largeur):
		for y in range(hauteur):
			(r, g, b) = im.getpixel((x,y))
			#print str((r, g, b))
			if (r, g, b) not in rgb_def_blue :
				if str((r, g, b)) in str(rgb_def_red):
					red_pixel += 1
							
				if str((r, g, b)) in str(rgb_def_brown):
					#print "[FOUND] => " + str((r, g, b))
					brown_pixel += 1

				if (str((r, g, b)) not in str(rgb_def_red)) and (str((r, g, b)) not in str(rgb_def_brown)):
					#print "[+] Autres pixels" + str((r, g, b))
					others_pixels += 1
				cmpt += 1


	#pool = Pool()
	#results = pool.map(function_to_count,)

	
	
	"""
	###Create a new picture with red_pixel and brown_pixel colored

	cmpt = 0

	img = Image.new(im.mode,im.size)
	pixelsNew = img.load()
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			(r, g, b) = im.getpixel((x,y))
			if str((r, g, b)) in str(rgb_def_red):
				red_pixel += 1
				pixelMap[x,y] = (255,255,0)
			pixelsNew[x,y] = pixelMap[x,y]

			if str((r, g, b)) in str(rgb_def_brown):
				#print "[FOUND] => " + str((r, g, b))
				brown_pixel += 1
				pixelMap[x,y] = (1,215,88)
			pixelsNew[x,y] = pixelMap[x,y]

			if (str((r, g, b)) not in str(rgb_def_red)) and (str((r, g, b)) not in str(rgb_def_brown)):
				#print "[+] Autres pixels" + str((r, g, b))
				others_pixels += 1
			cmpt += 1

	im.close()
	#img.show()
	#img.save("C:\\Users\\Immuno5\\Desktop\\test_imageblanc.png","PNG")
	plt.imshow(img)
	plt.show()
	"""

	###Calulate ratio
	
	ratio_calculating = {}
	if (red_pixel > 0) and (brown_pixel > 0) :
		ratio = Decimal(float(red_pixel)/float(brown_pixel))
		final_ratio = round(ratio,2)
		print "Ratio LyB/LyT : " + str(final_ratio)
		slides = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\resultats_slides.csv","a")
		slides.write(str(file) + "; Number of pixel : " + str(number_of_pixel) + "; Number of red pixel : " + str(red_pixel) + "; Number of brown pixel : " + str(brown_pixel) + "; ratio :" + str(final_ratio))
		slides.close()



		file_ratio = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\ratio.txt","r")
		data_ratio = file_ratio.readlines()
		file_ratio.close()
		for line in data_ratio:
			if line != "":
				line = line.replace("\n","")
				line_in_array = line.split(";")

				#print line_in_array[1]

				final_result = line_in_array[0]
				percent_ratio = line_in_array[1]

				if str(red_pixel) == 0 :
					ratio == 0
				if (final_result not in ratio_calculating.keys()):
					ratio_calculating[final_result] = percent_ratio

		for key in ratio_calculating.keys():
			if str(final_ratio) in ratio_calculating[key] :
				print "Ratio LyB/LyT : " + str(key)
			if (float(ratio_calculating[key]) - 0.1) < float(final_ratio) < (float(ratio_calculating[key]) + 0.1) :
				print "Essai ratio LyB/LyT : " + str(key)
			if str(final_ratio) not in ratio_calculating[key]:
				if ("0.05" in ratio_calculating[key]) and (ratio_calculating[key] > str(final_ratio)):
					print "Ratio LyB/LyT : 0/100"
				if ("19" in ratio_calculating[key]) and (ratio_calculating[key] < str(final_ratio)):
					print "Ratio LyB/LyT : 100/0"


	if (red_pixel == 0):
		print "Ratio LyB/LyT : 0/100"

	if (brown_pixel == 0) :
		print "Ratio LyB/LyT : 100/0"

