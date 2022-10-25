import pandas as pd
import unicodedata 
import os
import json
from constants.paths import PATHS


def heb_stripped(word):

    normalized = unicodedata.normalize('NFKD', word)

    return ''.join([c for c in normalized if not unicodedata.combining(c)])

# Note that some of cases 2-4 are Qere vs Ketiv related.
DIFF_CASES_DEF = {
    0: 'Identical pointed text', 
    1: 'Identical consonantal text, different markings',
    2: 'Likely the same base word, different affix parsing, aligned (e.g., "עַמּוּדָ֣י" + "ו" vs "עַמְדּ" + "וּ") or misaligned (e.g., "אֲ֝דֹנָ֗" + "י" vs "אֲ֝דֹנָ֗י")', 
    3: 'Likely a missing affix node (e.g., "הָ" + "עֲבָרִ֖ים" vs "הָעֲבָרִ֖ים"), or different word (e.g., "בַּ" vs "כַּ"', 
    4: 'Likely missing node for implied article (e.g., "NA" vs "" for implied "ה" in "בַּֽ") or for suffix (e.g., "NA" vs "י" for "אֲ֝דֹנָ֗י")'
}
# Note, cases like (2) "אֲ֝דֹנָ֗" vs "אֲ֝דֹנָ֗י" are often followed by (4) "י" vs "NA"

class WordFileParser:

    og_crawl_depth = 1

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

    def get_WFP_comparisons(self, wfp1:WordFileParser, wfp2:WordFileParser):
        
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
            "case": wfp2.cases_output,
        }

        write_file = f"{wfp1.name}-to-{wfp2.name}-comparison.csv"
        save_path = os.path.join(self.dest_path, write_file)
        df = pd.DataFrame(table, dtype=str)

        return df, save_path

    # compare_both compares wfp1 to wfp2, then compares the result to wfp2 to wfp1.
    def write_WFP_comparisons(self, wfp1:WordFileParser, wfp2:WordFileParser, compare_both:bool=False):
        
        df, save_path = self.get_WFP_comparisons(wfp1, wfp2)
        print("loading cases dictionary.")
        cases_dict = self.get_cases_dict(df)

        if not compare_both:

            self.write_comparison(df, save_path, cases_dict)

        else:

            print(save_path.split('/')[-1] + " comparison complete.")

            df2, save_path2 = self.get_WFP_comparisons(wfp2, wfp1)
            cases_dict2 = self.get_cases_dict(df2)

            if cases_dict != cases_dict2:
                self.write_comparison(df, save_path2, cases_dict2)
            
            self.write_comparison(df, save_path, cases_dict)



    def write_comparison(self, df:pd.DataFrame, save_path:str, cases_dict:dict):

        df.to_csv(save_path, encoding='utf-8', index=False)

        with open(save_path + '.json', "w", encoding='utf-8') as jsonfile:
            json.dump(cases_dict, jsonfile, ensure_ascii=False)


    def get_cases_dict(self, df:pd.DataFrame):
        
        df = df.astype({'case':'int'})
        cases_dict = {}

        for case, definition in DIFF_CASES_DEF.items():
            
            if case in (0,1):
                count = int(df['case'].value_counts()[case])
                cases_dict[case] = {
                    'definition': definition,
                    'count': count,
                }
                continue

            diff_text = {}

            case_df = df.loc[df['case'] == case]
            count = case_df.shape[0]
            cases_dict[case] = {
                'definition': definition,
                'count': count,
            }
            
            for word1, word2 in zip(case_df[case_df.columns[1]], case_df[case_df.columns[2]]):
               
                words = sorted( [heb_stripped(word1), heb_stripped(word2)] )
                comp = f"({words[0]},{words[1]})"

                if comp not in diff_text:
                    diff_text[comp] = 1

                else:
                    diff_text[comp] += 1

            if len(diff_text) > 0:
                cases_dict[case]['differences'] = diff_text

        return cases_dict


from constants.data import STEP_CORPUS, CLEAR_CORPUS, OHB_CORPUS
step_wfp = WordFileParser(
    file=os.path.join(PATHS.STEP_DATA_DEST_FULL_PATH, STEP_CORPUS.WRITE_FILE_FORMATTED), 
    word_col=STEP_CORPUS.TEXT_ATTR, 
    id_col=STEP_CORPUS.ID_ATTR, 
    name='step')

macula_wfp = WordFileParser(
    file=os.path.join(PATHS.CLEAR_MACULA_HEBREW_DEST_FULL_PATH, CLEAR_CORPUS.WRITE_FILE_UNFORMATTED), 
    word_col=CLEAR_CORPUS.TEXT_ATTR, 
    id_col=CLEAR_CORPUS.ID_ATTR, 
    name='macula')

w = '/Users/sethhowell/Desktop/Hebrew-Literacy-App/hebrew-data/data-staging/word.csv'
etcbc_wfp = WordFileParser(
    file=w, 
    word_col='text', 
    id_col='wordId', 
    name='etcbc')
fc = FileComparisons()

for wfps in [(etcbc_wfp, macula_wfp)]:
    wfp1, wfp2 = wfps 
    fc.write_WFP_comparisons(wfp1, wfp2, True)







