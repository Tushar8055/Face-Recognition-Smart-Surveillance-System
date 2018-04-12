import cv2
import numpy as np 
import os
import pickle
import sys

class CaptureAndTrain(object):

	def __init__(self):
		print('Hi')
		print('Image Training Started.')
		self.faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	def captureFromDir(self,path):
		count = 0

		for file in os.listdir(path):
			img = cv2.imread(path+'/'+file)
			img = cv2.resize(img,(500,400))
			img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

			faceCord = self.faceDetector.detectMultiScale(img,1.3,5)

			for x,y,w,h in faceCord:
				roi = img[y:y+h,x:x+w]
				roi = cv2.resize(roi,(200,200))
				count += 1
				cv2.imwrite('temp/'+str(count)+'.jpg', roi)


	def captureFromCam(self,cameraNumber):

		count = 0

		cap = cv2.VideoCapture(cameraNumber)

		while(True):

			_,frame = cap.read()

			frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

			cv2.imshow('Image', frame)

			faceCord = self.faceDetector.detectMultiScale(frame,1.3,5)

			for x,y,w,h in faceCord:
				roi = frame[y:y+h,x:x+w]
				roi = cv2.resize(roi,(200,200))
				count += 1
				
				cv2.imwrite('temp/'+str(count)+'.jpg', roi)
				cv2.putText(roi,str(count),(20,20),2,0.7,(0,0,255),2)
				cv2.imshow('ROI', roi)


			if (cv2.waitKey(1) & 0xFF == ord('q')) or count >=100:
				break
	

		cap.release()
		cv2.destroyAllWindows()

	def trainImage(self,personName):
		nameList = []
		imagePath = 'temp/'
		imageList = os.listdir(imagePath)
		trainingImage = []
		labelImage = []

		for i,item in enumerate(imageList):
			img = cv2.imread(imagePath+item)
			img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			trainingImage.append(np.asarray(img,dtype='uint8'))
			labelImage.append(i)

		model = cv2.createLBPHFaceRecognizer()
		model.train(np.asarray(trainingImage),np.asarray(labelImage))

		count = -1

		try:
			with open('train/FaceData/imagecount.txt','rb') as f:
				count = int(f.read())
				
			with open('train/FaceData/imagecount.txt','wb') as f:
				f.write(str(count+1))	

			with open('train/FaceData/nameList','r') as f:
				nameList = pickle.load(f)	
				nameList.append(personName)

			with open('train/FaceData/nameList','wb') as f:
				pickle.dump(nameList,f)	

		except:
			with open('train/FaceData/imagecount.txt','wb') as f:
				f.write('0')

			with open('train/FaceData/nameList','wb') as f:
				nameList.append(personName)
				pickle.dump(nameList,f)	

				


		model.save('train/FaceData/'+str(count+1)+'.cv2')				


	def __del__(self):
		print('Image Trained Succefully.')
		for item in sorted(os.listdir('temp/')):
				os.unlink('temp/'+item)	
		print('Bye')



if __name__ == "__main__":
	
	if not os.path.exists('train'):
		os.makedirs('train/FaceData/')
		os.makedirs('temp/')
		print('Directory created')

	try:
		personName = 'Your Name' # Change person name than run
		captrainObj = CaptureAndTrain() # Creating object for training

		if len(sys.argv)<=1:
			raise

		if sys.argv[1] == '-pn':
			if len(sys.argv[2])>0:
				
				personName = sys.argv[2]

				if sys.argv[3] == '-dir':
					if os.path.exists(sys.argv[4]):
						captrainObj.captureFromDir(sys.argv[4])
						captrainObj.trainImage(personName)
					else:
						raise	

				elif sys.argv[3]=='-cam':
					cameraNumber = 0
					
					try:
						cameraNumber = int(sys.argv[4])
					except:
						pass	

					captrainObj.captureFromCam(cameraNumber)
					captrainObj.trainImage(personName)		

				else:
					raise	
						
			else:
				raise				
		else:
			raise	

	except:
		print('Please pass arguments , while running program.')		
		print("-pn 'NameOfPerson' -dir Absolute_Path_To_Directory_Where_Training_Image_Is_Present ")
		print("-pn 'NameOfPerson' -cam Camera_Number_Default_Is_Set_To_0")
		raise
