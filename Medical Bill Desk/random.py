
import random
l=[]
for k in range(0,101):
    a=random.randrange(0,200,10)*10
    if (a not in l) and (a != 0):
        l.append(a*0.1)

for i in l:
    print(i)

    

