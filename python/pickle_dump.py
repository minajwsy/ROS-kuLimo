import pickle

name = 'James'
age = 57
address = '서울시 서초구 잠원동'
scores = {'korean': 90, 'english': 95, 'math': 85, 'science': 82}

with open('james.pk', 'wb') as file:
    pickle.dump(name, file)
    pickle.dump(age, file)
    pickle.dump(address, file)
    pickle.dump(scores, file)