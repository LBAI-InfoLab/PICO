"""
Project : slides CD3-CD20

Data base of pixel for red color and brown color based on zomm of slides
"""


from PIL import Image
from random import randint
import glob

def red_pixel():
	file_to_process_red = glob.glob("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\red_zoom\\*.jpg")
	print len(file_to_process_red)
	for file in file_to_process_red :
		im = Image.open(file)
		(largeur, hauteur) = im.size
		number_of_pixel = int(largeur)*int(hauteur)
		print file
		print "[+] Number of pixel red : " + str(number_of_pixel)
		for x in range(largeur):
			for y in range(hauteur):
				(rouge, vert, bleu) = im.getpixel((x,y))
				writing_file = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\red_color.csv","a")
				writing_file.write(str((rouge,vert,bleu)) + "\n")
				writing_file.close()
				#print str((rouge,vert,bleu))

def brown_pixel():
	file_to_process_brown = glob.glob("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\brown_zoom\\*.jpg")
	print len(file_to_process_brown)
	for file_brown in file_to_process_brown :
		im_brown = Image.open(file_brown)
		(largeur, hauteur) = im_brown.size
		number_of_pixel = int(largeur)*int(hauteur)
		print file_brown
		print "[+] Number of pixel brown : " + str(number_of_pixel)
		for w in range(largeur):
			for z in range(hauteur):
				(rouge, vert, bleu) = im_brown.getpixel((w,z))
				writing_file = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\brown_color.csv","a")
				writing_file.write(str((rouge,vert,bleu)) + "\n")
				writing_file.close()
				#print str((rouge,vert,bleu))

def other_pixel():
	file_to_process_blue = glob.glob("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\Images\\blue_zoom\\*.jpg")
	print len(file_to_process_blue)
	for file_blue in file_to_process_blue :
		im_blue = Image.open(file_blue)
		(largeur, hauteur) = im_blue.size
		number_of_pixel = int(largeur)*int(hauteur)
		print file_blue
		print "[+] Number of pixel blue : " + str(number_of_pixel)
		for x in range(largeur):
			for y in range(hauteur):
				(rouge, vert, bleu) = im_blue.getpixel((x,y))
				writing_file = open("C:\\Users\\Immuno5\\Desktop\\Tiphaine\\GitRepo\\CD3_CD20\\other_pixel.csv","a")
				writing_file.write(str((rouge,vert,bleu)) + "\n")
				writing_file.close()
				#print str((rouge,vert,bleu))

red_pixel()
#brown_pixel()
#other_pixel()
