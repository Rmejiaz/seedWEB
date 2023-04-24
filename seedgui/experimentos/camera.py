import cv2
from datetime import datetime
import os

class VideoCamera(object):
	def __init__(self, Image):
		self.video = cv2.VideoCapture(0)
		self.Image = Image

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()

		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes() 
	
	def save_frame(self, fecha, experimento):

		success, image = self.video.read()

		frame_flip = cv2.flip(image,1)
		path = f"./images/{fecha.strftime('%m:%d:%Y_%H:%M:%S')}.jpg"
		cv2.imwrite(path, frame_flip)

		image_obj = self.Image(fecha = fecha, experimento=experimento, photo = path)
		image_obj.save()

		return path, frame_flip

		