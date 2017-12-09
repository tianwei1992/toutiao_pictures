import json
import re
gallery = '{\"count\":9,\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/46fc0003d90609736e02\"}'
gallery_r = r'{\"count\":9,\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/46fc0003d90609736e02\"}'
print('gallery=',gallery)
print('gallery_r=',gallery_r)
#加了r，反斜巷还是作转义用。输出没有任何差别
print()

gallery_1 = re.sub(r'\\', '', gallery_r)
print('gallery_1=',gallery_1)
#打印看看re.sub是否会原地修改
#print('gallery after re.sub',gallery)
#print('gallery1 after re.sub',gallery1)

#gallery2 = re.sub(r'\', '', gallery)
gallery3 = re.sub('\\', '', gallery)

#data = json.loads(gallery3)
#data = json.loads(gallery3)
#print('data=',data)