import pandas as pd
import unicodedata
import os
import json
from constants.paths import PATHS
from enum import Enum

# Normalizes text input into its consonantal form.
# E.g., ἡμῖν becomes ημιν.
def text_normalized(word) -> str:

    normalized: str = unicodedata.normalize("NFKD", word)
    # E.g., oo010040220061,תּ֣וּבַל,תּ֣וּבַל קַ֔יִן,o2033
    normalized = normalized.replace(" ", "")
    # E.g., כְּדָר־
    normalized = normalized.replace("־","")

    return "".join([c for c in normalized if not unicodedata.combining(c)])

class Case(Enum):
    SAME_TEXT = 0
    SAME_CONS = 1
    SAME_ROOT = 2
    IMPLIED_HE = 3
    DIF_AFFIX = 4
    NEXT_MATCH = 5
    DIF_WORD = 6
    MISC = 7

CASE_VALUES = set(item.value for item in Case)

CASES_EVAL_ORDER = [
        Case.IMPLIED_HE, 
        Case.DIF_AFFIX,
        Case.NEXT_MATCH,
        Case.SAME_TEXT,
        Case.SAME_CONS,
        Case.SAME_ROOT,
        Case.DIF_WORD,
    ]

# Note that some of cases 2-4 are Qere vs Ketiv related.
# Note, cases like (2) "אֲ֝דֹנָ֗" vs "אֲ֝דֹנָ֗י" are often followed by (4) "י" vs "NA"
CASES_DEFINITIONS = {
    0: "Identical pointed text",
    1: "Identical consonantal text, different markings",
    2: 'Likely the same base word, different affix parsing, aligned (e.g., "עַמּוּדָ֣י" + "ו" vs "עַמְדּ" + "וּ") or misaligned (e.g., "אֲ֝דֹנָ֗" + "י" vs "אֲ֝דֹנָ֗י")',
    3: 'Likely a missing affix node (e.g., "הָ" + "עֲבָרִ֖ים" vs "הָעֲבָרִ֖ים"), or different word (e.g., "בַּ" vs "כַּ"',
    4: 'Likely missing node for implied article (e.g., "NA" vs "" for implied "ה" in "בַּֽ") or for suffix (e.g., "NA" vs "י" for "אֲ֝דֹנָ֗י")',
}

CRAWL_DEPTH = 1
CRAWL_ITERATIONS = 1


# ************************************************************************************************


