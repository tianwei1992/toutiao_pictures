import requests
import re
import json
from config import *
from pymongo import MongoClient
import os
from multiprocessing import Pool,Manager,Value,Process
from hashlib import md5


def get_index_page(url,offset):
	data={
		'offset':offset,
		'format':'json',
		'keyword':KEYWORD,
		'autoload':'true',
		'count': 20,
		'cur_tab': 1
	}
	headers={'User-Agent':'MOzilla/5.0'}
	try:
		#print(url)
		r=requests.get(url,params=data,headers=headers)
		#print(r.request.url)
		r.encoding=r.apparent_encoding
		r.raise_for_status()
		return r.text
	except:
		print('Exception:get page index ')



def parse_index_page(html):
	pattern=re.compile('article_url": "(.*?)"',re.S)
	url_list=re.findall(pattern,html)
	#urls=pattern.findall(html)
	#print(url_list)
	return url_list

def get_detail_page(url):
	headers={'User-Agent':'MOzilla/5.0'}
	try:
		print('分页的地址是=====',url)
		r=requests.get(url,headers=headers)
		#print(r.request.url)
		r.encoding=r.apparent_encoding
		r.raise_for_status()
		return r.text
		print('分页url请求完成，返回r.text')
	except:
		print('Exception:get page detail ')

def parse_detail_page(html,url_out,offset,i_fenye,counter_repetition,urls_exists):
	print('解析分页1：进入parse_detail_page',url_out)
	title_pattern=re.compile('<title>(.*?)</title>')
	pattern=re.compile('gallery: JSON\.parse\("(.*?)"\),',re.S)
	print('parss counter_repetition',counter_repetition)

	try:
		title = title_pattern.findall(html)[0]
		gallery=pattern.findall(html)[0]
		#print(gallery)

		gallery = re.sub(r'\\','',gallery)
		data=json.loads(gallery)
		#print(data)
		url_lst=[]
		#print("下面判断if data")
		print('解析分页2：提取gallery,如果不为空会有下一步')
		if data :
			print('解析分页3:gallery不为空，遍历分页内每个图')
			for i,item in enumerate(data["sub_images"]):
				#i就是该分页的图片序号,item是包含图片的下载地址的字典
				if item['url']:
					print("图片遍历1：item['url']")
					print("判断：图片url是否已经处理过了?")
					print('urls_exists===============',urls_exists)
					if  item['url'] not in urls_exists:

						print("图片遍历2:图片没有被处理过,执行append")
						urls_exists.append(item['url'])
						#print('append开始：把这张图片的下载地址append到分页的图片url列表')
						#print('urls_exists',urls_exists)
						url_lst.append(item['url'])
						#print("append完毕：这张图片的下载地址已append到分页的图片url列表")
						print("图片遍历3:download")
						download_image(item['url'],offset,i,i_fenye)
						print("图片遍历4:完成，下一张")

					else:
						print("图片遍历2：图片已经被处理过……，完成下一张")
						counter_repetition.value+=1
						print('counter_repetition=====',counter_repetition)

		print('解析分页4:完成')
		print('urls_exists', urls_exists)
		return({'url':url_out,'title':title,'pic_url':url_lst})
	except IndexError:
		#http://toutiao.com/group/6492262040000791053/这样的地址没有多图
		print('解析分页：没有多图url，跳出parse——detail')
		return None
	except Exception as e:
		print('解析分页：其他错误，跳出parse——detail')
		print('具体错误是',e)

#构造一个MongoClient对象，用于与服务器建立连接
client=MongoClient(MONGO_URL)
#创建一个名叫MONGO_DB的数据库
db=client[MONGO_DB]

def save_to_db(pic_infos):
	#client = MongoClient()
	#client = MongoClient('localhost', 27017)
	#db = client.pythondb
	#在db数据库的名为MONGO_TABLE的表中插入信息
	print('保存到数据库1：开始',pic_infos)
	if db[MONGO_TABLE].insert(pic_infos):
		print('保存到数据库2：insert成功保存到数据库!',pic_infos)
		return True
	else:
		return False

def download_image(url,offset,i,i_fenye):
	print('下载图片1：开始get',url)
	r=requests.get(url)
	#r.raise_for_status()
	r.encoding=r.apparent_encoding
	print('下载图片2：下面save')
	save_image(r,url,str(offset),str(i),str(i_fenye))
	print('下载图片3：完毕')
	#except Exception as e:
		#print('Exception in dowload_image')
		#print(e)
		#print(e)


def save_image(r,url,offset,i,i_fenye):
	print('图片保存本地1:开始')
	#windows路径分割必须用双斜杠\
	if not os.path.exists('D://pics2'):
		print('目录不存在，创建目录')
		os.mkdir('D://pics2')
		print('目录创建完成')
	print('开始构造图片存储本地路径')
	#file_path='D://pics1//'+offset+'_'+md5(r.content).hexdigest()+'_'+url[-4:]+'.jpg'

	file_path='D://pics2//'+str(offset)+'_'+str(int(i_fenye)+1)+'_'+str(int(i)+1)+'_'+url[-10:]+'.jpg'
	#offset,分页序号，分页内的的图片序号
	print('图片保存本地2:构造保存路径的字符串')
	print(file_path)
	if not os.path.exists(file_path):
		print('图片保存本地3:路径不存在，新建')
		with open(file_path,'wb') as f:
			f.write(r.content)
			#globals()['counter']+=1
			f.close()
		print('图片保存本地4:完毕')
	else:
		print('图片保存本地3:已存在，这一步应该不可能发生')



def main(offset,urls_exists,counter_repetition):
	print(urls_exists)
	print('main开始================，offset==',offset)
	print('main urls_exists',urls_exists)
	print('main counter_repetition.value',counter_repetition.value)
	html=get_index_page('https://www.toutiao.com/search_content/',offset*20)
	urls=parse_index_page(html)
	print('main提示：offset为{0}的index页已经解析完，获得了分页urls，下面遍历分页'.format(offset))
	print()
	for i_fenye,url in enumerate(urls):
		print('分页遍历1：开始对新的分页',url)
		detail_html=get_detail_page(url)
		print('分页遍历2：get获得了分页html，下面执行parse_detail_page')
		print()
		pic_infos=parse_detail_page(detail_html,url,offset,i_fenye,counter_repetition,urls_exists)
		print('分页遍历3：parse_detail完成，如果有返回信息会进入4')
		print('urls_exists in main',urls_exists)
		if pic_infos:
			print('分页遍历4：pic_infos存在，保存到数据库')
			#如果有的分页没有多图，那么就没有返回
			#print(pic_infos)
			save_to_db(pic_infos)
		print('分页遍历5：本分页遍历完成',url)
		print()
	print('main函数执行完毕=============offset={}'.format(offset))
	#return(urls_exists


if __name__=='__main__':
	manager = Manager()
	urls_exists = manager.list()
	counter_repetition = Value('d', 0.0)
	for offset in range(START,END+1):
		p= Process(target=main, args=(offset,urls_exists,counter_repetition))
		p.start()
		p.join()
	print("有效图片共计有：",len(urls_exists))
	print('节省了重复图片有:',counter_repetition.value)




