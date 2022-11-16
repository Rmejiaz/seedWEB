import cv2
from .models import Image
from datetime import datetime


class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()

		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes() 
	
	def save_frame(self, path, title):

		success, image = self.video.read()

		frame_flip = cv2.flip(image,1)
		cv2.imwrite(path, frame_flip)

		image = Image(title = title, photo = path, fecha = datetime.now())
		image.save()

		