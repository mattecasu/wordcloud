import spacy

nlp_en = spacy.load("it_core_news_sm")
nlp_it = spacy.load("en_core_web_sm")

stopwords_en = spacy.lang.en.stop_words.STOP_WORDS.union({"book", "author", "novel", "introduction", "chapter"})
stopwords_it = spacy.lang.it.stop_words.STOP_WORDS.union({"libro", "autore", "volume", "romanzo", "introduzione"})
STOPWORDS = stopwords_en.union(stopwords_it)
