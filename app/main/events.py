from flask import request, session
from flask_socketio import emit, join_room, leave_room,rooms
from ..videoManager import Hmd, VideoDevice
from .. import socketio, videoManager, hmdManager

@socketio.on('connect')
def connect():
    print(request.sid+" connected")

@socketio.on('disconnect')
def disconnect():
    if(videoManager.remove_videoDeviceById(request.sid)):
        print(f'Client {request.sid} disconnected')
    else:
        for hmd in hmdManager.hmds:
            if(hmd.id == request.sid):
                hmdManager.hmds.remove(hmd)


@socketio.on('registerVidSource')
def registerVidSource(data):
    join_room("videoSource")
    dev = VideoDevice(request.sid)    
    dev.add_sources(data)
    videoManager.add_video_device(dev)

@socketio.on('registerAdmin')
def registerAdmin():
    if('admin' not in socketio.server.manager.rooms['/']):
        join_room('admin')
        socketio.emit('admin joined', to = request.sid)
    else:
        socketio.emit("admin rejected", to = request.sid)
    

@socketio.on('refreshPreview')
def refreshVideo(vidId):
    #TODO:make multiple refresh
    if('admin' not in rooms()):
        return
    deviceid = videoManager.get_video_device_by_videoID(vidId).id
    if(deviceid):
        emit('refreshPreview',vidId , to=deviceid)


@socketio.on('videoRefreshed')
def videoRefreshed(data):
    for key, value in data.items():
        videoManager.update_source_by_id(key, value)
    emit('videoRefreshed', data, to='admin')

@socketio.on('register_hmd')
def register_hmd():
    join_room('hmd')
    hmdManager.hmds.append(Hmd(request.sid))

@socketio.on('projectOrder')
def projectOrder(data):
    if('admin' not in rooms()):
        return
    targetHmd = hmdManager.get_hmd_by_id(data['hmd'])
    targetHmd.view = data['vidId']
    vidDevice = videoManager.get_video_device_by_videoID(data['vidId'])
    roomId = targetHmd.id+vidDevice.id
    join_room(roomId,targetHmd.id)
    join_room(roomId,vidDevice.id)

    socketio.emit("projectOrder", {'room':roomId}, to=vidDevice.id)

@socketio.on('roomMessage')
def roomMessage(data):
    socketio.emit('roomMessage', data, to=data['room'])