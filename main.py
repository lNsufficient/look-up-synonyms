from urllib.request import urlopen
from html.parser import HTMLParser

class synonym_website(HTMLParser):
    def __init__(self):
        print("inside super init")
        HTMLParser.__init__(self)

    def lookup_synonym(self, word):
        pass

    def fetch_website_text(self, url):
        with urlopen(url) as f:
            text = f.read()
        return text

    #HTML Parsing related functions, handles:
    def read(self, data):
        print(data)
        print("\n\n")
        print(type(data))
        self.reset()
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        print("Encountered start of tag: ", tag)

    def handle_endtag(self, tag):
        print("Encountered end of tag:", tag)

class synonymer_dot_se(synonym_website):
    def __init__(self):
        super(synonymer_dot_se, self).__init__()

    def synonym_url(self, word):
        return r"https://www.synonymer.se/sv-syn/"+word
    
    def lookup_synonym(self, word):
        url = self.synonym_url(word)
        website_text = self.fetch_website_text(url)
        self.read(str(website_text)) #call for website parsing of text
        return website_text

word = "flor"
synonymer_se = synonymer_dot_se()
synonyms = synonymer_se.lookup_synonym(word)
print(synonyms)

