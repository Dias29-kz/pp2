i = int(input())
for j in range(i):
    sum = list(map(int, input().split()))
    c = sum[0]
    for c in range(sum):
        if sum > c:
            c = sum
        print(c)
        
