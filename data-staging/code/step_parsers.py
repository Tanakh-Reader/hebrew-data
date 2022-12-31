from constants.paths import PATHS
from constants.data import STEP_CORPUS, STEP_TBESH
import pandas as pd
import csv
import os

class StepBibleCorpusProcessor:

    def __init__(self, corpora_files_path:str = PATHS.STEP_BIBLE_SOURCE_DATA_FULL_PATH):
        
        self.corpora_files_path = corpora_files_path
        self.corpora_files_dict = self.get_corpora_dict() if corpora_files_path else {}
        self.trailers = ['׃', 'פ', '׀', 'ס', ' פ', '׆', '־', ' ']
        self.dest_path = PATHS.STEP_DATA_DEST_FULL_PATH


    def get_corpora_dict(self):

        # Assuming file format 'TOTHT Gen-Deu - Translators OT Hebrew Tagged text - STEPBible.org CC BY.txt'
        corpora_dict = {
            'Gen': '',
            'Jos': '',
            'Job': '',
            'Isa': ''
        }

        # Assign the files to the references in the dictionary.
        for file in os.listdir(self.corpora_files_path):

            if STEP_CORPUS.THOT_FILES_PREFIX in file:

                for ref in corpora_dict.keys():

                    if ref in file:

                        corpora_dict[ref] = file

        return corpora_dict


    # Write all corpora files into a single corpus csv.
    def write_corpora_data_unformatted(self):

        cols_len = len(STEP_CORPUS.THOT_OG_HEADER)
        rows = []   
    
        for ref, file in self.corpora_files_dict.items():

            file_path = os.path.join(self.corpora_files_path, file)

            if not os.path.exists(self.corpora_files_path):
                raise Exception(f"{file_path} is not a valid path for {ref}")

            # Track when we've arrived at the Hebrew OT content in the file. 
            at_data = False
        
            with open(file_path) as f:

                lines = [line.rstrip('\n') for line in f]
                for line_index, line in enumerate(lines):

                    row = line.split('\t')

                    # E.g., 'Gen.1.14-16	Gen.1.14-16	וְשָׁנִים	וְ/שָׁנִֽים/׃	HC/Ncmpa	H9002=ו=and/H8141=שָׁנָה=year/H9016=׃=verseEnd'
                    if len(row) == cols_len and ref in row[0]:
                        at_data = True

                    if at_data and len(row) == cols_len:
                        rows.append(row)

            print('Complete: ' + file)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = STEP_CORPUS.THOT_OG_HEADER
        write_file = STEP_CORPUS.WRITE_FILE_UNFORMATTED
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path



    def write_corpora_data_formatted(self, with_qere:bool=True) -> str:

        rows = []   
        books_visited = set()
        source_file_path = os.path.join(self.dest_path, STEP_CORPUS.WRITE_FILE_UNFORMATTED)
        
        if STEP_CORPUS.WRITE_FILE_UNFORMATTED not in os.listdir(self.dest_path):
            self.write_corpora_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )            

            for row_index, row in enumerate(csv_rows[1:]):

                if row[0][-2:] != '.Q':

                    try:
                        words = row[3].split('/') # E.g., 'וְ/שָׁנִֽים/׃/'
                        morph_codes = row[4].split('/') # E.g., 'HC/Ncmpa'
                        strongs_data_combined = row[5].split('/') # E.g., 'H9002=ו=and/H8141=שָׁנָה=year/H9016=׃=verseEnd'

                    except Exception as e: 
                        print(e, row_index, row)

                    word_count = 0

                    data = {}

                    for i, word in enumerate(words): 

                        if word == '':
                            continue

                        try:

                            strongs_data = strongs_data_combined[i].split('=')
                            strongs_number = strongs_data[0]
                            lex_text = strongs_data[1]
                            
                            # E.g., 'H6086=עֵץ=tree_§2_tree' -> ['tree', '§2', 'tree']
                            gloss_data = strongs_data[2].split('_')
                            gloss = gloss_data[0]

                            sense_gloss = self.get_sense_gloss(gloss_data=gloss_data)
                        
                        except Exception as e: 
                            print(e, row_index, i, word, row, words, morph_codes)

                        # Faulty data:
                        # 2Ki.7.15-14.K	2Ki.7.15-14k	בְּהֵחָפְזָם	בְּ/הֵ/חָפְזָ/ם	HR/VNcc/Sp3mp	H9003=ב=in/H9009#1=ה=the/H2648=חָפַז=to hurry/H9048=Sp3m=they
                        if strongs_number == 'H9009#1':
                            continue

                        if word in self.trailers:

                            data[STEP_CORPUS.TRAILER_ATTR] += word 
                            data[STEP_CORPUS.TRAILER_STRONGS_ATTR] = strongs_number

                        else:

                            if data.get(STEP_CORPUS.TEXT_ATTR) != None:
                                rows.append(data)

                            data = {}

                            try:

                                morph = morph_codes[word_count] if len(words) > len(morph_codes) else morph_codes[i]

                                data[STEP_CORPUS.ID_ATTR] = self.create_node_id(row[0], books_visited, word_count)
                                data[STEP_CORPUS.HEB_REF_ATTR] = row[0]
                                data[STEP_CORPUS.ENG_REF_ATTR] = row[1]
                                data[STEP_CORPUS.TEXT_ATTR] = word 
                                data[STEP_CORPUS.LEX_ATTR] = lex_text 
                                data[STEP_CORPUS.TRAILER_ATTR] = '' if i != len(words) - 1 else ' '
                                data[STEP_CORPUS.MORPH_ATTR] = morph
                                data[STEP_CORPUS.GLOSS_ATTR] = gloss 
                                data[STEP_CORPUS.SENSE_GLOSS_ATTR] = sense_gloss
                                data[STEP_CORPUS.STRONGS_ATTR] = strongs_number
                                data[STEP_CORPUS.TRAILER_STRONGS_ATTR] = None
                                data[STEP_CORPUS.QERE_ATTR] = self.get_qere_data(csv_rows, row_index+1) if with_qere else ''

                            except Exception as e: 
                                print(e, row_index, i, word, row)

                            word_count += 1

                    rows.append(data)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        write_file = STEP_CORPUS.WRITE_FILE_FORMATTED if with_qere else STEP_CORPUS.WRITE_FILE_FORMATTED_WITHOUT_QERE
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path

    def write_corpora_data_for_alignment(self) -> str:

        rows: list = []   
        source_file_path: str = os.path.join(self.dest_path, STEP_CORPUS.WRITE_FILE_FORMATTED)
        
        if STEP_CORPUS.WRITE_FILE_FORMATTED not in os.listdir(self.dest_path):
            self.write_corpora_data_formatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )            

            header: list = ['id', 'text', 'book', 'chapter', 'verse']     

            for row_index, row in enumerate(csv_rows[1:]):
                # references formatted like: 1Ki.4.7-17.K
                ref: str = row[1]
                # Is ketiv or qere
                id: str = row[0]
                if ref[-1].upper() in ['K','Q']:
                    id: str = id + ref[-1].lower()
                    ref = ref[:-2]

                book, chapter, verse_data = ref.split('.')
                verse, position = verse_data.split('-')
                
                row: list = [id, row[3], book.upper(), chapter, verse]
                rows.append(row)


        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = header
        write_file = STEP_CORPUS.WRITE_FILE_ALIGNMENT
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path


    def get_qere_data(self, rows:list, index:int):

        if rows[index][0][-2:] != '.K':
            return ''

        qere_row = rows[index+1]
        qere_data = f"{qere_row[3]}.{qere_row[4]}.{qere_row[5]}"

        return qere_data


    # ref should look similar to 'Gen.1.14-16'
    def create_node_id(self, ref:str, books_visited:set, word_count:int):

        node_id = ''

        book, chapter, verse_data = ref.split('.')[:3]
        verse, verse_pos = verse_data.split('-')

        books_visited.add(book)
        book_num = len(books_visited)

        for item in [(book_num, 2), (chapter, 3), (verse, 3), (verse_pos, 3)]:
            ref_component, desired_length = item
            ref_padded = self.add_leading_zeros(str(ref_component), desired_length)
            node_id += ref_padded 
        
        return node_id + str(word_count + 1)

    
    def add_leading_zeros(self, ref_component:str, desired_length:int):

        zeros = ''
        for zero in range(desired_length - len(ref_component)):
            zeros += '0'

        return zeros + ref_component
    

    # gloss_data should look similar to ['tree', '§2', 'tree']
    def get_sense_gloss(self, gloss_data:list):

        sense_gloss = None 
        
        if len(gloss_data) == 2: # E.g., 'Media_§Madai@Gen.10.2'
            sense_gloss = gloss_data[1]
        elif len(gloss_data) == 3:
            sense_gloss = gloss_data[1] + '.' + gloss_data[2]

        if type(sense_gloss) is str:
            sense_gloss = sense_gloss.strip('§')

        return sense_gloss


