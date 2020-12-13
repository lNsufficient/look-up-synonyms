from urllib.request import urlopen
from queue import LifoQueue
from bs4 import BeautifulSoup
import re

class synonym_website():
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
        

class synonymer_dot_se(synonym_website):
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
    
word = "flor"
synonymer_se = synonymer_dot_se()
synonyms = synonymer_se.lookup_word(word)
print(synonyms)
#print(synonyms)

