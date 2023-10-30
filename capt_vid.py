# Python program to save a 
# video using OpenCV 


counterfile = open("counter.txt")
count = int(counterfile.read())
print(count)
counterfile.close()
counterfile = open("counter.txt", 'w')
counterfile.write(str(count+1))
counterfile.close()

import cv2 


# Create an object to read 
# from camera 
video = cv2.VideoCapture(-1) 

# We need to check if camera 
# is opened previously or not 
if (video.isOpened() == False): 
	print("Error reading video file") 

# We need to set resolutions. 
# so, convert them from float to integer. 

video.set(3,320)
video.set(4,240)
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 

size = (frame_width, frame_height) 

# Below VideoWriter object will create 
# a frame of above defined The output 
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename'+str(count)+'.avi', 
						cv2.VideoWriter_fourcc(*'MJPG'), 
						24, size) 
	
while(True): 
	ret, frame = video.read() 

	if ret == True: 

		# Write the frame into the 
		# file 'filename.avi' 
		result.write(frame) 

		# Display the frame 
		# saved in the file 
		cv2.imshow('Frame', frame) 

		# Press S on keyboard 
		# to stop the process 
		if cv2.waitKey(1) & 0xFF == ord('s'): 
			break

	# Break the loop 
	else: 
		break

# When everything done, release 
# the video capture and video 
# write objects 
video.release() 
result.release() 
	
# Closes all the frames 
cv2.destroyAllWindows() 

print("The video was successfully saved") 

