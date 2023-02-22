from encoders.use import UniversalEncoder
from encoders.bert import BERT
from enum import Enum
from .search_index import VectorIndex
from .models import ServerStatus
from django.utils import timezone
class Algorithm(Enum):
    USE = 1
    BERT = 2

class ModelStatus(Enum):
    MODEL_LOAD = 0
    FAISS_LOAD = 1
    COMPLETE  = 2

class Runtime:
    def __init__(self):
        self.initializer(Algorithm.BERT ,BERT)
    
    def initializer(self,model_name,model):
        serverStatus = ServerStatus.objects.all().first()
        self.currentAlgo =model_name
        self.encoder = model()
        self.encoderType = model_name
        serverStatus.currentModel = "BERT" if model_name==Algorithm.BERT else "USE"
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

    # generates new index from uploaded data
    # def change_index(self, filename):
    #     questions = []
    #     with open(filename, "r") as fp:
    #         questions = [
    #             x.strip().lower().split("?,") for x in fp.readlines() if x != "\n"
    #         ]
    #     questions_string = [question[0] for question in questions]
    #     embeddings = self.encoder.encode_array(questions_string)
    #     annoy_index = AnnoyIndex(dimension=len(embeddings[0]))
    #     annoy_index.build(embeddings, questions_string)
    #     annoy_index.save("./indices/" + filename + str(self.current_algo) + ".ann")
    #     self.index = annoy_index
