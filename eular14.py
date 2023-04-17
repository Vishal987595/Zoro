import time
import matplotlib.pyplot as plt
tl = []
for i in range(7):
    t1 = time.time()
    lst = [1]
    mil = 10**i
    i = 2
    maxl = 1
    maxi = 1
    temp = 0
    j = 0
    while i <= mil:
        if i % 2 == 0:
            temp = 1 + lst[i//2 - 1]
            lst.append(temp)
        else:
            j = 3*i+1
            temp = 1
            while j >= i:
                if j%2 == 0:
                    j = j//2
                else:
                    j = 3*j+1
                temp = temp + 1
            temp = temp + lst[j-1]
            lst.append(temp)
        if temp > maxl:
            maxi = i
            maxl = temp
        i = i+1
    print(maxi, maxl)
    t2 = time.time()
    print("time for mil =", mil, ":", t2-t1)
    tl.append(t2-t1)

x = [10**i for i in range(7)]
plt.plot(x, tl)
plt.show()