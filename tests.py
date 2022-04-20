a = {1:322,
     2: 152}

def test(dict1,key1):
	dict1[key1] = 'a'
	return dict1

print(test(a , 1))
print(a)