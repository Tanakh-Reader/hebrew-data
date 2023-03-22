import firebase_admin
from firebase_admin import credentials, firestore
import csv



def init_db() -> firestore.client:
    f = 'firebase-credentials.json'
    cred = credentials.Certificate(f)
    firebase_admin.initialize_app(cred)

    return firestore.client()


def get_etcbc_words(book_id:int) -> tuple[dict,list[list[dict]]]:

    book_words:dict = {}
    book_words_list:list[list[dict]] = []

    with open('word.csv', 'r') as csv_file:
        
        csv_rows = list( csv.DictReader(csv_file, delimiter=',') )
        
        for row in csv_rows:
            if row['book'] == str(book_id):
                book_words[row['wordId']] = row
                chapter = int(row['chKJV'])
                if len(book_words_list) >= chapter:
                    book_words_list[chapter-1].append(row)
                else:
                    book_words_list.append([row])

        return book_words, book_words_list


def set_word_data_as_documents(book_id:int):
    
    db = init_db()
    data, data_list = get_etcbc_words(book_id=book_id)
    print(list(data.values())[0])

    for key in data.keys():
        db.collection("bible").document(str(book_id)) \
            .collection('words').document(key) \
            .set(data[key])


# Only a few reads, no writes, verses # of documents + writes.
def set_word_data_as_list(book_id):

    db = init_db()
    data, data_list = get_etcbc_words(book_id=book_id)
    print(data_list[0][0])

    for chapter, words in enumerate(data_list):
        db.collection("bible").document(str(book_id)) \
            .collection('chapters').document(str(chapter+1)) \
            .set( {'words': words} )


# 1,50,Gen,Ge,Genesis,בראשית,Genesis
# 2,40,Exod,Ex,Exodus,שמות,Exodus
# 3,27,Lev,Le,Leviticus,ויקרא,Leviticus
# 4,36,Num,Nu,Numbers,במדבר,Numbers
# 5,34,Deut,Dt,Deuteronomy,דברים,Deuteronomy
# 6,24,Josh,Jos,Joshua,יהושע,Joshua
# 7,21,Judg,Jdg,Judges,שופטים,Judges
# 8,4,Ruth,Ru,Ruth,רות,1 Samuel


for book in {2}:
    set_word_data_as_list(book_id=book)