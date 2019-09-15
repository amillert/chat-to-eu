import os
from topic_modeling.preprocessor import Preprocessor
from topic_modeling.modeling import Modeler

if __name__ == "__main__":
    tmp_path = os.path.join(os.getcwd(), "model/")
    if len(os.listdir(tmp_path)) > 0:
        modeler = Modeler(tmp_path)
    else:
        preprocessor = Preprocessor()
        modeler = Modeler(tmp_path, preprocessor.paras_tokenized, False)
    model = modeler.lda_model
    # print 15 key words for 20 most important topics
    # model.print_topics(20, num_words=15)

    # Part for paraphrasing user query if not found
    # question = "Will brexit happen now?"
    # tokenized = [question.split()]

    # print(tokenized)
    # new_corpus = [model.id2word.doc2bow(text) for text in tokenized]
    # vec = [(model.id2word[x[0]], x[1]) for x in  model[new_corpus[0]][0]]
    # paraphrased_query = ' '.join([x[0] for x in sorted(vec, key = lambda x: -x[1])[:15]])

    # print(paraphrased_query)
