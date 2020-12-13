from urllib.request import urlopen
from queue import LifoQueue
from bs4 import BeautifulSoup
import re
import pandas as pd
import sys
import os

class lookup_website():
    def __init__(self):
        pass

    def lookup_synonym(self, word):
        pass

    
    def fetch_website_text(self, url):
        with urlopen(url) as f:
            text = f.read()
        return text

    def strip_whitespaces(self, string):
        string = re.sub(r"\s", ",", string)
        string = re.sub(r",+", ",", string)
        string = re.sub(r";,", ";", string)
        string = re.sub(r"(^,)|(,$)", "", string)
        return string
    
    #TODO: keep track of last call timestamp to prevent website block
    # - if they suspect a bot is being used they might block it.
        

class synonymer_dot_se(lookup_website):
    def __init__(self):
        super(synonymer_dot_se, self).__init__()
        self.print_next_end_tag = False

    def synonym_url(self, word):
        return r"https://www.synonymer.se/sv-syn/"+word
    
    def lookup_word(self, word):
        url = self.synonym_url(word)
        website_text = self.fetch_website_text(url)
        self.soup = BeautifulSoup(website_text, "html.parser")
        synonyms = self.lookup_synonyms()
        return synonyms
    
    def lookup_synonyms(self):
        dictResult = self.soup.find("div", class_="DictResult")
        dictDefault = dictResult.find("div", id="dict-default")
        dictDefaultBodyText = dictDefault.find("div", class_="body").get_text()
        synonyms = self.strip_whitespaces(dictDefaultBodyText)
        return synonyms
        #print(website_parsed)

#TODO: class wikipedia (ingress), google (first result)


if __name__ == "__main__":
    print("test")
    input_file = sys.argv[1] #TODO: replace using click()
    df = pd.read_csv(input_file) #TODO: csv parser and don't import pandas
    #don't use df.apply since pandas will be removed.
    list_of_dicts = df.to_dict('records')
    synonymer_se = synonymer_dot_se()
    print(list_of_dicts)
    word_column = "quote" #TODO: Automatic
    synonym_column = "synonyms"
    for row in list_of_dicts:
        word = row[word_column] 
        try:
            #TODO: Append to row instead if it exists.
            row[synonym_column] = synonymer_se.lookup_word(word)
        except:
            row[synonym_column] = "failed looking up: " + str(word)
    df_updated = pd.DataFrame(list_of_dicts)
    print(df_updated)
    #TODO: csv parser and don't import pandas
    df_updated.to_csv(os.path.splitext(input_file)[0]+"_with_synonyms.csv")