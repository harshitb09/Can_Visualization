import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("canreverse-86485-firebase-adminsdk-ir700-fbd6583c30.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://canreverse-86485-default-rtdb.firebaseio.com/'}
                              )

def get_data():
    
  # Access the Database Reference
    dk = "test"
    ref = db.reference('realtime_data'+dk)
    data = ref.get()

    df = pd.DataFrame({"CANID":data})
    df['CANID'] = df['CANID'].explode()
    out = pd.DataFrame(df['CANID'].value_counts()).reset_index()
    can_data = out.to_dict(orient='records')
    return can_data