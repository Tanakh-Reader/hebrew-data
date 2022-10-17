import firebase_admin
from firebase_admin import credentials, db

f = 'firebase-credentials.json'
cred = credentials.Certificate(f)
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

ref = db.reference(path='/')

data = ref.get()

print(data)
