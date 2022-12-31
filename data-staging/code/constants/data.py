# from paths import PATHS 
import os 

class STEP_CORPUS:

    THOT_FILES_PREFIX = 'TOTHT'
    THOT_OG_HEADER = ['Ref in Heb', 'Eng ref', 'Pointed', 'Accented', 'Morphology', 'Extended Strongs']

    ID_ATTR = 'id'
    HEB_REF_ATTR = 'hebrewRef'
    ENG_REF_ATTR = 'englishRef'
    TEXT_ATTR = 'text'
    LEX_ATTR = 'lexText'
    TRAILER_ATTR = 'trailer'
    MORPH_ATTR = 'morph'
    GLOSS_ATTR = 'gloss'
    SENSE_GLOSS_ATTR = 'senseGloss'
    STRONGS_ATTR = 'strongs'
    TRAILER_STRONGS_ATTR = 'trailerStrongs'
    QERE_ATTR = 'qereData'

    THOT_COMBINED_HEADER = [
        ID_ATTR,
        HEB_REF_ATTR, 
        ENG_REF_ATTR, 
        TEXT_ATTR, 
        LEX_ATTR,
        TRAILER_ATTR, 
        MORPH_ATTR,
        GLOSS_ATTR, 
        SENSE_GLOSS_ATTR, 
        STRONGS_ATTR, 
        TRAILER_STRONGS_ATTR,
        QERE_ATTR
    ]

    WRITE_FILE_UNFORMATTED = 'translators-hebrew-OT-unformatted.tsv'
    WRITE_FILE_FORMATTED_WITHOUT_QERE = 'translators-hebrew-OT-no-qere.tsv'
    WRITE_FILE_FORMATTED = 'translators-hebrew-OT.tsv'

    WRITE_FILE_ALIGNMENT = 'translators-hebrew-OT-for-alignment.tsv'



class STEP_TBESH:

    TBESH_FILE_PREFIX = 'TBESH'
    TBESH_OG_HEADER = ['EStrong#', 'Hebrew', 'Transliteration', 'Morph', 'Gloss', 'Meaning']

    STRONGS_ATTR = 'strongs'
    LEX_ATTR = 'lexText'
    TRANSLITERATION_ATTR = 'transliteration'
    MORPH_ATTR ='morph'
    GLOSS_ATTR = 'gloss'
    MEANING_ATTR = 'definition'

    WRITE_FILE_UNFORMATTED = 'TBESH-unformatted.tsv'
    WRITE_FILE_FORMATTED = 'TBESH.tsv'
    

class CLEAR_CORPUS:

    HEBREW_TSV_FILE = 'macula-hebrew.tsv'
    HEBREW_TSV_SOURCE_PATH = os.path.join('TSV', HEBREW_TSV_FILE)

    ID_ATTR = 'xml:id'
    REF_ATTR = 'ref'
    TEXT_ATTR = 'text'

    WRITE_FILE_UNFORMATTED = 'macula-hebrew-unformatted.tsv'
    WRITE_FILE_ALIGNMENT = 'macula-hebrew-for-alignment.tsv'
    WRITE_FILE_FORMATTED = 'macula-hebrew.tsv'


class OHB_CORPUS:

    BHSA_EXTENDED_FILE = 'BHSA-with-extended-features.csv.zip'

    WRITE_FILE_UNFORMATTED = 'BHSA-with-extended-features-unformatted.tsv'
    WRITE_FILE_FORMATTED = 'BHSA-with-extended-features.tsv'


class ETCBC_CORPUS:

    ID_ATTR = 'id'
    TEXT_ATTR = 'text'
    PRS_ATTR = 'prs'
    TRAILER_ATTR = 'trailer'
    BOOK_ATTR = 'book'
    CHAPTER_ATTR = 'chapter'
    VERSE_ATTR = 'verse'

    HEADER = [
        ID_ATTR,
        TEXT_ATTR,
        PRS_ATTR,
        # TRAILER_ATTR,
        BOOK_ATTR,
        CHAPTER_ATTR,
        VERSE_ATTR
    ]

    WRITE_FILE_UNFORMATTED = 'BHSA-words-unformatted.tsv'
    WRITE_FILE_FORMATTED = 'BHSA-words.tsv'
    