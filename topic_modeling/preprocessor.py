import os
import PyPDF2
import re
from collections import Counter


class Preprocessor:
    def __init__(self):
        stop_words = [x.replace("\n", "").lower() for x in open(os.path.join(os.getcwd(), "stop_words.txt")).readlines()]
        pdfs = [PyPDF2.PdfFileReader(open(os.path.join(os.getcwd(), f"data/{filename}"), "rb")) for filename in os.listdir(os.path.join(os.getcwd(), "data"))]

        punctuation = [x for x in ",/<>:;\'\"[]{}-_+=@#$%^&*()/"]
        PAGESPLITTER = "``"
        PARASPLITTER = "~~"
        PARA_REGEX = "(\\n.){2}(\\n)"

        pages = PAGESPLITTER.join([pdf.getPage(pdfsPage).extractText() for pdf in pdfs for pdfsPage in range(0, pdf.numPages)])

        for pun in punctuation:
            pages = pages.replace(pun, "")

        pages = ''.join(pages.split(PAGESPLITTER))
        pages = re.sub(PARA_REGEX, PARASPLITTER, pages)

        paras = pages.split(PARASPLITTER)
        paras = [''.join(para.split("\n")).split() for para in paras]
        self.paras_tokenized = [[word.lower() for word in para if word.lower() not in stop_words] for para in paras]

        #tokens = [word for sent in sents for word in sent if word not in stop_words]
        #vocab = sorted(list(set(list(tokens))))
        #tokens_cnt = Counter(tokens)
        #word_freqs = {word: tokens_cnt[word] / len(tokens) for word in vocab}
        #print(sorted(word_freqs.items(), key=lambda l: -l[1])[:10])

