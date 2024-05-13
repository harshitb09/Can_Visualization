import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import time

duration_seconds = 3
test_seconds = 12
start_time = time.time()
# Initialize Firebase Admin SDK
cred = credentials.Certificate("canreverse-86485-firebase-adminsdk-ir700-fbd6583c30.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://canreverse-86485-default-rtdb.firebaseio.com/'}
                              )

# Access the Database Reference
dk = "test"
ref = db.reference('realtime_data'+dk)

while True:
    # Download Data
    if ((time.time() - start_time) >= duration_seconds)<=0.01:
        data = ref.get()

        df = pd.DataFrame({"CANID":data})
        df['CANID'] = df['CANID'].explode()
        out = pd.DataFrame(df['CANID'].value_counts()).reset_index()
        out.to_excel('output.xlsx', sheet_name='CanID', index=False)

    if time.time() - start_time >= test_seconds:
        break