class WordFileParser:

    og_crawl_depth: int = CRAWL_DEPTH
    case: int = 0
    crawled_index = 0

    def __init__(self, file: str, name: str, word_col: str, id_col: str):

        self.name: str = name

        self.df = pd.read_csv(
            file,
            sep=self.get_sep(file),
            na_filter=False,
            encoding="utf-8",
            usecols=[word_col, id_col],
            dtype=str,
        )

        self.words: list = self.df[word_col].to_list()
        self.ids: list = self.df[id_col].to_list()

        self.init_values()

    # Initialize the instance values.
    def init_values(self):

        self.words_output: list = []
        self.ids_output: list = []
        self.cases_output: list = []

        self.i: int = 0
        self.crawl_depth: int = self.og_crawl_depth
        self.length: int = len(self.words)

        self.crawled_index = 0
        self.case = 0

    # Get the separator used for the file.
    def get_sep(self, file: str) -> str:

        if file.endswith(".csv"):
            return ","
        elif file.endswith(".tsv"):
            return "\t"
        else:
            raise Exception("Unknown file format. Accepts: .csv, .tsv")

    # Get the word text for a given index.
    # Returns the word at the current instance index if none provided.
    def word(self, i: int = None) -> str:

        if i:
            return self.words[i]

        return self.words[self.i]

    # Get the word id for a given index.
    # Returns the id at the current instance index if none provided.
    def id(self, i: int = None) -> str:

        if i:
            return self.ids[i]

        return self.ids[self.i]

    # Reset the crawl depth to its original value.
    def reset_crawl_depth(self) -> None:

        self.crawl_depth = self.og_crawl_depth

    # Update the output lists given a list with [word, id, case].
    def update_output_lists(self, values: list) -> None:

        self.words_output.append(values[0])
        self.ids_output.append(values[1])
        self.cases_output.append(values[2])

    # Check if we are at the end of the current words lists.
    def at_end_of_words(self, other_wfp: "WordFileParser") -> bool:

        try:
            self.word(self.i + 1)
            other_wfp.word(other_wfp.i + 1)
            return False 

        except IndexError:
            return True
        
    # Check if two words are the same.
    # For use in the comparison method. 
    def same_word_dif_markings(self, word_a: str, word_b: str) -> int:

        word_a_cons = text_normalized(word_a)
        word_b_cons = text_normalized(word_b)
        
        # Consonantal match, e.g., 'עַסּוֹתֶ֣ם' vs 'עַסֹּותֶ֣ם'.
        if word_a_cons == word_b_cons:
            return Case.SAME_CONS.value

        # E.g., the same word with a different consonant @010140080091 'צביים' vs. 'צבוים'.
        elif (
            len(word_a_cons) > 1
            and len(word_b_cons) > 1
            and word_a_cons[0] == word_b_cons[0]
        ):
            if (
                word_a_cons[-1] == word_b_cons[-1] 
                # No more than 1 character diffirence in length.
                and abs( len(word_a_cons) - len(word_b_cons) ) < 2
                # or len(word_a_cons) == len(word_b_cons)
            ):
                # TODO change this value. 
                return Case.SAME_ROOT.value

            else:
                return False

        else:
            return False

    # Check if the next two words are the same.
    def next_words_match(self, other_wfp: "WordFileParser", other_index: int) -> bool:

        if (not self.at_end_of_words(other_wfp)

            and self.same_word_dif_markings(
                self.word(self.i + 1),
                other_wfp.word(other_index + 1)
            ) != False
        ):
            return Case.NEXT_MATCH.value

        else:
            return False

    # An instance where one dataset includes the implied article, but the other doesn't. 
    def implied_article_instance(self, 
        other_wfp: "WordFileParser", 
        other_index: int
    ) -> bool:

        try:
            word_a_cons: str = text_normalized(self.word())
            word_b_cons: str = text_normalized(other_wfp.word(other_index))

            if (
                len(word_a_cons) == 1 # signifies a preposition.
                and word_a_cons == word_b_cons
                and other_wfp.word(other_index + 1) == ''
                # TODO hmmm
                and self.word(self.i + 1) != ''
            ):
                return Case.IMPLIED_HE.value

            else:
                return False

        except IndexError:
            return False

    # Tries to locate and instance where a word is split because of an affix.
    # Or an implied article. 
    def dif_word_split_instance(self, other_wfp: "WordFileParser", other_index: int):

        # https://www.wikiwand.com/en/Suffixes_in_Hebrew
        affix_options = ['א', 'י', 'ו', 'ה', 'ך',]

        try:
            word_a_cons: str = text_normalized( self.word() )
            word_b_cons: str = text_normalized( other_wfp.word(other_index) )
            next_word_b: str = text_normalized( other_wfp.word(other_index + 1) )
            
            if ( word_b_cons != ''
            and word_a_cons != word_b_cons
            and word_b_cons in word_a_cons):

                if next_word_b in word_a_cons:
                    return Case.DIF_AFFIX.value
                # 'תצאתו' vs 'תֹצְאֹתָ֖י' + 'ו' 
                elif (word_a_cons[-1] in affix_options
                and next_word_b in affix_options
                # and not self.next_words_match(other_wfp, other_index)
                ):
                    return Case.DIF_AFFIX.value

                else: 
                    return False
                
            else: 
                return False

        except IndexError:
            return False
            

    # Compare the word text in the current WFP instance to that of another.
    def word_comparison(self, other_wfp: "WordFileParser", new_index: int = 0) -> int:

        other_index: int = max(other_wfp.i, new_index)
        word_a: str = self.word()
        word_b: str = other_wfp.word(other_index)

        if self.implied_article_instance(other_wfp, other_index):
            return Case.IMPLIED_HE.value

        # Case 0 -- exact match, e.g., 'רְשָׁעִ֔ים' vs 'רְשָׁעִ֔ים'.
        elif word_a == word_b:
            return Case.SAME_TEXT.value

        # Check if the next words match. 
        elif self.dif_word_split_instance(other_wfp, other_index):
            return Case.DIF_AFFIX.value

        elif self.same_word_dif_markings(self.word(), other_wfp.word()):
            return self.same_word_dif_markings(self.word(), other_wfp.word())

        # TODO WTF is this?
        elif self.next_words_match(other_wfp, other_wfp.i):
            return Case.NEXT_MATCH.value

        else:
            return Case.DIF_WORD.value

    # THIS COULD BE REWORKED TO REMOVE CASE FROM CLASS INSTANCES: cases=[a,b] in input.
    def evaluate_comparison(self, other_wfp: "WordFileParser", do_comparisons: bool=False) -> tuple["WordFileParser", "WordFileParser", int]:

        comparison_a: int = self.case
        comparison_b: int = other_wfp.case

        if do_comparisons:

            comparison_a = self.word_comparison(other_wfp)
            comparison_b = other_wfp.word_comparison(self)

        # Prioritize comparisons the suggest difference rather than a match.

        for case in CASES_EVAL_ORDER:

            if comparison_a == case.value:
                return self, other_wfp, comparison_a

            elif comparison_b == case.value:
                return other_wfp, self, comparison_b

        return self, other_wfp, comparison_a

    # Traverse the index of the current WFP and another until a matching word is found.
    # Returns False if the depth is exceeded without finding a matching word.
    def crawl(self, other_wfp: "WordFileParser", try_again: bool = False) -> bool:

        depth: int = 0
        runner_index: int = other_wfp.i + 1

        while depth < self.crawl_depth and runner_index < other_wfp.length:

            self.case = self.word_comparison(other_wfp, new_index=runner_index)
            # TODO explain try_again.
            # if comparison < 3 or (try_again and comparison > 2): #was range(2,5)
            # if self.update_comparisons(other_wfp, comparison, runner_index):
            if self.case != Case.DIF_WORD.value:
                other_wfp.crawled_index = runner_index
                return True

            runner_index += 1
            depth += 1
        # self.case = Case.DIF_WORD.value
        other_wfp.crawled_index = other_wfp.i
        return False

    # First, realign the two WFPs to the new_index if one has gone ahead. Then,
    # update the output lists with the comparison value and increment the indices.
    # If there's not a meaningul comparison, return False.
    def update_comparisons(
        self, other_wfp: "WordFileParser", comparison: int, new_index: int = 0
    ) -> bool:

        try:

        # While the current WFP index is less than the other WFP index, add rows to the output.
            if comparison not in {Case.DIF_WORD.value}:
                while other_wfp.i < new_index:
                    other_wfp.update_output_lists([other_wfp.word(), other_wfp.id(), Case.DIF_WORD.value])
                    self.update_output_lists(["NA", '', Case.DIF_WORD.value])
                    other_wfp.i += 1
                
            if comparison in (Case.IMPLIED_HE.value, Case.DIF_AFFIX.value):
                other_wfp.update_output_lists([other_wfp.word(), other_wfp.id(), comparison])
                self.update_output_lists([self.word(), self.id(), comparison])
                # self.i += 1
                other_wfp.i += 1
                other_wfp.update_output_lists([other_wfp.word(), other_wfp.id(), comparison])
                self.update_output_lists(['', self.id() + 'a', comparison])
                other_wfp.i += 1
                self.i += 1
            
                return True

            elif comparison not in {Case.DIF_WORD.value}:
                other_wfp.update_output_lists([other_wfp.word(), other_wfp.id(), comparison])
                self.update_output_lists([self.word(), self.id(), comparison])
                self.i += 1
                other_wfp.i += 1

                return True

                # If the comparison difference is significant, return False.
            else:
                return False
            
        except Exception as e:
            print('GOT IT?', self.id())
            # raise Exception(e, self.name, self.id(), other_wfp.id(), len(self.words), self.i, len(other_wfp.words), other_wfp.i)

        

    def add_row(self, other_wfp: "WordFileParser") -> None:

        other_wfp.update_output_lists([other_wfp.word(), other_wfp.id(), Case.MISC.value])
        self.update_output_lists([self.word(), self.id(), Case.MISC.value])
        self.i += 1
        other_wfp.i += 1


