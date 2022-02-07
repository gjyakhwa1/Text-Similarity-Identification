import re
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import time

model = None
count = 0
index = None
sentence_embeddings = None


def cleanText(text):
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def storeModel():
    modelFile = open("./pickle_files/modelFile", "wb")
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    pickle.dump(model, modelFile)
    modelFile.close()


def loadModel():
    filepath = "./pickle_files/modelFile"
    modelFile = open(filepath, "rb")
    ourModel = pickle.load(modelFile)
    modelFile.close()
    return ourModel


def indexing():  # function to serialize index done in colab
    filepath = './csv_files/sentence_embedding.csv'
    df = pd.read_csv(filepath)
    sentence_embeddings = np.array(np.array(df.iloc[:, 1:]), dtype='float32')
    # must set to float32
    sentence_embeddings = np.ascontiguousarray(sentence_embeddings)
    # IndexFlatL2-flatten index and euclidean distance
    index = faiss.IndexFlatL2(sentence_embeddings.shape[1])  # 768
    index.add(sentence_embeddings)
    buf = faiss.serialize_index(index)
    indexFile = open("./pickle_files/serializedIndex", "wb")
    pickle.dump(buf, indexFile)
    indexFile.close()


def loadIndex():
    filepath = './pickle_files/serializedIndex'
    indexFile = open(filepath, 'rb')
    serializedIndex = pickle.load(indexFile)
    indexFile.close()
    return faiss.deserialize_index(serializedIndex)


def initializeModel():
    print("Model Loading started")
    global model, index, count
    time.sleep(20)
    model = loadModel()
    index = loadIndex()
    count = 1
    print("Model loading ended")


def getCount():
    global count
    return count


def similaritySearch(text):
    # storeModel() #-run only oncel to pickling the model
    k = 4  # number of similar vector
    xq = model.encode([text])  # query text
    D, I = index.search(xq, k)
    #lst = [I[0][idx] for idx, i in enumerate(D[0]) if i < 100]
    # return np.array(lst)
    return I[0]
