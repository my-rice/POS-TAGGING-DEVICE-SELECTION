from pos_tagging import pos_tagging
from DeviceSelection import DeviceSelection
from time import time

def read_data(folder):
    f = open(folder + "/transition",'r')
    t = dict()
    t["Start"] = dict()
    words = f.readline().split()
    r = open(folder + "/roles", 'r')
    roles=[]
    for i in range(len(words)-1):
        roles.append(r.readline().strip())
    r.close()
    for i in range(len(words)-1):
        t['Start'][roles[i]]=float(words[i])
    t['Start']['End']=float(words[len(words)-1])
    j=0
    for line in f:
        t[roles[j]]=dict()
        words = line.split()
        for i in range(len(words)-1):
            t[roles[j]][roles[i]]=float(words[i])
        t[roles[j]]['End']=float(words[len(words)-1])
        j += 1
    f.close()

    f = open(folder + "/emission",'r')
    s = open(folder + "/sentence",'r')
    e = dict()
    j = s.readline().strip()
    for line in f:
        e[j] = dict()
        words = line.split()
        for i in range(len(words)):
            e[j][roles[i]] = float(words[i])
        j = s.readline().strip()
    f.close()
    s.close()

    return t, e

def read_sol(folder,r_num):
    f = open(folder + "/sol",'r')
    r = open(folder + "/roles", 'r')
    w = open(folder + "/sentence",'r')
    s = dict()
    words = f.readline().split()
    roles=[]
    for i in range(r_num):
        roles.append(r.readline().strip())
    r.close()
    for i in range(len(words)):
        s[w.readline().strip()]=roles[int(words[i])]
    f.close()
    w.close()

    return s

#Testing pos_tagging
# R=('Noun', 'Modal', 'Verb')
# S=('Will', 'Mary', 'Spot', 'Jane')
# T=dict()
# T['Start']={'Noun': 3/4, 'Modal': 1/4, 'Verb': 0, 'End': 0}
# T['Noun']={'Noun': 1/9, 'Modal': 3/9, 'Verb': 1/9, 'End': 4/9}
# T['Modal']={'Noun': 1/4, 'Modal': 0, 'Verb': 3/4, 'End': 0}
# T['Verb']={'Noun': 1, 'Modal': 0, 'Verb': 0, 'End': 0}
# E=dict()
# E['Will']={'Noun': 1/4, 'Modal': 3/4, 'Verb': 0}
# E['Mary']={'Noun': 1, 'Modal': 0, 'Verb': 0}
# E['Spot']={'Noun': 1/2, 'Modal': 0, 'Verb': 1/2}
# E['Jane']={'Noun': 1, 'Modal': 0, 'Verb': 0}
# out={'Will': 'Modal', 'Mary': 'Noun', 'Spot': 'Verb', 'Jane': 'Noun'}
folder = "dataset3"
T, E = read_data(folder)
R = tuple(T.keys())[1:len(T)]
S = tuple(E.keys())
start = time()
sol = pos_tagging(R, S, T, E)
end = time()-start
out = read_sol(folder,len(T)-1)
#print(R)
#print(S)

if sol != out:
    print('FAIL')
else:
    print('True')
    print(end)

#Testing DeviceSelection
# N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5')
# X = 7
# data = {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)}
# partition = [['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']]

# start = time()
# ds=DeviceSelection(N, X, data)
# C=ds.countDevices()
# subsets = [[] for i in range(C)]
# for i in range(C):
#     dev = ds.nextDevice(i)
#     while dev is not None:
#         subsets[i].append(dev)
#         dev = ds.nextDevice(i)
# end=time()-start

# if sorted(subsets) != sorted(partition):
#     print('FAIL')
# else:
#     print('True')
#     print(end)


#Testing DeviceSelection
def dominates(a, b):
    done = True
    for i in range(len(a)):
        if a[i] <= b[i]:
            done = False
            break
    return done

def verify(data,partition):
    try:
        devices = list(data.keys())
        for sets in partition:
            for i in range(len(sets)-1):
                if not dominates(data[sets[i]], data[sets[i+1]]):
                    return False
                devices.remove(sets[i])
            devices.remove(sets[len(sets)-1])
        if len(devices) != 0:
            return False
    except:
        return False
    return True

def dev_read_data():
    data = dict()
    f = open(folder + "data",'r')
    for line in f:
        sline=line.split()
        data[sline[0].strip()] = []
        for i in range(1, len(sline)):
            data[sline[0].strip()].append(int(sline[i]))
    f.close()
    return data

def dev_read_sol():
    sol = []
    f = open(folder + "devsol",'r')
    for line in f:
        sline=line.split()
        subset=[]
        for dev in sline:
            subset.append(dev.strip())
        sol.append(subset)
    f.close()
    return sol

# N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5')
# X = 7
# data = {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)}
# partition = [['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']]
folder = "dev_dataset1/"
data = dev_read_data()
N = tuple(data.keys())
X = len(data['D0'])

start = time()
ds=DeviceSelection(N, X, data)
C=ds.countDevices()
subsets = [[] for i in range(C)]
for i in range(C):
    dev = ds.nextDevice(i)
    while dev is not None:
        subsets[i].append(dev)
        dev = ds.nextDevice(i)
end=time()-start
partition = dev_read_sol()
if not verify(data, subsets) or C > len(partition):
    print('FAIL')
else:
    print('True')
    print(end)