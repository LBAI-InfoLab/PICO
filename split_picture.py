###Test split picture
from PIL import Image
import glob
import image_slicer
import os
from decimal import Decimal
import time
import multiprocessing
from pathos.multiprocessing import ProcessPool as Pool

"""
Functions : create_red_list; create_brown_list; create_other_list
- Create and return rgb for pixels of red color, brown color and "other"
  (blue for conterstaining, white and part of tissue a little bit brown)
- Pictures are selected from differents slides with a zoom on the part of interest
- functions scan pictures and obtain the RGB code 
"""
def create_red_list():
	rgb_def_red = []
	file_red = open("red_color.csv","r")
	data = file_red.readlines()
	file_red.close()

	for line in data : 
		line = line.replace("\n","")
		line_a = (line)
		if (line_a) not in rgb_def_red:
			rgb_def_red.append((line_a))

	return rgb_def_red
def create_brown_list() :
	"""
	-> Create and return rgb for brown pixels for database
	"""
	rgb_def_brown = []
	file_brown = open("brown_color.csv","r")
	data_brown = file_brown.readlines()
	file_brown.close()

	for line in data_brown : 
		line = line.replace("\n","")
		line_a = (line)
		if (line_a) not in rgb_def_brown :
			rgb_def_brown.append((line_a))
	return rgb_def_brown
def create_other_list():
	"""
	-> Create and return rgb for others pixels for database (blue understaining, white, brown moderate)
	"""
	rgb_def_blue = []
	file_blue = open("other_pixel.csv","r")
	data_blue = file_blue.readlines()
	file_blue.close()

	for line in data_blue : 
		line = line.replace("\n","")
		line_a = (line)
		if (line_a) not in rgb_def_blue :
			rgb_def_blue.append((line_a))

	return rgb_def_blue

## List initialisation
red = create_red_list()
brown = create_brown_list()
other = create_other_list()


"""
Functions :  analyse_red_list,  analyse_blue_list,  analyse_other_list
- The selection of zoom (for previous function) aren't precise
  so on differents lis of RGB code we delete pixels presents in others lists
  To have in fine 3 specifics lists for each color 'red', 'brown' and 'counterstaining'
"""

def analyse_red_list(red,brown,others) :
	red_p = []
	for line in red :
		if line in brown and line in others :
			line = " "
		if line != " " :
			red_p.append(line)
	return red_p
def analyse_brown_list(red,brown,others):
	brown_p = []
	for line in brown :
		if line in red and line in others :
			line = " "
		if line != " " :
			brown_p.append(line)
	return brown_p
def analyse_other_list(red,brown,others):
	other_p = []
	for line in others :
		if line in red and line in brown :
			line = " "
		if line != " " :
			other_p.append(line)
	return other_p

red_p = analyse_red_list(red,brown,other)
brown_p = analyse_brown_list(red,brown,other)
other_p = analyse_other_list(red,brown,other)

def divided_picture(split,filename) :
	"""
	Function used to cut input picture to do multiprocessing 
	- split : argument to choose the number of part to cut slide
	"""
	file_to_process = glob.glob(filename)
	for file in file_to_process :
		#print file
		line = file.split("\\")
		line_in_array = line[-1].split(".")
		title = line_in_array[0]

		im = Image.open(file)
		pixelMap = im.load()

		(largeur, hauteur) = im.size
		number_of_pixel = int(largeur)*int(hauteur)
		img = image_slicer.slice(file, split, save = False)
		final_results = image_slicer.save_tiles(img, directory = 'Images\\split', prefix = title)

		im.close()

divided_picture(4,"Images\\output\\*.bmp")

def count_pixel(input_data):
	"""
	- This function are multiprossess to parallelise the 4 part of the picture
	- Input data : list composed of different list to found
	  red pixel, brown pixel, and others pixels
	- For every pixel of picture the function exclude "others" pixels
	  to simplified the research of red and brown pixels
	- Function return the number of red and brown pixels in a list for each part of split picture
	"""
	image = input_data[0]
	red_p = input_data[1]
	brown_p = input_data[2]
	other_p = input_data[3]

	## create def list there
	im = Image.open(image)
	print "|| Start count_pixel function || " + str(image) + " || " + str(time.strftime("%A %d %B %Y %H:%M:%S"))
	width = im.size[0]
	height = im.size[1]
	number_of_pixel = int(width)*int(height)

	red_pixel = 0
	brown_pixel = 0
	others_pixels = 0
	cmpt = 0
	for x in range(width) :
		for y in range(height) :
			(r,g,b) = im.getpixel((x,y))
			if str((r, g, b)) not in str(other_p) :
				if str((r, g, b)) in str(red_p):
					red_pixel += 1
									
				if str((r, g, b)) in str(brown_p):
					brown_pixel += 1

				if (str((r, g, b)) not in str(red_p)) and (str((r, g, b)) not in str(brown_p)):
					others_pixels += 1
			cmpt += 1

	print "FILE NAME : " + str(image) + "TOTAL RED : " + str(red_pixel) + " || TOTAL BROWN : " + str(brown_pixel)
	print "|| END count-pixel function ||"

	return red_pixel,brown_pixel,image


