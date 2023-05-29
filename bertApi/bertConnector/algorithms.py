from encoders.bert import BERT
from enum import Enum
from .search_index import VectorIndex
from .models import ServerStatus, Question
from django.utils import timezone
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
class Algorithm(Enum):
    BERT = 1

class ModelStatus(Enum):
    MODEL_LOAD = 0
    FAISS_LOAD = 1
    COMPLETE  = 2

class FaissUpdateStatus(Enum):
    DATABASE_UPDATE = 0
    ENCODE = 1
    DUMP = 2
    COMPLETE = 3

class Runtime:
    def __init__(self):
        self.initializer(Algorithm.BERT ,BERT)
    
    def initializer(self,model_name,model):
        serverStatus = ServerStatus.objects.all().first()
        if serverStatus is None:
            serverStatus = ServerStatus.objects.create()
        self.currentAlgo =model_name
        self.encoder = model()
        self.encoderType = model_name
        serverStatus.currentModel = "BERT"
        serverStatus.modelLoadingStatus = ModelStatus.FAISS_LOAD.value
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.save()
        vectorIndex = VectorIndex()
        path = serverStatus.currentQuestionsPath
        vectorIndex.load(path)
        self.index = vectorIndex
        serverStatus.modelLoadingStatus = ModelStatus.COMPLETE.value
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.isModelLoading=False
        serverStatus.save()
    
    def getCosineSimilarity(self,question,results):
        questionEmbedding = self.encoder.encode(question)
        resultsEmbedding = self.encoder.encode_array(results)
        return [cosine_similarity(questionEmbedding, resultEmbedding.reshape(1,-1))[0] for resultEmbedding in resultsEmbedding] 
    
    def similaritySearch(self,text):
        encodedQuery = self.encoder.encode(text)
        return self.index.query(encodedQuery)
    
    def uploadCSV(self, reader,examinationType,examYear,user):
        serverStatus = ServerStatus.objects.all().first()
        if serverStatus is None:
            serverStatus = ServerStatus.objects.create()
        serverStatus.isQuestionsUpdating = True
        #Add data to the database
        serverStatus.questionsUpdatingStatus = FaissUpdateStatus.DATABASE_UPDATE.value
        serverStatus.startTimeStampQuestions = timezone.now()
        serverStatus.currentTimeStampQuestions = timezone.now()
        serverStatus.serverUpTime = timezone.now()
        serverStatus.save()
        csvData =[row[0] for row in reader]
        for question in csvData:
            questionModel = Question()
            questionModel.question = question
            questionModel.examYear = examYear
            questionModel.examinationType= examinationType
            questionModel.user = user
            questionModel.save()
        #Encode the sentences
        serverStatus.questionsUpdatingStatus = FaissUpdateStatus.ENCODE.value
        serverStatus.currentTimeStampQuestions = timezone.now()
        serverStatus.save()
        embeddings = self.encoder.encode_array(csvData)
        embeddings = np.ascontiguousarray(embeddings)

        #Dumping the index
        serverStatus.questionsUpdatingStatus = FaissUpdateStatus.DUMP.value
        serverStatus.currentTimeStampQuestions = timezone.now()
        serverStatus.save()

        fileName = os.path.basename(serverStatus.currentQuestionsPath)
        newPath = VectorIndex().dumpSerializeIndex(embeddings,fileName)
        serverStatus.currentQuestionsPath = f"./pickle_files/indexFiles/{newPath}"
        os.remove(f"./pickle_files/indexFiles/{fileName}")
        self.index.load(serverStatus.currentQuestionsPath)
        serverStatus.save()
        #Complete
        serverStatus.questionsUpdatingStatus =FaissUpdateStatus.COMPLETE.value
        serverStatus.currentTimeStampQuestions = timezone.now()
        serverStatus.isQuestionsUpdating=False
        serverStatus.save()
