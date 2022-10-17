# from paths import PATHS 
import os 

class STEP_CORPUS:

    CORPORA_PREFIX = 'TOTHT'
    CORPORA_OG_HEADER = ['Ref in Heb', 'Eng ref', 'Pointed', 'Accented', 'Morphology', 'Extended Strongs']

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

    CORPORA_HEADER = [
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

    WRITE_FILE_UNFORMATTED = 'translators-hebrew-OT-unformatted.csv'
    WRITE_FILE_FORMATTED_WITHOUT_QERE = 'translators-hebrew-OT-no-qere.csv'
    WRITE_FILE_FORMATTED = 'translators-hebrew-OT.csv'


class CLEAR_CORPUS:

    HEBREW_TSV_FILE = 'macula-hebrew.tsv'
    HEBREW_TSV_SOURCE_PATH = os.path.join('TSV', HEBREW_TSV_FILE)

    ID_ATTR = 'xml:id'
    REF_ATTR = 'ref'
    TEXT_ATTR = 'text'

    WRITE_FILE_UNFORMATTED = 'macula-hebrew-unformatted.tsv'
    WRITE_FILE_FORMATTED = 'macula-hebrew.tsv'
