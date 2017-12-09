from multiprocessing import Pool,Manager,Value,Process

#lst = []
#foo = 0

def main(lst,num,offset):
	lst.append(offset)
	num.value+=1
	print("lst in main：",lst)
	print('num.value main:',num.value)


if __name__=='__main__':
	manager = Manager()
	lst = manager.list()
	num = Value('d', 0.0)
	for offset in range(0,4):
		p= Process(target=main, args=(lst,num, offset))
		p.start()
		p.join()
	#results=pool.map(main,[param for param in [(lst,num,l) for l in (1,2,3)]])
	#pool_outputs = pool.map(main, [param for param in[(lst, l) for l in range(10)]])
	lst.append(10)
	print("lst：",lst)
	print('num.value:',num.value)




