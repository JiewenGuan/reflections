install python 3.11

install virtualenv

$ python -m venv env

$ .\env\Scripts\activate

$ pip install -r .\requirements.txt

$ python reflections.py

在有摄像头的笔记本电脑上运行 reflections.py，可能需要在防火墙添加入站规则，预设端口为5000
在笔记本电脑上访问 https://localhost:5000 以确认运行是否正常
注意需要使用https
使用在同一网络中的头显访问https://<笔记本电脑ip>:5000 进行体验
当前分辨率预设为640*480,使用quest2可以相对流畅运行，最大测试过720p，非常卡顿