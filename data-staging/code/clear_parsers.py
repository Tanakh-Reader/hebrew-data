import pandas as pd
import os
import file_relocator
import csv
from constants.paths import PATHS
from constants.data import CLEAR_CORPUS

class ClearCorpusParser:

    def __init__(self):
        self.dest_path: str = PATHS.CLEAR_MACULA_HEBREW_DEST_FULL_PATH

    def write_corpus_data_unformatted(self) -> str:

        save_path = os.path.join(self.dest_path, CLEAR_CORPUS.WRITE_FILE_UNFORMATTED)
        fr = file_relocator.FileRelocator()

        # Copy Macula Hebrew 
        fr.copy_to_new_dir(
            source_path= os.path.join(
                PATHS.CLEAR_MACULA_HEBREW_SOURCE_DATA_FULL_PATH, 
                CLEAR_CORPUS.HEBREW_TSV_SOURCE_PATH),
            dest_path= save_path
        )

        return save_path

    def write_corpus_data_formatted(self):

        rows = []   
        source_file_path = os.path.join(self.dest_path, CLEAR_CORPUS.WRITE_FILE_UNFORMATTED)
        
        if CLEAR_CORPUS.WRITE_FILE_UNFORMATTED not in os.listdir(self.dest_path):
            self.write_corpus_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )     
            header = csv_rows[0] + ['book', 'chapter', 'verse']     

            for row_index, row in enumerate(csv_rows[1:]):
                # references formatted like: GEN 1:1!1
                ref = row[1]
                book, chapter_data = ref.split(' ')
                chapter, verse_data = chapter_data.split(':')
                verse = verse_data.split('!')[0]
                row += [book, chapter, verse]
                rows.append(row[0])

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = ['id','text','book','chapter','verse']
        write_file = CLEAR_CORPUS.WRITE_FILE_FORMATTED
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path

    def write_corpus_data_for_alignment(self):

        rows = []   
        source_file_path = os.path.join(self.dest_path, CLEAR_CORPUS.WRITE_FILE_UNFORMATTED)
        
        if CLEAR_CORPUS.WRITE_FILE_UNFORMATTED not in os.listdir(self.dest_path):
            self.write_corpus_data_unformatted()

        with open(source_file_path, 'r') as csv_file:
            
            csv_rows = list( csv.reader(csv_file, delimiter='\t') )     
            header = ['id', 'text', 'book', 'chapter', 'verse']     

            for row_index, row in enumerate(csv_rows[1:]):
                # references formatted like: GEN 1:1!1
                ref = row[1]
                book, chapter_data = ref.split(' ')
                chapter, verse_data = chapter_data.split(':')
                verse = verse_data.split('!')[0]
                row = [row[0], row[3], book, chapter, verse]
                rows.append(row)

        # Write the data.
        df = pd.DataFrame(rows, dtype=str)
        df.columns = header
        write_file = CLEAR_CORPUS.WRITE_FILE_ALIGNMENT
        save_path = os.path.join(self.dest_path, write_file)
        df.to_csv(save_path, sep='\t', encoding='utf-8', index=False)

        return save_path


parser = ClearCorpusParser()
parser.write_corpus_data_for_alignment()
