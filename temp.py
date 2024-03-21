a = [1,2,3,4,3,2,1]
n = 20
for i in range(n):
    print(a[i%7]*" ",end = "")
    print("*")