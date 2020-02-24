
def splitlist(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def splitnum(a, n):
    num, div = a, n
    return (num // div + (1 if x < num % div else 0)  for x in range (div))
    # result: [4, 4, 4, 3]

#x =20
#print(list(splitnum(x, int(x/2))))

def get_dim_arr(x):
    curr = 1
    res_arr = [1]
    while curr < x:
        val, idx = min((val, idx) for (idx, val) in enumerate(res_arr))
        print(res_arr)

        if(val > len(res_arr)): # if abs(row, col) >= 1
            # split
            temp = []
            for i in range(0,len(res_arr)):
                if i == 0:
                    temp.append(res_arr[i])
                else:
                    temp.append(res_arr[i]-1)
            temp.append(res_arr[i]-1)
            res_arr = temp
        else:
            val+=1
            res_arr[idx] = val
        curr+=1

    return [len(res_arr), res_arr]

x = 20
print(get_dim_arr(x))

# data pattern TABLE
# INPUT => OUTPUT (len(array), array )
# 1 => 1 1
# 2 => 1 2
# 3 => 2 2,1
# 4 => 2 2,2
# 5 => 2 3,2
# 6 => 2 3,3
# 7 => 3 3,2,2
# 8 => 3 3,3,2
# 9 => 3 3,3,3
# 10 => 3 4,3,3
# 11 => 3 4,4,3
# 12 => 3 4,4,4
# 13 => 4 4,3,3,3
# 14 => 4 4,4,3,3
# 15 => 4 4,4,4,3
# 16 => 4 4,4,4,4
# 17 => 4 5,4,4,4
# 18 => 4 5,5,4,4
# 19 => 4 5,5,5,5
# 20 => 4 5,5,5,5
