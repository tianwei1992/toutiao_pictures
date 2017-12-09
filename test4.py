#test
#if we pass  a lst as a parameter to a funciotn and use lst.append in that ,
#the lst return is the original or the new?

lst1=[1,2]

def append_test(lst):
	lst.append(3)
	return lst

lst2=append_test(lst1)
print(lst2)
print(lst1)

#the output is as follows:
#[1, 2, 3]
#[1, 2, 3]
#that is to say
#lst1 can be  changed ,in this way.

print(list(range(0,5)))