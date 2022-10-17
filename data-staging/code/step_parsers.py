from constants import *
import pandas as pd
import csv

class StepBibleHebrewDataProcessor:

    def __init__(self, corpora_files_path:str, lexicon_file_path:str=None):
        
        self.lexicon_file_path = lexicon_file_path
        self.corpora_files_path = corpora_files_path
        self.corpora_files_dict = self.get_corpora_dict()
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

            if STEP_CORPORA.CORPORA_PREFIX in file:

                for ref in corpora_dict.keys():

                    if ref in file:

                        corpora_dict[ref] = file

        return corpora_dict


    # Write all corpora files into a single corpus csv.
    def write_corpora_data_unformatted(self):

        cols_len = len(STEP_CORPORA.CORPORA_OG_HEADER)
        rows = []   

        for ref, file in self.corpora_files_dict.items():

            file_path = os.path.join(self.corpora_files_path, file)
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
        df = pd.DataFrame(rows)
        df.columns = STEP_CORPORA.CORPORA_OG_HEADER
        write_file = STEP_CORPORA.WRITE_FILE_UNFORMATTED
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep=',', encoding='utf-8', index=False)

        return save_path



    def write_corpora_data_formatted(self, with_qere:bool=True):

        rows = []   
        books_visited = set()
        source_file_path = os.path.join(self.dest_path, STEP_CORPORA.WRITE_FILE_UNFORMATTED)
        
        if STEP_CORPORA.WRITE_FILE_UNFORMATTED not in os.listdir(self.dest_path):
            self.write_corpora_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file) )            

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

                            data[STEP_CORPORA.TRAILER_ATTR] += word 
                            data[STEP_CORPORA.TRAILER_STRONGS_ATTR] = strongs_number

                        else:

                            if data.get(STEP_CORPORA.TEXT_ATTR) != None:
                                rows.append(data)

                            data = {}

                            try:

                                morph = morph_codes[word_count] if len(words) > len(morph_codes) else morph_codes[i]

                                data[STEP_CORPORA.ID_ATTR] = self.create_node_id(row[0], books_visited, word_count)
                                data[STEP_CORPORA.HEB_REF_ATTR] = row[0]
                                data[STEP_CORPORA.ENG_REF_ATTR] = row[1]
                                data[STEP_CORPORA.TEXT_ATTR] = word 
                                data[STEP_CORPORA.LEX_ATTR] = lex_text 
                                data[STEP_CORPORA.TRAILER_ATTR] = '' if i != len(words) - 1 else ' '
                                data[STEP_CORPORA.MORPH_ATTR] = morph
                                data[STEP_CORPORA.GLOSS_ATTR] = gloss 
                                data[STEP_CORPORA.SENSE_GLOSS_ATTR] = sense_gloss
                                data[STEP_CORPORA.STRONGS_ATTR] = strongs_number
                                data[STEP_CORPORA.TRAILER_STRONGS_ATTR] = None
                                data[STEP_CORPORA.QERE_ATTR] = self.get_qere_data(csv_rows, row_index+1) if with_qere else ''

                            except Exception as e: 
                                print(e, row_index, i, word, row)

                            word_count += 1

                    rows.append(data)

        # Write the data.
        df = pd.DataFrame(rows)
        write_file = STEP_CORPORA.WRITE_FILE_FORMATTED if with_qere else STEP_CORPORA.WRITE_FILE_FORMATTED_WITHOUT_QERE
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep=',', encoding='utf-8', index=False)

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