#check_pic_number.py
#核对数据库和本地目录里的图片数量
from config import *
from pymongo import MongoClient
import os



#第一步：从MongoDB中拿出图片的url
#构造一个MongoClient对象，用于与服务器建立连接
client=MongoClient(MONGO_URL)
#创建一个名叫MONGO_DB的数据库
db=client[MONGO_DB]

def get_item_from_db():
#在表中查找，返回一个个字典
	for i,item in enumerate(db[MONGO_TABLE].find()):
		#提取需要的'pic_url'字段
		#i是数据库的记录号
		for j,pic_url in enumerate(item['pic_url']):
			#j是图片在记录里的次序
			#print (i, j, pic_url)
			yield(i,j,pic_url)

def get_pure_urls_from_db():
	lst=[]
	for item in db[MONGO_TABLE].find():
		#提取需要的'pic_url'字段
		#i是数据库的记录号
		for pic_url in item['pic_url']:
			#j是图片在记录里的次序
			#print (i, j, pic_url)
			lst.append(pic_url)
	return lst


def get_pure_urls_from_local():
	lst=[]
	filepath='D://pics2//'
	pathDir = os.listdir(filepath)
	for url_local in pathDir:
		lst.append(url_local.rstrip('.jpg')[-10:])
	return lst

def get_info_list_from_local():
	lst = []
	filepath = 'D://pics2//'
	pathDir = os.listdir(filepath)
	for url_local in pathDir:
		#offset,page_index,pic_index,pic_url=(url_local.split('_'))
		lst.append(url_local.split('_'))
	return lst

def check_exists(pic_urls_in_db):
	i, j, url_db=pic_urls_in_db
	#对每个url_db，查看本地是否有对应的，返回true
	url_db_tail=url_db[-10:]
	filepath='D://pics2//'
	pathDir = os.listdir(filepath)
	#取出每个本地文件名，以最后10个字符作为特征，看能否找到和传入的url匹配
	#找不到就是未下载
	#查看本地存储的图片数量
	#print(len(pathDir))
	print('url_db_tail===',url_db_tail)
	for url_local in pathDir:
		url_local_tail=url_local.rstrip('.jpg')[-10:]
		if url_db_tail in url_local_tail:
			print(url_local_tail)
			#数据库记录从1开始编号，所以i+1
			#print("数据库中第{0}条记录，第{1}号图片已下载，url为{2}".format(i+1,j,url_db))
			return
	print("数据库中第{0}条记录，第{1}号图片不存在，url为{2}".format(i+1,j,url_db))


def find_duplication(mylist):
	print('原本共有{0}项，下面进行去重……'.format(len(mylist)))
	myset = set(
		mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
	count=0
	print('去重以后，还剩{0}条记录'.format(len(myset)))
	for item in myset:
		if not mylist.count(item)==1:
			#print("the %s has found %d" %(item,mylist.count(item)))
			count=count+mylist.count(item)
	print("其中重复项有:"+str(count/2))

def find_duplication_detail(lst):
	#用集合构造一个不重复的url池，作为标准
	urls=[item[-1] for item in lst]
	urls_set=set(urls)
	#lst_total是本函数的返回，包含有关重复的全部信息
	lst_total=[]
	for url in urls_set:
		counter=0
		#对集合里的每个url依次处理
		#每发现1个重复都append到这个lst里
		lst_item=[]
		for item in lst:
			if url==item[-1]:
				#没找到1个匹配，计数器+1，并吧相关信息加入列表
					counter+=1
					lst_item.append(item)
		#在遍历完成之后，通过counter判断是否有重复，以及有几个重复
		#只有重复才构造dic输出，不重复没必要输出
		if counter>1:
			dic = {}
			dic['url'] = url
			dic['dupicated_item']=lst_item
			dic['count_total']=counter
			lst_total.append(dic)
	print("经过比较，重复项具体有：")
	for item in lst_total:
		print(item)





def main():
	urls_count_db=0
	counter=0
	for i in db[MONGO_TABLE].find():
		urls_count_db=urls_count_db+len(i['pic_url'])
	print('数据库中的总条数是;',urls_count_db)
	#数据库中86，文件夹67，也就是其中有19个没有下载下来
	for pic_infos_in_db in get_item_from_db():
		print("进入")
		#print (pic_infos_in_db)
		print('开始查找数据库中第{0}个url'.format(counter+1))
		check_exists(pic_infos_in_db)
		print('查找完毕，数据库中第{0}个url'.format(counter+1))
		counter += 1
		print()


	print("好奇怪，难道86个url有重复？查一查吧")
	pure_urls_from_db=get_pure_urls_from_db()
	print('对数据库查重，结果如下：')
	find_duplication(pure_urls_from_db)
	print()

	print("那为什么图片有67张？反过来查查哪些是本地图片里有，但是数据库里没有的吧？")
	print()
	pure_urls_from_local=get_pure_urls_from_local()
	print('对本地目录查重，结果如下：')
	find_duplication(pure_urls_from_local)
	print()

	print("好吧，问题找到了，实际上就只有53张图片，其他都是有重复的")
	print('如果过分一点……想知道本地目录里，到底哪些项重复了?')
	print()
	print("开始对本地目录查找具体重复项……")
	#print(get_info_list_from_local())
	find_duplication_detail(get_info_list_from_local())

if __name__=='__main__':
	main()


#对每一个url提取最后4位，查找是否有匹配的文件，如果没有把图片url和分页url一起打印出来



