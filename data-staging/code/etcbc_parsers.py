import pandas as pd
import os
import csv
from tf.app import use
from constants.paths import PATHS
from constants.data import ETCBC_CORPUS

VERSION: str = '2021'

class ETCBCCorpusParser:

    def __init__(self, version: str = VERSION):
        self.version: str = version
        self.dest_path: str = PATHS.ETCBC_DATA_DEST_FULL_PATH
    
    def __write_file(self, write_file: str) -> str:
        name, ext = os.path.splitext(write_file) 
        write_file = f'{name}-{self.version}{ext}'
        return write_file

    def init_app(self):
        A = use('bhsa', hoist=globals(), checkout='local', version=self.version, silent=True)

    def write_corpus_data_unformatted(self) -> str:
        
        try:
            A
        except NameError:
            self.init_app()

        rows: list = []

        for word_node in F.otype.s('word'):
            book, chapter, verse = T.sectionFromNode(word_node)
            text: str = F.g_word_utf8.v(word_node)
            prs: str = F.prs.v(word_node)
            rows.append([word_node, text, prs, book, chapter, verse])


        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = ETCBC_CORPUS.HEADER
        write_file = self.__write_file(ETCBC_CORPUS.WRITE_FILE_UNFORMATTED)
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path

    def write_corpus_data_formatted(self):

        rows = []   
        saved_file = self.__write_file(ETCBC_CORPUS.WRITE_FILE_UNFORMATTED)
        source_file_path = os.path.join(self.dest_path, saved_file)
        
        if saved_file not in os.listdir(self.dest_path):
            self.write_corpus_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )

            for row_index, row in enumerate(csv_rows[1:]):
                prs = row[2]
                book = row[3].replace('_','').upper()[:3]
                book = {'EZE':'EZK','JUD':'JDG','SON':'SNG','JOE':'JOL','NAH':'NAM'}[book] if book in ('EZE','JUD','SON','JOE','NAH') else book
                row[3] = book
                rows.append(row)
                # if prs not in ('absent', 'n/a'):
                #     modified_row = row.copy()
                #     modified_row[0] = modified_row[0] + 's'
                #     modified_row[1] = ''
                #     rows.append(modified_row)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = ETCBC_CORPUS.HEADER
        write_file = self.__write_file(ETCBC_CORPUS.WRITE_FILE_FORMATTED)
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path


parser = ETCBCCorpusParser(version='2021')

# parser.init_app()

# parser.write_corpus_data_formatted()
