from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from test.camera import VideoCamera
import time
from datetime import datetime
import os
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return render(request, 'test/index.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

@staff_member_required
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


@staff_member_required
def captures(request):

	camera = VideoCamera()
	
	for i in range(20):
		camera.save_frame(title = i, path = f"./results/{i}.jpg")
		print("Saved image")
		time.sleep(1)


	return render(request, 'test/captures_results.html')


@staff_member_required
def captures_results(request):
	data = Image.objects.all()
	context = {'data': data}

	return render(request, 'test/display_captures.html', context)



# Create your views here.
