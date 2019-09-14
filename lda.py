import os
import PyPDF2
import re
from collections import Counter
from pprint import pprint #as print
import datefinder

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.test.utils import datapath

#from smart_open import smart_open

import spacy


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

stop_words = [x.replace("\n", "").lower() for x in open(os.path.join(os.getcwd(), "stop_words.txt")).readlines()]
pdfs = [PyPDF2.PdfFileReader(open(os.path.join(os.getcwd(), f"data/{filename}"), "rb")) for filename in os.listdir(os.path.join(os.getcwd(), "data"))]
print(len(pdfs))
# 5
#pdfs = [PyPDF2.PdfFileReader(open(os.path.join(os.getcwd(), f"data/{filename}"), "rb")) for filename in ["02.pdf"]]

separators = [".", "...", "!", "?"]
punctuation = [x for x in ",/<>:;\'\"[]{}-_+=@#$%^&*()/"]
PAGESPLITTER = "``"
PARASPLITTER = "~~"
PARA_REGEX = "(\\n.){2}(\\n)"
 
pages = PAGESPLITTER.join([pdf.getPage(pdfsPage).extractText() for pdf in pdfs for pdfsPage in range(0, pdf.numPages)])

for pun in punctuation:
    pages = pages.replace(pun, "")

pages = ''.join(pages.split(PAGESPLITTER))
pages = re.sub(PARA_REGEX, PARASPLITTER, pages)

# for sep in separators:
#     pages = pages.replace(sep, SENTANCESPLITTER)

paras = pages.split(PARASPLITTER)
print(len(paras))
paras = [''.join(para.split("\n")).split() for para in paras]
paras = [[word.lower() for word in para if word.lower() not in stop_words] for para in paras]
print(len(paras))

#tokens = [word for sent in sents for word in sent if word not in stop_words]
#vocab = sorted(list(set(list(tokens))))
#tokens_cnt = Counter(tokens)
#word_freqs = {word: tokens_cnt[word] / len(tokens) for word in vocab}

#print(len(tokens))
#print(len(vocab))
#print(sorted(word_freqs.items(), key=lambda l: -l[1])[:10])

bigram = gensim.models.Phrases(paras, min_count=3, threshold=65) # higher threshold fewer phrases.
bigram_mod = gensim.models.phrases.Phraser(bigram)
# trigram = gensim.models.Phrases(bigram[sents], threshold=75)
# trigram_mod = gensim.models.phrases.Phraser(trigram)
# print(trigram_mod[bigram_mod[sents[0]]])

# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

bigrams = [bigram_mod[para] for para in paras]
allowed_postags = ["NOUN", "ADJ", "VERB", "ADV", "NUM"]
data_lemmatized = [[token.lemma_ for token in nlp(" ".join(para)) if token.pos_ in allowed_postags] for para in bigrams]
print(len(data_lemmatized))

# print(data_lemmatized[:1])

# word2idx = {word: idx for (idx, word) in enumerate(vocab)}
# idx2word = {idx: word for (word, idx) in word2idx.items()}

id2word = corpora.Dictionary(data_lemmatized)
corpus = [id2word.doc2bow(text) for text in data_lemmatized]
print(len(corpus))
print()
print()
print()
#print(corpus[:1])

#print(id2word.__dict__)
# print(word2idx)
# print([x for x idx2word.items()][:10])
# print([x for x id2word.items()][:10])

mallet_path = "/home/amillert/private/chat-to-eu/mallet-2.0.8/bin/mallet"
lda_model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

# lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                            id2word=id2word,
#                                            num_topics=20, 
#                                            random_state=6,
#                                            update_every=1,
#                                            chunksize=100,
#                                            passes=20,
#                                            alpha='auto',
#                                            per_word_topics=True)

pprint(lda_model.print_topics())
# doc_lda = lda_model[corpus]
#exit(12)
#print('\nPerplexity: ', lda_model.log_perplexity(corpus))

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

limit=211; start=10; step=20;
x = range(start, limit, step)

model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=start, limit=limit, step=step)

for m, cv in zip(x, coherence_values):
    print("Num Topics =", m, " has Coherence Value of", round(cv, 4))


exit(12)


print("STARTED")
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

tmp_file = datapath("/home/amillert/private/chat-to-eu/model/lda")
lda_model.save(tmp_file)

# lda = LdaModel.load(temp_file)
# lda.update(other_corpus)
# vector = lda[unseen_doc]
