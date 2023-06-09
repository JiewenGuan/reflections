class ReprMixin(object):
    def __repr__(self):
        ret = '<{}:{}'.format(self.__class__.__name__, self.id)
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state' and key != 'id':
                buffer = str(value)
                if(len(buffer) > 30):
                    buffer = buffer[:10]+"..."+buffer[-10:]
                ret += '|{}:{}'.format(key, buffer)
        return ret+">"



class Source(ReprMixin):
    def __init__(self, id, value):
        self.id = id
        self.description = value["label"]
        self.preview = value["preview"]
    def to_dict(self):
        return {
            'id':self.id,
            'description':self.description,
            'preview':self.preview
        }
class VideoDevice(ReprMixin):
    def __init__(self, id):
        self.id = id
        self.sources: list[Source] = []

    def add_sources(self, source):
        for key,value in source.items():
            self.sources.append(Source(key,value))

    def to_dict(self):
        ret = []
        for source in self.sources:
            ret.append(source.to_dict())
        return {
            self.id: ret
        }

class VideoManager(ReprMixin):
    def __init__(self):
        self.video_devices: list[VideoDevice] = []

    def add_video_device(self, video_device):
        self.video_devices.append(video_device)
        

    def get_video_device_by_id(self, id):
        for video_device in self.video_devices:
            if video_device.id == id:
                return video_device
        return None
    
    def remove_videoDeviceById(self, id):
        for video_device in self.video_devices:
            if video_device.id == id:
                self.video_devices.remove(video_device)
                return True
        return False
    
    def to_dict(self):
        ret = {}
        for video_device in self.video_devices:
            ret.update(video_device.to_dict())
        return ret

    def get_video_device_by_videoID(self, videoID):
        for video_device in self.video_devices:
            for source in video_device.sources:
                if source.id == videoID:
                    return video_device
        return False
    
    def update_source_by_id(self, id, preview):
        for device in self.video_devices:
            for source in device.sources:
                if source.id == id:
                    source.preview = preview
                    return True
        return False

class Hmd(ReprMixin):
    def __init__(self, id, view = None, name = ""):
        self.id = id
        self.view = view
        self.name = name

    def get_name(self):
        if(len(self.name)>0):
            return self.name
        else:
            return self.id
        
    def to_dict(self):
        ret = {
            "id":self.id
        }
        if(self.view):
            ret["view"] = self.view
        if(len(self.name)>0):
            ret["name"] = self.name
        return ret
    

class HmdManager:
    def __init__(self) -> None:
        self.hmds: list[Hmd] = []

    def add_hmd(self, hmd):
        self.hmds.append(hmd)

    def get_hmd_by_id(self, id):
        for hmd in self.hmds:
            if hmd.id == id:
                return hmd
        return None
    
    