# ************************************************************************************************

# Uses sections like book, chapter, and verse.
class WordFileSectionalParser(WordFileParser):

    og_crawl_depth: int = CRAWL_DEPTH
    case: int = 0
    crawled_index = 0

    def __init__(
        self,
        file: str,
        name: str,
        word_col: str,
        id_col: str,
        book_col: str = None,
        chapter_col: str = None,
        verse_col: str = None,
    ):

        self.name: str = name

        usecols = [
            col for col in [word_col, id_col, book_col, chapter_col, verse_col] if col
        ]
        self.df = pd.read_csv(
            file,
            sep=self.get_sep(file),
            na_filter=False,
            encoding="utf-8",
            usecols=usecols,
            dtype=str,
        )

        self.words: list = self.df[word_col].to_list()
        self.ids: list = self.df[id_col].to_list()
        self.books: list = self.df[book_col].to_list() if book_col else None
        self.chapters: list = self.df[chapter_col].to_list() if chapter_col else None
        self.verses: list = self.df[verse_col].to_list() if verse_col else None

        self.corpus_dict = {}  # {book} -> {chapter} -> {verse} -> [(id, word)]
        self.__load_corpus_dict()

        self.words_output: list = []
        self.ids_output: list = []
        self.cases_output: list = []

        self.i: int = 0
        self.crawl_depth: int = self.og_crawl_depth
        self.length: int = 0

    # TODO add logic for variability in sections used. B
    def __load_corpus_dict(self):

        self.df = self.df.reset_index()

        for i, word in enumerate(self.words):

            id: str = self.ids[i]
            book: str = self.books[i]
            chapter: str = self.chapters[i]
            verse: str = self.verses[i]

            if book in self.corpus_dict:

                if chapter in self.corpus_dict[book]:

                    if verse in self.corpus_dict[book][chapter]:
                        self.corpus_dict[book][chapter][verse].append((id, word))

                    else:
                        self.corpus_dict[book][chapter][verse] = [(id, word)]

                else:
                    self.corpus_dict[book][chapter] = {verse: [(id, word)]}

            else:
                self.corpus_dict[book] = {chapter: {verse: [(id, word)]}}

        # with open(self.name + '-dict.json', 'w', encoding="utf-8") as jsonfile:
        #     json.dump(self.corpus_dict, jsonfile, ensure_ascii=False, indent=4)

    # Update the index and words to be content of current verse.
    def set_current_verse(self, book: str, ch: str, vs: str):
        self.i = 0
        try:
            self.words = self.corpus_dict[book][ch][vs]
        except Exception as e:
            raise Exception(self.name, book, ch, vs, self.words)
        self.length = len(self.words)

    # Get the word text for a given index.
    # Returns the word at the current instance index if none provided.
    def word(self, i: int = None) -> str:
        
        try:
            if i:
                return self.words[i][1]

            return self.words[self.i][1]
        except Exception as e:
            return "*"

    # Get the ref text for a given index.
    # Returns the reference at the current instance index if none provided.
    def id(self, i: int = None) -> str:
        try:
            if i:
                return 'o' + self.words[i][0]

            return 'o' + self.words[self.i][0]
        except Exception as e:
            return "*"


