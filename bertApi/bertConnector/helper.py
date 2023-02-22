import re
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

from .algorithms import Runtime
from .models import ServerStatus
from django.utils import timezone

sentence_embeddings = None

count = 0
runTime=None

def cleanText(text):
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def storeModel():
    modelFile = open("./pickle_files/modelFile", "wb")
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    pickle.dump(model, modelFile)
    modelFile.close()


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


def loadModel():
    # filepath = "./pickle_files/fine_tuned_model"
    filepath = "./pickle_files/modelTest"
    modelFile = open(filepath, "rb")
    ourModel = pickle.load(modelFile)
    modelFile.close()
    return ourModel


def loadIndex():
    # filepath = './pickle_files/fineTuned_serializedIndex'
    filepath = './pickle_files/serializedIndex02'
    indexFile = open(filepath, 'rb')
    serializedIndex = pickle.load(indexFile)
    indexFile.close()
    return faiss.deserialize_index(serializedIndex)

def initializeModel():
    serverStatus = ServerStatus.objects.all().first()
    serverStatus.isModelLoading =True
    serverStatus.modelLoadingStatus = 0 
    serverStatus.startTimeStampModel = timezone.now()
    serverStatus.currentTimeStampModel = timezone.now()
    serverStatus.serverUpTime = timezone.now()
    serverStatus.save()
    print("Model Loading started")
    global runTime 
    runTime =Runtime()
    print("Model loading ended")


def getCount():
    global count
    return count

def similaritySearch(text):
    return runTime.similaritySearch(text)

def switchAlgorithm(algo):
    global runTime,count
    print("Algorithm is switching")
    runTime.switch_algo(algo)
    print("Algorithm Switched")

