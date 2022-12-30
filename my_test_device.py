from pos_tagging import pos_tagging
from DeviceSelection import DeviceSelection
from time import time

N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5', 'Device 6', 'Device 7', 'Device 8')
X = 4
data = {'Device 1': (3, 3), 'Device 2': (2, 1), 'Device 3': (1, 2), 'Device 4': (4, 2), 'Device 5': (1, 1), 'Device 6': (4, 3), 'Device 7': (2, 2), 'Device 8': (1, 1)}
partition = [['Device 1', 'Device 7', 'Device 5'], ['Device 4', 'Device 2'], ['Device 6', 'Device 3'], ['Device 8']]
#Dataset 2
# N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5', 'Device 6', 'Device 7', 'Device 8', 'Device 9', 'Device 10')
# X = 5
# data = {'Device 1': (11, 20, 8), 'Device 2': (12, 0, 2), 'Device 3': (48, 1, 1), 'Device 4': (10, 9, 8), 'Device 5': (10, 10, 6), 'Device 6': (1, 32, 0), 'Device 7': (5, 7, 9), 'Device 8': (4, 6, 3), 'Device 9': (7, 12, 18), 'Device 10': (0, 1, 1)}
# partition = [['Device 4', 'Device 8', 'Device 10'], ['Device 1', 'Device 5'], ['Device 9', 'Device 7'], ['Device 2'], ['Device 3'], ['Device 6']]
# #Testing DeviceSelection
# N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5')
# X = 7
# data = {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)}
# partition = [['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']]
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
print(C)
print(subsets)
if sorted(subsets) != sorted(partition):
    print('FAIL')
else:
    print('True')
    print(end)