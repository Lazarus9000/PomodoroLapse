import cv2
#pip install opencv-python
import numpy as np
import glob

filenames = []
dates = []

#Timelapse script by Lars Knudsen

#This script read all files ending in .jpg in the current folder
#Filenames are expected to be named IMG_YYYYMMDD_HHMMSS, eg. IMG_20220409_203557.jpg
#All files are compiled to one video file per day, with frames being sorted in ascending order (e.g. the movie plays forward in time)

#General implementation heavily inspired by https://stackoverflow.com/a/44948030

#Read all filenames and build an array of all dates in the fileset
for filename in glob.glob('*.jpg'):
    #print(filename)
	filenames.append(filename)
	#IMG_20220409_203557.jpg
	
	#Date is extracted by reading the 4th to the 12th character
	#print(filename[4:12])
	filedate = filename[4:12]
	
	#Check if date from file already is in list of dates
	if filedate not in dates:
		#If not then it is added
		dates.append(filedate)

#print(dates)

#Make a movie for each date - making a movie for the entire dataset in one go exhausts system memory
for	date in dates:
	image_array = []
	size = (0,0)
	dark = 0
	light = 0

	print("processing " + date)

	for filename in filenames:
		#Find images from the current date only
		if ("IMG_" + date) in filename:
			#Read image
			img = cv2.imread(filename)
			
			#Calculate average brightness of frame, by converting to greayscale using HSV and calculating the average
			#Inspired by https://stackoverflow.com/a/58155405
			#Used to discard dark frames taken during nighttime
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			_, _, v = cv2.split(hsv)
			brightness = int(np.average(v.flatten()))
			
			#print("Image : " + filename + ", brightness: " + str(brightness))
			
			#The threshold for brightness is found by a bit of experimentation
			if brightness > 25:
				#Count how many frames were included, only used for debugging
				light += 1
				#Append frame to array of images which will be compiled to video
				image_array.append(img)
				
				#If size of images for date hasn't been found
				if size == (0,0):
					#print("Size not set")
					height, width, layers = img.shape
					size = (width,height)
				#else:
					#print("Size set!")

			else:
				#Count how many frames were discarded due to low brightness, only used for debugging
				dark += 1
	
	moviename = 'project- ' + date + '.mp4'
	#Set up writing a video - parameters are file name, video type, frame rate and frame size
	out = cv2.VideoWriter(moviename, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
 
	#Add light images for the current date
	for i in range(len(image_array)):
		out.write(image_array[i])
	#Write video file
	out.release()
	
	print(str(light) + " images compiled to " + moviename + " - " + str(dark) + " dark images omitted")