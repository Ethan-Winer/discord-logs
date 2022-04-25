import pickle
x = {}
with open('./files/logs.pickle', 'wb') as file:
    pickle.dump(x,file)