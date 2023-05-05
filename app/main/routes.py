from flask import Response, send_from_directory, session, redirect, url_for, render_template, request
from . import main
from .. import videoManager, hmdManager
from ..camera_opencv import Camera


@main.route("/favicon.ico")
def fav():
    return send_from_directory("static", "favicon.ico")


@main.route("/script/<filename>")
def script(filename):
    return send_from_directory("script", filename)

@main.route("/video_devices")
def video_devices():
    return videoManager.to_dict()

@main.route("/get_hmds")
def get_hmds():
    ret = []
    for hmd in hmdManager.hmds:
        ret.append(hmd.to_dict())
    return ret


@main.route('/', methods=['GET'])
def index():
    return render_template("main/index.html")


@main.route('/video_source', methods=['GET'])
def video_source():
    return render_template("main/video_source.html")


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("main/admin.html")

@main.route('/camera')
def cameraPage():
    return render_template("main/camera.html")

def gen(camera:Camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n--frame\r\n'

@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    headers={
                        'Content-Security-Policy': "default-src 'self'",
                        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
                    })


@main.route('/capture', methods=['GET', 'POST'])
def capture():
    return render_template("main/capturetest.html")


