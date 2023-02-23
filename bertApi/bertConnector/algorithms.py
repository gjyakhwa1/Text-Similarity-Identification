from encoders.use import UniversalEncoder
from encoders.bert import BERT
from enum import Enum
from .search_index import VectorIndex
from .models import ServerStatus, Question
from django.utils import timezone
import numpy as np
import os
class Algorithm(Enum):
    USE = 1
    BERT = 2

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
        serverStatus.currentModel = "BERT" if model_name==Algorithm.BERT else "USE"
        serverStatus.modelLoadingStatus = ModelStatus.FAISS_LOAD.value
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.save()
        vectorIndex = VectorIndex()
        path = serverStatus.currentQuestionsPath if model_name==Algorithm.BERT else serverStatus.currentQuestionsPathUSE
        vectorIndex.load(path)
        self.index = vectorIndex
        serverStatus.modelLoadingStatus = ModelStatus.COMPLETE.value
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.isModelLoading=False
        serverStatus.save()
        
    def similaritySearch(self,text):
        encodedQuery = self.encoder.encode(text)
        return self.index.query(encodedQuery)

    def switch_algo(self, algo: Algorithm):
        algo =Algorithm[algo]
        self.currentAlgo = algo
        if self.encoderType == algo:
            return
        elif algo == Algorithm.USE:
            self.initializer(Algorithm.USE ,UniversalEncoder)
        elif algo == Algorithm.BERT:
            self.initializer(Algorithm.BERT ,BERT)
    
    def uploadCSV(self, reader):
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

        if self.currentAlgo == Algorithm.BERT:
            fileName = os.path.basename(serverStatus.currentQuestionsPath)
            newPath = VectorIndex().dumpSerializeIndex(embeddings,fileName)
            serverStatus.currentQuestionsPath = f"./pickle_files/indexFiles/{newPath}"
            os.remove(f"./pickle_files/indexFiles/{fileName}")
            self.index.load(serverStatus.currentQuestionsPath)
        else:
            fileName = os.path.basename(serverStatus.currentQuestionsPathUSE)
            newPath = VectorIndex().dumpSerializeIndex(embeddings,fileName)
            serverStatus.currentQuestionsPathUSE =f"./pickle_files/indexFiles/{newPath}"
            os.remove(f"./pickle_files/indexFiles/{fileName}")
            self.index.load(serverStatus.currentQuestionsPathUSE)
        serverStatus.save()
        #Complete
        serverStatus.questionsUpdatingStatus =FaissUpdateStatus.COMPLETE.value
        serverStatus.currentTimeStampQuestions = timezone.now()
        serverStatus.isQuestionsUpdating=False
        serverStatus.save()
