import re
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import time

from .algorithms import Runtime, ModelStatus
from .models import ServerStatus
from django.utils import timezone
from datetime import datetime

sentence_embeddings = None

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
    if serverStatus is None:
        serverStatus = ServerStatus.objects.create()
    serverStatus.isModelLoading =True
    serverStatus.modelLoadingStatus = ModelStatus.MODEL_LOAD.value
    serverStatus.startTimeStampModel = timezone.now()
    serverStatus.currentTimeStampModel = timezone.now()
    serverStatus.serverUpTime = timezone.now()
    serverStatus.save()
    print("Model Loading started")
    global runTime 
    runTime =Runtime()

    print("Model loading ended")

def uploadCSVFile(reader,examinationType,examYear,user):
    print("Database is updating")
    global runTime
    runTime.uploadCSV(reader,examinationType,examYear,user)
    print("Database update Complete")

def similaritySearch(text):
    return runTime.similaritySearch(text)

def getCosineSimilarity(ques,results):
    return runTime.getCosineSimilarity(ques,results)

def getTimeStamp(value):
    try:
        currentTimeStampModel = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        currentTimeStampModel = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
    return currentTimeStampModel
  
def similaritySearch(text):
    # storeModel() #-run only oncel to pickling the model
    k = 4  # number of similar vector
    xq = model.encode([text])  # query text
    D, I = index.search(xq, k)
    #lst = [I[0][idx] for idx, i in enumerate(D[0]) if i < 100]
    # return np.array(lst)
    return I[0]

def getCosineSimilarity(question, result):
    questionEmbedding = model.encode([question])
    resultsEmbedding = model.encode([result])
    return(cosine_similarity(questionEmbedding, resultsEmbedding)[0])

