
def splitlist(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def splitnum(a, n):
    num, div = a, n
    return (num // div + (1 if x < num % div else 0)  for x in range (div))
    # result: [4, 4, 4, 3]

x =1
print(list(splitnum(x, int(x/2))))
