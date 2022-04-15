import library
import pandas as pd
import numpy as np

result_log = pd.DataFrame()

for i in range(1,100):
    log1 = library.PassIndex()
    log1.generate()
    log1.discrete_value()
    # log1.show()

    _,Guardtime = log1.Guardtime()
    _,Defdist = log1.Defdist()
    _,Closestenemydist = log1.Closestenemydist()
    _,Shoot_dir = log1.Shoot_dir()
    _,Passlinedist = log1.Passlinedist()
    Goal = log1.Goal()

    a = {'Guardtime':Guardtime,'Defdist':Defdist,'Closestenemydist':Closestenemydist,'Shoot_dir':Shoot_dir,'Passlinedist':Passlinedist,'Goal':Goal}
    result_log = result_log.append(a,ignore_index=True)
print(result_log)

def ent(data):
    prob1 = pd.value_counts(data)/len(data)
    return sum(np.log2(prob1)*prob1*(-1))

def gain(data,str1,str2):
    e1 = data.groupby(str1).apply(lambda x:ent(x[str2]))
    p1 = pd.value_counts(data[str1])/len(data[str1])
    e2 = sum(e1*p1)
    return ent(data[str2]) - e2

print(gain(result_log,'Guardtime','Goal'))