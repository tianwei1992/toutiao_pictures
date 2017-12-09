# coding: utf-8
from multiprocessing import Pool
from multiprocessing import Value
from multiprocessing import  Manager



def main(params):
    lst = params[0]
    offset = params[1]
    value+=1
    print ('in main,params,lst, offset:',params,lst, offset)
    print ('in main,value:',value)
    lst.append(offset)


if __name__ == '__main__':
    pool = Pool()
    manager = Manager()
    val=Value('d',10)
    lst = manager.list()

    pool_outputs = pool.map(main, [param for param in[(lst, l) for l in range(10)]])
    #pool_outputs = pool.map(main, [(lst, 1),(lst,2),(lst,3)])
    print (lst)
    print (val.value)

print(__name__)