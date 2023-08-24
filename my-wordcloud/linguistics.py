from enum import Enum

import textacy

import utils, books_utils

CLEANER = " ,‟”;-\".()?!"


class Mode(Enum):
    NOUN_CHUNKS = 1
    NGRAMS = 2


def clean_chunk(chunk):
    clean_chunk = chunk.lower().strip(CLEANER)
    split_chunk = clean_chunk.split()
    chunk = ' '.join(utils.strip_list([t for t in split_chunk], books_utils.STOPWORDS))
    return chunk


def get_noun_chunks(doc, connectives):
    chunks = [chunk.text for chunk in doc.noun_chunks]
    chunks_expanded = [utils.split_by(chunk, connectives) for chunk in chunks]
    return utils.flatten(chunks_expanded)


def get_n_grams(doc, n: int):
    return [ngram.text for ngram in list(textacy.extract.basics.ngrams(doc, n))]


def get_frequency_dict_for_text(chunks):
    tmpDict = {}

    for chunk in chunks:
        cleaned = clean_chunk(chunk)
        if (cleaned == "") or (cleaned in books_utils.STOPWORDS):
            continue
        val = tmpDict.get(cleaned, 0)
        tmpDict[cleaned] = val + 1

    return utils.to_multidict(tmpDict)
