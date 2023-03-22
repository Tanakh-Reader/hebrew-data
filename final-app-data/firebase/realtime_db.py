import firebase_admin
from firebase_admin import credentials, db

f = 'firebase-credentials.json'
cred = credentials.Certificate(f)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tanakh-reader-default-rtdb.firebaseio.com'
})

ref = db.reference(path='books/')

data = ref.get()

ref.set(

    {
        1: {'abbrLEB': 'GEN', 'abbrOSIS': 'gen', 'chapters': 50, 'bookId': 1, 'bookName': 'Genesis', 'bookNameHeb': 'ברשית', 'tanakhSort': 1},
        2: {'abbrLEB': 'GEN', 'abbrOSIS': 'gen', 'chapters': 50, 'bookId': 1, 'bookName': 'Genesis', 'bookNameHeb': 'ברשית', 'tanakhSort': 1}
    }
    
)

print(data)
