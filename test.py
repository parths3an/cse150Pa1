from heapq import *
a=[]
c=[(0,(2,3))]
heappush(a,(1,(3,4)))
heappush(a,(3,(2,3)))

for each in a:
	print ("each is: " + str(each) + str(c[0][0]) + " and p is: " + str(each[0]))
	if each[1] == c[0][1] and each[0] > c[0][0]:
		print ("is there and is big")
		a.remove(each)
		heapify(a) 
		print(a[0])
        heappush(c[0])
	else:
		print("did not work")
	
	