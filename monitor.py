import os

class Monitor(): # Monitor struct
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
    def __str__(self):
        return self.name +" : "+ str(self.x) + " " + str(self.y) + " " + str(self.width) + " "+ str(self.height)

def squarit(n: int):
    """
    Code from Stackoverflow @CedricDruck
    """
    import math
    size = int(math.floor(math.sqrt(n)))
    ans = [n//size]*size
    for i in range(n-n//size*size):
        ans[i] += 1
    return size, ans

for i in range(4, 25):
  print(f'{i}: {squarit(i)}')

def getParenthesis(texte):
    content = None
    p1 = texte.find('(')
    if p1 >= 0:
        p2 = texte.find(')')
        if p2 > p1:
            content = texte[p1:p2+1]
    return content

def monitorsInfo():
    # for linux
    import subprocess
    commande = ['xrandr','--listmonitors']
    res = subprocess.check_output(commande, shell=True).decode().split('\n')

    monitors = {}

    for l in res:
        if len(l) > 1:
            if l[0] != ' ':
                if l.split()[0] == l.split()[0].upper():

                    options = getParenthesis(l)
                    if options:
                        l = l.replace(options, '')
                    z = l.split()

                    # this is a connector
                    name = z[0]
                    conn = None
                    primary = None
                    geo = None
                    size = None
                    width = height = offsetx = offsety = None
                    if z[1].lower() == 'connected':
                        conn = True
                        # monitor in use :-)
                    else:
                        # screeen connection exists, no screen used
                        conn = False
                    # for connected screens : get extra data
                    if conn:
                        if z[2].lower() == 'primary':
                            primary = True
                            z.pop(2)
                        # other data for connected screeens
                        geo = z[2]   # get rid of extra 'primary'
                        size = ''.join(z[3:])
                        # get width and height
                        z = geo.split('+')
                        offsetx = int(z[1])
                        offsety = int(z[2])
                        z = z[0].split('x')
                        width = int(z[0])
                        height = int(z[1])


                    # create a dict per monitor
                    d = {}
                    d['name'] = name
                    d['connected'] = conn
                    d['primary'] = primary
                    d['geometry'] = geo
                    d['options'] = options
                    d['size'] = size
                    d['width'] = width
                    d['height'] = height
                    d['offsetx'] = offsetx
                    d['offsety'] = offsety

                    monitors[name] = d
    return monitors

def detect_monitors():
    # get all screens, with offset and resolution
    if os.name == 'nt':
        from screeninfo import get_monitors
        return get_monitors()
    else:
        # Linux/ubuntu command
        monitor_list = []
        monitors = monitorsInfo()

        for monitor in monitors:
            if monitors[monitor]["connected"]:
                monitor_list.append(Monitor(x=monitors[monitor]["offsetx"], y=monitors[monitor]["offsety"], width=monitors[monitor]["width"], height=monitors[monitor]["height"],name=monitor))
        return monitor_list

def get_monitors_to_use(monitor_list, MONITOR_INDEX_LIST):
    # filter on the monitor index list
    if MONITOR_INDEX_LIST:
        res_list = []
        for i in range(0,len(monitor_list)):
            res_list.append(monitor_list[MONITOR_INDEX_LIST[i]])
    else:
        return monitor_list

def split_monitors(monitor_list, source_list, MONITOR_INDEX_LIST):
    # This function is an algoritm for splitting up any amount of screens into even boxes.
    monitor_box_list = []
    camera_amount = len(source_list)
    monitor_list = get_monitors_to_use(monitor_list, MONITOR_INDEX_LIST)
    monitor_amount = len(monitor_list)

    cameras_per_monitor_split = list(splitlist(source_list, monitor_amount))

    for i in range(0,len(cameras_per_monitor_split)):
        if len(cameras_per_monitor_split[i]) == 1:
            cameras_on_monitor_divide = [1]
        else:
            cameras_on_monitor_divide = get_dim_arr(len(cameras_per_monitor_split[i]))

        # Divide monitor into N boxes
        for j in range(0,len(cameras_on_monitor_divide)): # rows
            for k in range(0,cameras_on_monitor_divide[j]): # columns
                camera_width = int(monitor_list[i].width/cameras_on_monitor_divide[j])
                camera_height = int(monitor_list[i].height/len(cameras_on_monitor_divide))
                x= monitor_list[i].x + k*camera_width
                y= monitor_list[i].y + j*camera_height
                h= y+camera_height
                w= x+camera_width

                monitor_box_list.append([x,y,w,h])
    return monitor_box_list

def get_dim_arr(x):
    """
    split number into array
    """
    curr = 1
    res_arr = [1]
    while curr < x:
        val, idx = min((val, idx) for (idx, val) in enumerate(res_arr))
        #print(res_arr)

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

    return res_arr


def splitnum(a, n):
    """
    Split numbers into even divided numbers
    """
    num, div = a, n
    return (num // div + (1 if x < num % div else 0)  for x in range (div))

def splitlist(a, n):
    """
    Simple split array into even sizes
    """
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
