from encoders.base import Encoder
from sentence_transformers import SentenceTransformer
import pickle


class BERT(Encoder):
    def __init__(self, model_path: str = "./pickle_files/modelFiles/modelTest"):
        if model_path=="bert-base-nli-mean-tokens":
            self.model = SentenceTransformer(model_path)
        else:
            modelFile = open(model_path, "rb")
            self.model = pickle.load(modelFile)
            modelFile.close()

    def encode(self, sentence):
        embeddings = self.model.encode([sentence])
        return embeddings

    def encode_array(self, sentences):
        embeddings = self.model.encode(sentences)
        return embeddings