from flask import send_from_directory, session, redirect, url_for, render_template, request
from . import main
from .. import videoManager, hmds


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
    for hmd in hmds:
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




@main.route('/capture', methods=['GET', 'POST'])
def capture():
    return render_template("main/capturetest.html")