# ************************************************************************************************


class FileComparisons:

    dest_path: str = PATHS.HEBREW_DATA_COMPARISONS_FULL_PATH    

    def evaluate_comparison(self, wfp1: WordFileParser, wfp2: WordFileParser) -> tuple[WordFileParser, WordFileParser, int]:

        comparison_a: int = wfp1.word_comparison(wfp2)
        comparison_b: int = wfp2.word_comparison(wfp1)

        # Prioritize comparisons the suggest difference rather than a match.

        for case in CASES_EVAL_ORDER:

            if comparison_a == case.value:
                return wfp1, wfp2, comparison_a

            elif comparison_b == case.value:
                return wfp2, wfp1, comparison_b

        return wfp1, wfp2, comparison_a

    def get_comparisons(self, wfp1: WordFileParser, wfp2: WordFileParser) -> None:

        while wfp1.i < wfp1.length and wfp2.i < wfp2.length:

            try:
                # First, get the comparison at the current index of each WFP. 
                _wfp1, _wfp2, comparison = wfp1.evaluate_comparison(wfp2, do_comparisons=True)

                if not _wfp1.update_comparisons(_wfp2, comparison):

                    while wfp1.crawl_depth <= CRAWL_ITERATIONS:
                        wfp1.crawl(wfp2)
                        wfp2.crawl(wfp1)

                        _wfp1, _wfp2, comparison = wfp1.evaluate_comparison(wfp2)
                        if _wfp1.update_comparisons(_wfp2, wfp1.case, wfp2.crawled_index):
                            break
                        # elif wfp2.crawl(wfp1):
                        #     wfp2.update_comparisons(wfp1, wfp2.case, wfp1.crawled_index)
                        #     break
                        # _wfp1, _wfp2, new_index = wfp1.evaluate_comparison(wfp2)
                        #     break
                        # elif wfp1.crawl(wfp2, try_again=True):
                        #     break
                        # elif wfp2.crawl(wfp1, try_again=True):
                        #     break
                        wfp1.crawl_depth += 1
                        wfp2.crawl_depth += 1

                    else:
                        wfp1.add_row(wfp2)
                        # print("ERROR", wfp1.crawl_dist, wfp1.i, wfp1.word(), wfp2.i, wfp2.word())
                        # return table

                    wfp1.reset_crawl_depth()
                    wfp2.reset_crawl_depth()

                if len(wfp1.words_output) % 50000 < 1:
                    print(len(wfp1.words_output), " complete.")

            except Exception as e:
                # print(wfp1.word(), wfp2.word())
                raise Exception("ERROR", wfp1.word(), wfp2.word(), e)

    def get_WFP_comparisons(self, wfp1: WordFileParser, wfp2: WordFileParser) -> tuple:

        try:
            #  TODO: allow for only book, or only chapters, etc.
            for book, chapter_data in wfp1.corpus_dict.items():
                for chapter, verse_data in chapter_data.items():
                    for verse, word_data in verse_data.items():
                        wfp1.set_current_verse(book, chapter, verse)
                        wfp2.set_current_verse(book, chapter, verse)
                        self.get_comparisons(wfp1, wfp2)

        except AttributeError:

            self.get_comparisons(wfp1, wfp2)

        

        table: dict = {
            f"{wfp1.name}Id": wfp1.ids_output,
            f"{wfp1.name}Text": wfp1.words_output,
            f"{wfp2.name}Text": wfp2.words_output,
            f"{wfp2.name}Id": wfp2.ids_output,
            "case": wfp2.cases_output,
        }

        def pad_dict_list(dict_list, padel):
            lmax = 0
            for lname in dict_list.keys():
                lmax = max(lmax, len(dict_list[lname]))
            for lname in dict_list.keys():
                ll = len(dict_list[lname])
                if  ll < lmax:
                    dict_list[lname] += [padel] * (lmax - ll)
            return dict_list

        table = pad_dict_list(table, "_")

        write_file: str = f"{wfp1.name}-to-{wfp2.name}-comparison.csv"
        save_path: str = os.path.join(self.dest_path, write_file)
        df: pd.DataFrame = pd.DataFrame(table, dtype=str)

        return df, save_path

    # compare_both compares wfp1 to wfp2, then compares the result to wfp2 to wfp1.
    def write_WFP_comparisons(
        self, wfp1: WordFileParser, wfp2: WordFileParser, compare_both: bool = False
    ) -> None:

        df, save_path = self.get_WFP_comparisons(wfp1, wfp2)
        print("loading cases dictionary.")
        cases_dict: dict = self.get_cases_dict(df)

        if not compare_both:

            self.write_comparison(df, save_path, cases_dict)

        else:

            print(save_path.split("/")[-1] + " comparison complete.")
            for wfp in [wfp1, wfp2]:
                wfp.init_values()
            df2, save_path2 = self.get_WFP_comparisons(wfp2, wfp1)
            cases_dict2: dict = self.get_cases_dict(df2)
            # Check if the counts differ for any of the cases.
            if [v["count"] for v in cases_dict.values()] != [
                v["count"] for v in cases_dict2.values()
            ]:
                self.write_comparison(df2, save_path2, cases_dict2)

            self.write_comparison(df, save_path, cases_dict)

    # Write the alignment and cases files.
    def write_comparison(self, df: pd.DataFrame, save_path: str, cases_dict: dict=None):

        df.to_csv(save_path, encoding="utf-8", index=False)

        if cases_dict:

            with open(save_path + ".json", "w", encoding="utf-8") as jsonfile:
                json.dump(cases_dict, jsonfile, ensure_ascii=False, indent=4)

    # Get all the mismatch cases as a dictionary.
    def get_cases_dict(self, df: pd.DataFrame) -> dict:

        df: pd.DataFrame = df.astype({"case": "int"})
        cases_dict: dict = {}

        # for definition, case in CASES_DEFINITIONS.items():
        for case in Case:
            definition = case.name
            case = case.value

            # For words that match, only collect the count data.
            if case in (0, 1):
                try:
                    count: int = int(df["case"].value_counts()[case])
                except KeyError:
                    count = 0
                # Add the data for each case into the cases_dict.
                cases_dict[case]: dict = {
                    "definition": definition,
                    "count": count,
                }
                continue
            
            text_comparisons: dict = {}

            case_df: pd.DataFrame = df.loc[df["case"] == case]
            count: int = case_df.shape[0]
            # Update the count for the case.
            cases_dict[case]: dict = {
                "definition": definition,
                "count": count,
            }

            # Compare all the words in the rows containing the current case.
            for word1, word2 in zip(
                case_df[case_df.columns[1]], case_df[case_df.columns[2]]
            ):

                # Take the current two words and store them sorted.
                current_word_pair: list[str] = sorted(
                    [text_normalized(word1), text_normalized(word2)]
                )
                comparison: str = f"({current_word_pair[0]},{current_word_pair[1]})"

                if comparison not in text_comparisons:
                    text_comparisons[comparison]: int = 1

                else:
                    text_comparisons[comparison] += 1

            if len(text_comparisons) > 0: 
                # Sort by frequency of mismatch.
                text_comparisons: dict = sorted(
                    text_comparisons.items(), key=lambda x: x[1], reverse=True
                )
                cases_dict[case]["differences"]: dict = text_comparisons

        return cases_dict


