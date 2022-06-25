import matplotlib.pyplot as plt


x = 2
soma = 0
xs = []
ys = []
counters = 0
while round(x , 5 ) > 0:
	xs.append(x)
	x*= 0.9
	soma += x
	ys.append(x)
	counters += 1

print(counters)
print(soma , 'soma')

print('')

plt.plot(xs)
# plt.scatter(xs , ys)
plt.show()