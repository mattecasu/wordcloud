import spacy, csv, re, sys, textacy
from wordcloud import WordCloud
import multidict as multidict
import matplotlib.pyplot as plt
from itertools import groupby
from enum import Enum

nlp_en = spacy.load("it_core_news_sm")
nlp_it = spacy.load("en_core_web_sm")

stopwords_en = spacy.lang.en.stop_words.STOP_WORDS.union({"book", "author", "novel", "introduction", "chapter"})
stopwords_it = spacy.lang.it.stop_words.STOP_WORDS.union({"libro", "autore", "volume", "romanzo", "introduzione"})
stopwords = stopwords_en.union(stopwords_it)

def to_multidict(d: dict):
    multi = multidict.MultiDict()
    for key in d:
        multi.add(key, d[key])
    return multi

def to_normal_dict(multi):
    return {k: v for k, v in multi.items()}


CLEANER = " ,‟”;-\".()?!"

class Mode(Enum):
    NOUN_CHUNKS = 1
    NGRAMS = 2

def flatten(nested):
    return [item for l in nested for item in l]

def splitBy(chunk, connectives):
    l = chunk.split()
    if any([x in connectives for x in l]):
        groupby(l, lambda x: x == "")
        lists = [list(group) for k, group in groupby(l, lambda x: x in connectives) if not k]
        return flatten(lists)
    else:
        return [chunk]

def strip_list(l):
    while l and (l[-1] in stopwords or l[-1].isnumeric()):
        l.pop()
    l.reverse()
    while l and (l[-1] in stopwords or l[-1].isnumeric()):
        l.pop()
    l.reverse()
    return l

def clean_chunk(chunk):
    clean_chunk = chunk.lower().strip(CLEANER)
    split_chunk = clean_chunk.split()
    chunk = ' '.join(strip_list([t for t in split_chunk]))
    return chunk

def getNounChunks(doc, connectives):
        chunks = [chunk.text for chunk in doc.noun_chunks]
        chunks_expanded = [splitBy(chunk, connectives) for chunk in chunks]
        return flatten(chunks_expanded)

def getNGrams(doc, n: int):
    return [ngram.text for ngram in list(textacy.extract.basics.ngrams(doc, n))]

def getFrequencyDictForText(chunks):
    tmpDict = {}

    for chunk in chunks:
        cleaned = clean_chunk(chunk)
        if (cleaned == "") or (cleaned in stopwords):
            continue
        val = tmpDict.get(cleaned, 0)
        tmpDict[cleaned] = val + 1
    
    return to_multidict(tmpDict)

def makeImage(freqs):

    wc = WordCloud(background_color="white", max_words=500, relative_scaling='auto')
    wc.generate_from_frequencies(freqs)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


chunks = []
MODE = Mode.NGRAMS
filePath = '<myFilePath>'

with open(filePath) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = (
            row['Title'].strip(),
            # row['Author'].strip(),
            row['Summary'].strip()
            ,)
        text = " . " + ' . '.join(values)
        doc_it = nlp_it(text)
        doc_en = nlp_en(text)

        if MODE == Mode.NOUN_CHUNKS:
            chunks += getNounChunks(doc_en, ["and", "or"]) + getNounChunks(doc_it, ["e", "o"])
        elif MODE == Mode.NGRAMS:
            chunks += getNGrams(doc_en, 3) + getNGrams(doc_it, 3)
        else: continue

print(chunks)

freqs = getFrequencyDictForText(chunks)

# freqs_normal_dict = to_normal_dict(freqs)
# factor = 1.0 / sum(freqs_normal_dict.values())
# freqs = to_multidict({k: v * factor for k, v in freqs_normal_dict.items()})

#print(sorted({item for item in freqs.items()}, key=lambda item: item[1], reverse=True))

makeImage(freqs)


