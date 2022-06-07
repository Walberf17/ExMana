a = [1,2,3]

b = [3,4,5]

def test():
	for el in a:
		if el in b:
			return True

print(test())