import os 
from pathlib import Path

# General Directories
PROJECT_ROOT_DIR = 'hebrew-data'

DATA_STAGING_DIR = 'data-staging'
DATA_DIR = 'data'
SOURCES_DIR = 'sources'
CODE_DIR = 'code'
COMPARISONS_DIR = 'comparisons'

# Data Source Directories
STEP_DIR = 'STEP-Bible'
CLEAR_DIR = 'Clear-Bible'
WONG_DIR = 'Eliran-Wong'

# Data Source Relative Paths
STEP_CORE_SOURCE_DATA_PATH = 'step/step-core-data/src/main/resources/com/tyndalehouse/step/core/data/create'
STEP_BIBLE_SOURCE_DATA_PATH = 'STEPBible-Data'
CLEAR_MACULA_HEBREW_SOURCE_DATA_PATH = 'macula-hebrew'
WONG_OHB_SOURCE_DATA_PATH = 'OpenHebrewBible'

class PATHS:

    # General Paths
    SELF_FULL_PATH = Path(__file__)
    PROJECT_ROOT_FULL_PATH = [p for p in SELF_FULL_PATH.parents if p.parts[-1]==PROJECT_ROOT_DIR][0]

    # Data Staging Paths
    HEBREW_DATA_FULL_PATH = os.path.join(PROJECT_ROOT_FULL_PATH, DATA_STAGING_DIR)
    HEBREW_DATA_DATA_FULL_PATH = os.path.join(HEBREW_DATA_FULL_PATH, DATA_DIR)
    HEBREW_DATA_SOURCES_FULL_PATH = os.path.join(HEBREW_DATA_FULL_PATH, SOURCES_DIR)
    HEBREW_DATA_CODE_FULL_PATH = os.path.join(HEBREW_DATA_FULL_PATH, CODE_DIR)
    HEBREW_DATA_COMPARISONS_FULL_PATH = os.path.join(HEBREW_DATA_DATA_FULL_PATH, COMPARISONS_DIR)

    # STEP Paths
    STEP_CORE_SOURCE_DATA_FULL_PATH = os.path.join(HEBREW_DATA_SOURCES_FULL_PATH, STEP_DIR, STEP_CORE_SOURCE_DATA_PATH)
    STEP_BIBLE_SOURCE_DATA_FULL_PATH = os.path.join(HEBREW_DATA_SOURCES_FULL_PATH, STEP_DIR, STEP_BIBLE_SOURCE_DATA_PATH)

    STEP_DATA_DEST_FULL_PATH = os.path.join(HEBREW_DATA_DATA_FULL_PATH, STEP_DIR)

    # CLEAR Paths
    CLEAR_MACULA_HEBREW_SOURCE_DATA_FULL_PATH = os.path.join(HEBREW_DATA_SOURCES_FULL_PATH, CLEAR_DIR, CLEAR_MACULA_HEBREW_SOURCE_DATA_PATH)
    
    CLEAR_MACULA_HEBREW_DEST_FULL_PATH = os.path.join(HEBREW_DATA_DATA_FULL_PATH, CLEAR_DIR)

    # Wong Paths 
    WONG_OHB_SOURCE_DATA_FULL_PATH = os.path.join(HEBREW_DATA_SOURCES_FULL_PATH, WONG_DIR, WONG_OHB_SOURCE_DATA_PATH)

    WONG_OHB_DEST_FULL_PATH = os.path.join(HEBREW_DATA_DATA_FULL_PATH, WONG_DIR)
