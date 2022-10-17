import pandas as pd
import unicodedata 
import os
from constants.paths import PATHS


def heb_stripped(word):

    normalized = unicodedata.normalize('NFKD', word)

    return ''.join([c for c in normalized if not unicodedata.combining(c)])


class WordFileParser:

    og_crawl_depth = 1
    # According to index == case.
    word_cases = ["Same", "Dif markings", "Dif spelling", "Dif word, next same", "Dif word, next not same"]

    def __init__(self, file:str, word_col:str, id_col:str, name:str):

        self.df = pd.read_csv(
            file, 
            sep=self.__get_sep(file), 
            na_filter=False,
            encoding='utf-8',
            usecols=[word_col, id_col],
            dtype=str)
        self.words = self.df[word_col].to_list()
        self.ids = self.df[id_col].to_list()
        self.words_output = []
        self.ids_output = []
        self.cases_output = []
        self.i = 0
        self.crawl_depth = self.og_crawl_depth
        self.length = len(self.words)
        self.name = name


    def __get_sep(self, file:str) -> str:

        if file.endswith('.csv'):
            return ','
        elif file.endswith('.tsv'):
            return '\t'
        # TODO raise error


    def word(self, i:int=None) -> str:

        if i:
            return self.words[i]

        return self.words[self.i]


    def ref(self, i:int=None) -> str:

        if i:
            return self.ids[i]

        return self.ids[self.i]


    def reset_crawl_depth(self):

        self.crawl_depth = self.og_crawl_depth


    def update_output_lists(self, values:list):
        
        self.words_output.append(values[0])
        self.ids_output.append(values[1])
        self.cases_output.append(values[2])


    def word_comparison(self, other_wfp:'WordFileParser', new_index:int=0) -> int:
        
        other_index = max(other_wfp.i, new_index)
        word_a = self.word()
        word_b = other_wfp.word(other_index)

        if word_a == word_b:
            return 0

        else:

            word_a_cons = heb_stripped(word_a)
            word_b_cons = heb_stripped(word_b)

            if word_a_cons == word_b_cons:
                return 1

            elif 0 in [len(word_a_cons), len(word_b_cons)]:
                return 4

            elif len(word_a_cons) > 1 and len(word_b_cons) > 1 and word_a_cons[0] == word_b_cons[0]:

                if word_a_cons[-1] == word_b_cons[-1] or len(word_a_cons) == len(word_b_cons):
                    return 1
                
                else:
                    return 2

            elif self.i + 1 < self.length and other_wfp.i + 1 < other_wfp.length \
            and heb_stripped(self.word(self.i+1)) == heb_stripped(other_wfp.word(other_index+1)):
                return 3

            else:
                return 4


    def crawl(self, other_wfp:'WordFileParser', again=False):
        
        depth = 0
        runner_index = other_wfp.i + 1

        while depth < self.crawl_depth and runner_index < other_wfp.length:

            comp = self.word_comparison(other_wfp, new_index=runner_index)

            if comp == 0 or (again and comp in [1,2,3]):
                self.update_comparisons(other_wfp, comp, runner_index)
                return True
                
            runner_index += 1
            depth += 1
        
        return False

            
    def update_comparisons(self, other_wfp:'WordFileParser', comp:int, new_index:int=0):

        while other_wfp.i < new_index:
            other_wfp.update_output_lists([other_wfp.word(), other_wfp.ref(), 4])
            self.update_output_lists(['NA', self.ref(), 4])
            other_wfp.i += 1
            
        if comp in range(4):

            other_wfp.update_output_lists([other_wfp.word(), other_wfp.ref(), comp])
            self.update_output_lists([self.word(), self.ref(), comp])
            self.i += 1
            other_wfp.i += 1

            return True
        
        else:
            return None


    def add_row(self, other_wfp:'WordFileParser'):
        
        other_wfp.update_output_lists([other_wfp.word(), other_wfp.ref(), 5])
        self.update_output_lists([self.word(), self.ref(), 5])
        self.i += 1
        other_wfp.i += 1

    
class FileComparisons:

    dest_path = PATHS.HEBREW_DATA_COMPARISONS_FULL_PATH

    def write_WFP_comparisons(self, wfp1:WordFileParser, wfp2:WordFileParser):
        
        while wfp1.i < wfp1.length and wfp2.i < wfp2.length:
            
            comp = wfp1.word_comparison(wfp2)
            
            if not wfp1.update_comparisons(wfp2, comp):

                while wfp1.crawl_depth <= 3:
                    if wfp1.crawl(wfp2):
                        break
                    elif wfp2.crawl(wfp1):
                        break
                    elif wfp1.crawl(wfp2, again=True):
                        break
                    elif wfp2.crawl(wfp1, again=True):
                        break
                    wfp1.crawl_depth += 1
                    wfp2.crawl_depth += 1
                
                else:
                    wfp1.add_row(wfp2)
                    # print("ERROR", wfp1.crawl_dist, wfp1.i, wfp1.word(), wfp2.i, wfp2.word())
                    # return table

                wfp1.reset_crawl_depth()
                wfp2.reset_crawl_depth()

            if wfp1.i % 50000 < 1:
                print(wfp1.i, " complete.")

        table = {
            f"{wfp1.name}Id": wfp1.ids_output,
            f"{wfp1.name}Text": wfp1.words_output,
            f"{wfp2.name}Text": wfp2.words_output,
            f"{wfp2.name}Id": wfp2.ids_output,
            "code": wfp2.cases_output,
        }

        write_file = f"{wfp1.name}-to-{wfp2.name}-comparison.csv"
        save_path = os.path.join(self.dest_path, write_file)
        df = pd.DataFrame(table, dtype=str)
        df.to_csv(save_path, encoding='utf-8', index=False)

        return save_path

# from constants.data import STEP_CORPUS
# step_wfp = WordFileParser(
#     file=os.path.join(PATHS.STEP_DATA_DEST_FULL_PATH, STEP_CORPUS.WRITE_FILE_FORMATTED), 
#     word_col=STEP_CORPUS.TEXT_ATTR, 
#     id_col=STEP_CORPUS.ID_ATTR, 
#     name='step')

# print(step_wfp.ids[0:3])