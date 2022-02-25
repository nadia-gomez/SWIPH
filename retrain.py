# Set up to connect to django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'miguel.settings'
django.setup()

# Connect and manage the datbase
from swiph.models import BasicMachineLearningDB
import pandas as pd
import numpy as np

#Retrain the algorithm
from joblib import dump
from sklearn.ensemble import RandomForestClassifier

def retrain_classificator():
    dataBase = pd.DataFrame(list(BasicMachineLearningDB.objects.all().values()))

    target=np.array(dataBase['label_id'])

    del dataBase['id']

    del dataBase['label_id']

    dataBase = dataBase[['P_turb_des', 'T_cold_ref', 'asm', 'lat', 'lon', 'nModBoil']]
    headers = [col for col in dataBase.columns]
    data=dataBase.values

    forest=RandomForestClassifier(n_estimators=100,random_state=2)
    forest.fit(data,target)
    dump(forest, 'swiph/basic_classificator.joblib') 

    print("Finished retraining")
    print(f'Order of columns {headers}')

#Que pasa si se esta usando el basic_classificator cuando hace el dump?
retrain_classificator()