# ************************************************************************************************

from constants.data import STEP_CORPUS, CLEAR_CORPUS, OHB_CORPUS, ETCBC_CORPUS

# step_wfp = WordFileSectionalParser(
#     file=os.path.join(PATHS.STEP_DATA_DEST_FULL_PATH, STEP_CORPUS.WRITE_FILE_ALIGNMENT),
#     name="step",
#     word_col=STEP_CORPUS.TEXT_ATTR,
#     id_col=STEP_CORPUS.ID_ATTR,
#     book_col="book",
#     chapter_col="chapter",
#     verse_col="verse",
# )
# print("1 loaded")

macula_wfp = WordFileSectionalParser(
    file=os.path.join(
        PATHS.CLEAR_MACULA_HEBREW_DEST_FULL_PATH, CLEAR_CORPUS.WRITE_FILE_FORMATTED
    ),
    name="macula",
    word_col=CLEAR_CORPUS.TEXT_ATTR,
    id_col=CLEAR_CORPUS.ID_ATTR,
    book_col="book",
    chapter_col="chapter",
    verse_col="verse",
)

print("1 loaded")

etcbc_wfp = WordFileSectionalParser(
    file=os.path.join(PATHS.ETCBC_DATA_DEST_FULL_PATH, "BHSA-words-2021.tsv"),
    name="etcbc",
    word_col=ETCBC_CORPUS.TEXT_ATTR,
    id_col=ETCBC_CORPUS.ID_ATTR,
    book_col=ETCBC_CORPUS.BOOK_ATTR,
    chapter_col=ETCBC_CORPUS.CHAPTER_ATTR,
    verse_col=ETCBC_CORPUS.VERSE_ATTR,
)

print("2 loaded")


fc = FileComparisons()

for wfps in [(macula_wfp, etcbc_wfp)]:

    wfp1, wfp2 = wfps
    fc.write_WFP_comparisons(wfp1, wfp2, compare_both=False)
# for wfps in [(step_wfp, macula_wfp)]:

#     wfp1, wfp2 = wfps
#     fc.write_WFP_comparisons(wfp1, wfp2, compare_both=False)
