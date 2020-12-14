import os
import sys
import re
from queue import LifoQueue
from urllib.request import urlopen
from urllib.parse import quote

from bs4 import BeautifulSoup
import pandas as pd


class lookup_website:
    def __init__(self):
        pass

    def lookup_word(self, word):
        pass

    def fetch_website_text(self, url):
        url = quote(url, safe="://åäö")
        with urlopen(url) as f:
            text = f.read()
        return text

    def strip_whitespaces(self, string):
        string = re.sub(r"\s", " ", string)
        string = re.sub(r"\ +", " ", string)
        string = re.sub(r",+", ",", string)
        string = re.sub(r";,", ";", string)
        string = re.sub(r"(^(,|\ ))|((,|\ )$)", "", string)
        return string

    # TODO: keep track of last call timestamp to prevent website block
    # - if they suspect a bot is being used they might block it.


class synonymer_dot_se(lookup_website):
    def __init__(self, debug_text=False):
        super(synonymer_dot_se, self).__init__()
        self.print_next_end_tag = False
        debug_attrs_vals = [
            ("too_long_word", "(word too long)"),
            ("no_meaning_found", "(no meaning found)"),
            ("no_synonyms_found", "(no synonyms found)"),
        ]
        if not debug_text:
            debug_attrs_vals = [(attr, "") for attr, _ in debug_attrs_vals]
        for attr, val in debug_attrs_vals:
            setattr(self, attr, val)

    def word_url(self, word):
        # TODO: Take care of special characters
        word = word.replace(" ", "-")
        if len(word) > 30:
            return None  # Synonymer.se only supports 30-length words
        return r"https://www.synonymer.se/sv-syn/" + word

    def lookup_word(self, word):
        url = self.word_url(word)
        if url is None:
            return (self.too_long_word,) * 2
        website_text = self.fetch_website_text(url)
        self.soup = BeautifulSoup(website_text, "html.parser")
        dictResult = self.soup.find("div", class_="DictResult")
        synonyms = self.lookup_synonyms(dictResult)
        meaning = self.lookup_meaning(dictResult)
        return synonyms, meaning

    def lookup_synonyms(self, dictResult):
        dictDefault = dictResult.find("div", id="dict-default")
        if dictDefault:
            dictDefaultBodyText = dictDefault.find("div", class_="body").get_text()
            synonyms = self.strip_whitespaces(dictDefaultBodyText)
        else:
            synonyms = self.no_synonyms_found
        return synonyms

    def lookup_meaning(self, dictResult):
        meaning_div = dictResult.find("div", id="bso")
        if meaning_div:
            meaning_text = meaning_div.find("div", class_="body").get_text()
            meaning = self.strip_whitespaces(meaning_text)
        else:
            meaning = self.no_meaning_found
        return meaning
        # print(website_parsed)


# TODO: class wikipedia (ingress), google (first result)


def pretty_print(word, synonyms, meaning):
    synonym_text, meaning_text, separator = ("", "", "")
    if synonyms:
        synonym_text = "SYNONYMS: " + synonyms

    if meaning:
        meaning_text = "MEANING: " + meaning

    if synonym_text and meaning_text:
        separator = ". "

    if synonym_text or meaning_text:
        word_spacing = " " * max((15 - len(word)), 1)
        return (
            word.upper() + word_spacing + "| " + synonym_text + separator + meaning_text
        )
    else:
        return ""


if __name__ == "__main__":
    print("test")
    input_file = sys.argv[1]  # TODO: replace using click()
    df = pd.read_csv(input_file)  # TODO: csv parser and don't import pandas
    # don't use df.apply since pandas will be removed.
    list_of_dicts = df.to_dict("records")
    synonymer_se = synonymer_dot_se(debug_text=False)
    print(list_of_dicts)
    word_column = "quote"  # TODO: Automatic
    synonym_column = "synonyms"
    meaning_column = "meaning"
    note_column = "note"
    out_data = [{} for _ in list_of_dicts]
    for row_in, row_out in zip(list_of_dicts, out_data):
        word = row_in[word_column]
        print(word)
        row_out[word_column] = word

        try:
            # TODO: Append to row instead if it exists.
            synonyms, meaning = synonymer_se.lookup_word(word)
        except:
            error_text = "failed looking up word"
            synonyms = error_text
            meaning = error_text

        row_out[synonym_column] = synonyms
        row_out[meaning_column] = meaning
        row_out[note_column] = row_in[note_column]

    df_updated = pd.DataFrame(out_data)
    print(df_updated)
    # TODO: csv parser and don't import pandas
    df_updated.to_csv(os.path.splitext(input_file)[0] + "_with_synonyms.csv", sep=";")
    list_of_strings = [
        pretty_print(row[word_column], row[synonym_column], row[meaning_column])
        for row in out_data
    ]
    list_of_strings = [e for e in list_of_strings if e]  # Remove empty lines

    text_file_path = os.path.splitext(input_file)[0] + ".txt"
    with open(text_file_path, "w") as text_file:
        text_file.write("\n".join(list_of_strings))
