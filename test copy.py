from pos_tagging import pos_tagging
from DeviceSelection import DeviceSelection
from time import time

#Testing pos_tagging
R=('Noun', 'Modal', 'Verb')
S=('Will', 'Mary', 'Spot', 'Jane')
T=dict()
T['Start']={'Noun': 3/4, 'Modal': 1/4, 'Verb': 0, 'End': 0}
T['Noun']={'Noun': 1/9, 'Modal': 3/9, 'Verb': 1/9, 'End': 4/9}
T['Modal']={'Noun': 1/4, 'Modal': 0, 'Verb': 3/4, 'End': 0}
T['Verb']={'Noun': 1, 'Modal': 0, 'Verb': 0, 'End': 0}
E=dict()
E['Will']={'Noun': 1/4, 'Modal': 3/4, 'Verb': 0}
E['Mary']={'Noun': 1, 'Modal': 0, 'Verb': 0}
E['Spot']={'Noun': 1/2, 'Modal': 0, 'Verb': 1/2}
E['Jane']={'Noun': 1, 'Modal': 0, 'Verb': 0}
out={'Will': 'Modal', 'Mary': 'Noun', 'Spot': 'Verb', 'Jane': 'Noun'}

#Secondo dataset
# R = ('Noun', 'Modal', 'Verb', 'Article', 'Adjective')
# S = ('This', 'is', 'where', 'the', 'fun', 'begins', 'This2', 'is2', 'where2', 'the2', 'fun2', 'begins2')
# T = dict()
# T['Start'] = {'Noun': 3/5, 'Modal': 1/5, 'Verb': 0, 'Adjective': 0, 'Article': 1/5, 'End': 0}
# T['Noun'] = {'Noun': 2/10, 'Modal': 3/10, 'Verb': 2/10, 'Adjective': 0, 'Article': 1/10, 'End': 2/10}
# T['Modal'] = {'Noun': 2/6, 'Modal': 0, 'Verb': 3/6, 'Adjective': 0, 'Article': 1/6, 'End': 0}
# T['Verb'] = {'Noun': 2/6, 'Modal': 1/6, 'Verb': 0, 'Adjective': 0, 'Article': 2/6, 'End': 1/6}
# T['Adjective'] = {'Noun': 4/5, 'Modal': 0, 'Verb': 0, 'Adjective': 0, 'Article': 1/5, 'End': 0}
# T['Article'] = {'Noun': 9/10, 'Modal': 1/10, 'Verb': 0, 'Adjective': 0, 'Article': 0, 'End': 0}
# E = dict()
# E['This'] = {'Noun': 0, 'Modal': 1/2, 'Verb': 0, 'Adjective': 1/2, 'Article': 0}
# E['is'] = {'Noun': 0, 'Modal': 0, 'Verb': 1, 'Adjective': 0, 'Article': 0}
# E['where'] = {'Noun': 0, 'Modal': 1, 'Verb': 0, 'Adjective': 0, 'Article': 0}
# E['the'] = {'Noun': 0, 'Modal': 0, 'Verb': 0, 'Adjective': 0, 'Article': 1}
# E['fun'] = {'Noun': 1, 'Modal': 0, 'Verb': 0, 'Adjective': 0, 'Article': 0}
# E['begins'] = {'Noun': 1/3, 'Modal': 0, 'Verb': 2/3, 'Adjective': 0, 'Article': 0}
# E['This2'] = {'Noun': 0, 'Modal': 1/2, 'Verb': 0, 'Adjective': 1/2, 'Article': 0}
# E['is2'] = {'Noun': 0, 'Modal': 0, 'Verb': 1, 'Adjective': 0, 'Article': 0}
# E['where2'] = {'Noun': 0, 'Modal': 1, 'Verb': 0, 'Adjective': 0, 'Article': 0}
# E['the2'] = {'Noun': 0, 'Modal': 0, 'Verb': 0, 'Adjective': 0, 'Article': 1}
# E['fun2'] = {'Noun': 1, 'Modal': 0, 'Verb': 0, 'Adjective': 0, 'Article': 0}
# E['begins2'] = {'Noun': 1/3, 'Modal': 0, 'Verb': 2/3, 'Adjective': 0, 'Article': 0}
# out = {'This': 'Modal', 'is': 'Verb', 'where': 'Modal', 'the': 'Article', 'fun': 'Noun', 'begins': 'Verb', 'This2': 'Modal', 'is2': 'Verb', 'where2': 'Modal', 'the2': 'Article', 'fun2': 'Noun', 'begins2': 'Verb'}



start = time()
sol = pos_tagging(R, S, T, E)
end = time()-start

#print(sol)
if sol != out:
    print('FAIL')
else:
    print('True')
    print(end)




