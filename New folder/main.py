import json
import os
from bbox import BBox2D
from collections import Iterable

classes = []
datasetdir = 'F:/New folder (2)/dataset/labels/train/'
validationdir = 'val'
traindir = 'train'


def get_unique_numbers(numbers):
    list_of_unique_numbers = []
    unique_numbers = set(numbers)
    for number in unique_numbers:
        list_of_unique_numbers.append(number)
    return list_of_unique_numbers


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)]


strructure = {
    "info": {"description": "my-project-name"},
    "images": [],
    "annotations": [],
    "categories": []
}
anatotions = {
    "id": 0,
    
    "iscrowd": 0,
    "image_id": 1,
    "category_id": 1,
    "segmentation": [[]],
    "bbox": [],
    "area": 0
    }
imageStructure = {

    "id": 1,
    "width": 3881,
    "height": 1514,
    "file_name": "path"
}

classestructure = {
    "id": 1,
    "name": "class1"
}
for filename in os.listdir(datasetdir):
    for i in os.listdir(f'{datasetdir}{filename}'):
        f = open(f"{datasetdir}{filename}/{i}", 'r',encoding="cp437")
        myjson = json.load(f)

        for i in range(len(myjson['objects'][0])):
            classes.append(myjson['objects'][i]['label'])
classes = get_unique_numbers(classes)

for count, i in enumerate(classes):
    classestructure['id'] = count + 1
    classestructure['name'] = classes[count]
    strructure['categories'].append(classestructure.copy())
    print(classestructure)
for filename in os.listdir(datasetdir):
    for count, i in enumerate(os.listdir(filename)):
        f = open(f"{filename}/{i}")
        myjson = json.load(f)
        imageStructure['id'] = count + 1
        imageStructure['width'] = myjson['imgWidth']
        imageStructure['height'] = myjson['imgHeight']
        strructure['images'].append(imageStructure.copy())

cnt = 0
for filename in os.listdir(datasetdir):
    for count, i in enumerate(os.listdir(f'{datasetdir}{filename}')):
        f = open(f"{datasetdir}{filename}/{i}")
        myjson = json.load(f)
        for subcount, i in enumerate(myjson['objects']):
            if i['label'] == 'road':
                anatotions['id'] = cnt
                anatotions['iscrowd'] = 0
                anatotions['image_id'] = count + 1
                catid = i['label']
                for i in strructure['categories']:
                    if i['name'] == catid:
                        mcatid = i['id']
                        break
                anatotions['category_id'] = mcatid
                poly = myjson['objects'][subcount]['polygon']
                anatotions['segmentation'] = [list(flatten(poly))]
                anatotions['bbox'] = bounding_box(
                    myjson['objects'][subcount]['polygon'])
                box = BBox2D(anatotions['bbox'])
                anatotions['area'] = box.height * box.width
                strructure['annotations'].append(anatotions.copy())
        cnt += 1

print(strructure)
