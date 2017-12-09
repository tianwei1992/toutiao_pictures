from hashlib import md5
import requests
r=requests.get('http://p1.pstatp.com/origin/470200049863ce0b1446')
file_path='{0}/{1}.{2}'.format('D://pics//',md5(r.content).hexdigest(),'jpg')
print(type(md5(r.content).hexdigest()))
print(file_path)
