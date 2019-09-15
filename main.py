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
