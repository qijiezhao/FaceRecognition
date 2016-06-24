#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: hello.py

API_KEY = '1f62e1802e3bdcaa3f1b8c0713eb824a'
API_SECRET = 'Y5FWySkIlL-LWxSLQy9MzXcOt4NgiEZ9'

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
import time
from pprint import pformat
def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

# First import the API class from the SDK
# 首先，导入SDK中的API类
from facepp import API
from facepp import File
import os

api = API(API_KEY, API_SECRET)
#api.group.delete(group_name = 'test')
# Here are the person names and their face images
# 人名及其脸部图片
PERSONS = [
    #(u'欧列川', '/Users/O/Downloads/TJ_Faces/788'),
    (u'刘潇', '/Users/O/Downloads/TJ_Faces/787'),
    (u'龚思宏', '/Users/O/Downloads/TJ_Faces/487'),
    (u'邵玄', '/Users/O/Downloads/TJ_Faces/492'),
    (u'王甜虾', '/Users/O/Downloads/TJ_Faces/786')
]

IMAGES = {}
for name, directory in PERSONS:
    IMAGES[name] = []
    for file in os.listdir(directory):
        if file.split('.')[-1] == 'jpg':
            IMAGES[name].append(os.path.join(directory, file))

TARGET_IMAGE = '/Users/O/Downloads/TJ_Faces/788_c_1.jpg'

# Step 1: Detect faces in the 3 pictures and find out their positions and
# attributes
# 步骤1：检测出三张输入图片中的Face，找出图片中Face的位置及属性
FACES = {}
for name in IMAGES:
    FACES[name] = ''
    for img_path in IMAGES[name]:
        print img_path
        ret = api.detection.detect(img=File(img_path), mode='oneface')
        if len(ret['face']) > 0:
            face_id = ret['face'][0]['face_id']
            FACES[name] += (face_id + ',')
    FACES[name] = FACES[name][:-1]

# Step 2: create persons using the face_id
# 步骤2：引用face_id，创建新的person
for name, faces in FACES.items():
    print name, faces
    rst = api.person.create(
            person_name = name, face_id = faces)

# Step 3: create a new group and add those persons in it
# 步骤3：.创建Group，将之前创建的Person加入这个Group
#rst = api.group.create(group_name = 'test')
#print_result('create group', rst)
rst = api.group.add_person(group_name = 'test', person_name = FACES.iterkeys())
print_result('add these persons to group', rst)

# Step 4: train the model
# 步骤4：训练模型
rst = api.train.identify(group_name = 'test')
print_result('train', rst)
# wait for training to complete
# 等待训练完成
rst = api.wait_async(rst['session_id'])
print_result('wait async', rst)

# Step 5: recognize face in a new image
# 步骤5：识别新图中的Face
rst = api.recognition.identify(group_name = 'test', img = File(TARGET_IMAGE))
print_result('recognition result', rst)
print '=' * 60
print 'The person with highest confidence:', \
        rst['face'][0]['candidate'][0]['person_name']

# Finally, delete the persons and group because they are no longer needed
# 最终，删除无用的person和group
#api.group.delete(group_name = 'test')
#api.person.delete(person_name = FACES.iterkeys())

# Congratulations! You have finished this tutorial, and you can continue
# reading our API document and start writing your own App using Face++ API!
# Enjoy :)
# 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
# 己的App了！
# 旅途愉快 :)
