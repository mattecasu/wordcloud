import os

import csv, logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import books_utils
import linguistics

logger = logging.getLogger(__name__)

MODE = linguistics.Mode.NGRAMS
CSV_FIELDS = ['Title', 'Summary']
CSV_PATH = os.path.expanduser('~/Desktop/HandyLib.csv')


def make_image(freqs):
    wc = WordCloud(background_color="white", max_words=500, relative_scaling='auto')
    wc.generate_from_frequencies(freqs)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def get_values(fields):
    return [row[field].strip() for field in fields]


chunks = []
with open(CSV_PATH) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = get_values(CSV_FIELDS)
        text = " . " + ' . '.join(values)
        doc_it = books_utils.nlp_it(text)
        doc_en = books_utils.nlp_en(text)
        if MODE == linguistics.Mode.NOUN_CHUNKS:
            chunks += linguistics.get_noun_chunks(doc_en, ["and", "or"])
            chunks += linguistics.get_noun_chunks(doc_it, ["e", "o"])
        elif MODE == linguistics.Mode.NGRAMS:
            chunks += linguistics.get_n_grams(doc_en, 3) + linguistics.get_n_grams(doc_it, 3)
        else:
            continue

freqs = linguistics.get_frequency_dict_for_text(chunks)

logger.info(
    sorted({(chunk, freq) for (chunk, freq) in freqs.items() if freq > 2}, key=lambda item: item[1], reverse=True))

make_image(freqs)