class StepBibleLexiconProcessor:

    dest_path = PATHS.STEP_DATA_DEST_FULL_PATH

    def write_TBESH_data_unformatted(self, source_dir:str=PATHS.STEP_BIBLE_SOURCE_DATA_FULL_PATH):

        source_file = set(f for f in os.listdir(source_dir) if STEP_TBESH.TBESH_FILE_PREFIX in f).pop()
        source_file_path = os.path.join(source_dir, source_file)

        cols_len = len(STEP_TBESH.TBESH_OG_HEADER)
        rows = []
        at_data = False
        
        with open(source_file_path) as f:

            lines = [line.rstrip('\n') for line in f]
            for line_index, line in enumerate(lines):

                row = line.split('\t')
                row.pop()

                # E.g., 'H0002	אַב	av	A:N-M	father	1) father<br>'
                if len(row) == cols_len and row[0] == 'H0001':
                    at_data = True

                if at_data and len(row) == cols_len:
                    rows.append(row)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = STEP_TBESH.TBESH_OG_HEADER
        write_file = STEP_TBESH.WRITE_FILE_UNFORMATTED
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path


    def write_TBESH_data_formatted(self):

        rows = []   
        source_file_path = os.path.join(self.dest_path, STEP_TBESH.WRITE_FILE_UNFORMATTED)
        
        if STEP_TBESH.WRITE_FILE_UNFORMATTED not in os.listdir(self.dest_path):
            self.write_TBESH_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )            

            for row_index, row in enumerate(csv_rows[1:]):

                data = {}                    

                try:
                    data[STEP_TBESH.STRONGS_ATTR] = row[0]
                    data[STEP_TBESH.LEX_ATTR] = row[1] 
                    data[STEP_TBESH.TRANSLITERATION_ATTR] = row[2]
                    data[STEP_TBESH.MORPH_ATTR] = row[3]
                    data[STEP_TBESH.GLOSS_ATTR] = row[4]
                    data[STEP_TBESH.MEANING_ATTR] = row[5]

                except Exception as e: 
                    print(e, row_index, row)

                rows.append(data)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        write_file = STEP_TBESH.WRITE_FILE_FORMATTED
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path

stepParser = StepBibleCorpusProcessor() 
stepParser.write_corpora_data_for_alignment()