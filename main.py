import os
from topic_modeling.preprocessor import Preprocessor
from topic_modeling.modeling import Modeler

if __name__ == "__main__":
    tmp_path = os.path.join(os.getcwd(), "model/")
    if len(os.listdir(tmp_path)) > 0:
        print(1)
        exit(1)
        model = Modeler(tmp_path)
    else:
        preprocessor = Preprocessor()
        model = Modeler(tmp_path, preprocessor.paras_tokenized, False)
    
    print("Ukończone!")
    exit(12)
