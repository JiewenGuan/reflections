from flask import request, session
from flask_socketio import emit, join_room, leave_room,rooms
from ..videoManager import VideoDevice
from .. import socketio, videoManager

@socketio.on('connect')
def connect():
    print(request.sid+" connected")

@socketio.on('disconnect')
def disconnect():
    videoManager.remove_videoDeviceById(request.sid)
    print(f'Client {request.sid} disconnected')

@socketio.on('registerVidSource')
def registerVidSource(data):
    join_room("videoSource")
    dev = VideoDevice(request.sid)    
    dev.add_sources(data)
    videoManager.add_video_device(dev)

@socketio.on('registerAdmin')
def registerAdmin():
    #TODO:the rooms() function is not working
    if('admin' not in socketio.server.manager.rooms['/']):
        join_room('admin')
        socketio.emit('admin joined', to = request.sid)
    else:
        socketio.emit("admin rejected", to = request.sid)
    

@socketio.on('refreshPreview')
def refreshVideo(vidId):
    deviceid = videoManager.get_video_device_by_videoID(vidId)
    if(deviceid):
        emit('refreshPreview',vidId , to=deviceid)


@socketio.on('videoRefreshed')
def videoRefreshed(data):
    emit('videoRefreshed', data, to='admin')