def final_ratio(total_red,total_brown,title) :
	"""
	- total_red and total_brown are the count of pixel from "count_pixel" function for 4 part of picture
	- function add the 4 "red_pixel" and "brown_pixel" count to calculate the final ratio of LyB/LyT
	"""
	final_red_pixel = int(total_red[0]) + int(total_red[1]) + int(total_red[2]) + int(total_red[3])
	final_brown_pixel = int(total_brown[0]) + int(total_brown[1]) + int(total_brown[2]) + int(total_brown[3])
	print "FINAL TOTAL RED :" + str(final_red_pixel)
	print "FINAL TOTAL BROWN : " + str(final_brown_pixel)

	if (final_red_pixel == 0):
		print "Ratio LyB/LyT : 0/100"
	if (final_brown_pixel == 0) :
		print "Ratio LyB/LyT : 100/0"
	
	### doctor of anapath give a ratio in percent (ex : 95/5 ; 70/30 ; ...) -> 'medecin ratio'
	### I calculate each 'medecin ratio' in text file cith the correlation with real result (ex : 95/5 = 19 ; 70/30 = 2.33)
	### ratio_calculating is a dictionnary with correspondance betwenn ratio and real result
	ratio_calculating = {}
	if (final_red_pixel > 0) and (final_brown_pixel > 0) :
		## Calculate the number of red pixel / number of brown pixel
		## Add results on CSV file
		ratio = Decimal(float(final_red_pixel)/float(final_brown_pixel))
		final_ratio = round(ratio,2)
		print "Ratio LyB/LyT : " + str(final_ratio)
		info_date = time.strftime("%A %d %B %Y %H:%M:%S")
		slides = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\resultats_BGSA_25_05_2019.csv","a")
		slides.write(str(info_date) + "FILE : " + str(title) + "; Number of red pixel : " + str(final_red_pixel) + "; Number of brown pixel : " + str(final_brown_pixel) + "; ratio :" + str(final_ratio) + "\n")
		slides.close()


		## search the correspondance with the calculate ratio
		file_ratio = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\ratio.txt","r")
		data_ratio = file_ratio.readlines()
		file_ratio.close()
		for line in data_ratio:
			if line != "":
				line = line.replace("\n","")
				line_in_array = line.split(";")
				final_result = line_in_array[0]
				percent_ratio = line_in_array[1]
				if (final_result not in ratio_calculating.keys()):
					ratio_calculating[final_result] = percent_ratio

		for key in ratio_calculating.keys():
			if str(final_ratio) in ratio_calculating[key] :
				print "Ratio LyB/LyT : " + str(key)
			if (float(ratio_calculating[key]) - 0.15) < float(final_ratio) < (float(ratio_calculating[key]) + 0.15) :
				print "Essai ratio LyB/LyT : " + str(key)
				
			if 9.2 <str(final_ratio)<20:
				print "Ratio LyB/LyT : 95/5"
		final_red_pixel = "NA"
		final_brown_pixel = "NA"
		print "END : " + str(time.strftime("%A %d %B %Y %H:%M:%S"))
def delete_file():
	"""
	Pictures are cut in 4 parts and stock in a folder during calcul,
	to don't saturate memory parts of pictures are delete
	"""
	file_to_process = glob.glob("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\split\\*.png")
	for file in file_to_process :
		os.remove(file)


if __name__ == '__main__':
	print "|| INITIATION MULTIPROCESSING ||"
	pool = multiprocessing.Pool()
	file_to_process = glob.glob("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\split\\*.png")
	input_data_list = []
	for file in file_to_process :
		input_data = (file, red_p, brown_p,other_p) 
		input_data_list.append(input_data)
	results = pool.map(count_pixel,input_data_list)
	pool.close()
	pool.join()

	## Collect return of "count_pixel" function 
	total_red = []
	total_brown = []
	file = []
	nb_result = 0
	for iteration in results :
		total_red.append(iteration[0])
		total_brown.append(iteration[1])
		file.append(iteration[2])

		nb_result+=1
		## Reconstitute count of pixel for picture with final_ratio function
		## Need to run funciton for 4 iteration (cause picture are cut in 4 parts)
		if nb_result == 4 :
			file_write = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\results_BGSA_anapath.tsv","a")
			file_write.write(str(file) + ";" + str(total_red) + ";" + str(total_brown) + "\n")
			file_write.close()
			final_ratio(total_red,total_brown,file)
			
			## Initialisation of variable to count and calculate ratio for next file
			nb_result = 0
			total_brown = []
			total_red = []
			file = []
			


	print "|| END OF MULTIPROCESSING ||"

	delete_file()
