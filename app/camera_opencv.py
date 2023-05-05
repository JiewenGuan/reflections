import os
import cv2
from .base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set frame width to 640 pixels
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # set frame height to 480 pixels

        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            #height, width, channels = img.shape  # get image dimensions
            #print("Frame resolution: {}x{} ({} channels)".format(width, height, channels))
            # encode as a jpeg image and return it
            yield cv2.imencode('.png', img)[1].tobytes()