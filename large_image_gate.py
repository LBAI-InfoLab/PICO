#OpenSlide used to open MRXS file and keep pixel quality
#Can run only on Linux OpenSlide not in Windows
import os
import numpy as np
import matplotlib.pyplot as plt
from openslide import OpenSlide
import cv2 as cv
import glob

file_to_process = glob.glob("/home/elwin/BGSA/*.mrxs")
for datas in file_to_process :
	line = datas.split("/")
	line_in_array = line[-1].split(".")
	title = line_in_array[0]
	
	mrx_image = OpenSlide(datas)
	gate = mrx_image.read_region((0,0),4,mrx_image.level_dimensions[4])
	##read_region is used to get the level 4 of the pyramidal picture ; level 1 to 3 can't
	##be used because the size and the quality of picture is too important for next step
	##PIL can't open too big file

	array_gate = np.array(gate)
	gate_bgr = cv.cvtColor(array_gate, cv.COLOR_RGBA2BGR)
	
	print "GATE IMAGE READ REGION : " + str(type(gate))
	cv.imwrite(str(title)+ ".bmp",gate_bgr)
	 


