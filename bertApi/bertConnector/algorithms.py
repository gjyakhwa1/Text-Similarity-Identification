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
        global count
        serverStatus = ServerStatus.objects.all().first()
        self.currentAlgo = Algorithm.BERT
        self.encoder = BERT()
        serverStatus.modelLoadingStatus = 1
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.save()
        vectorIndex = VectorIndex()
        vectorIndex.load("./pickle_files/serializedIndex02")
        self.index = vectorIndex
        serverStatus.modelLoadingStatus = 2
        serverStatus.currentTimeStampModel = timezone.now()
        serverStatus.isModelLoading=False
        serverStatus.save()
        self.encoderType = Algorithm.BERT

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
    def similaritySearch(self,text):
        encodedQuery = self.encoder.encode(text)
        return self.index.query(encodedQuery)

    def switch_algo(self, algo: Algorithm):
        algo =Algorithm[algo]
        self.currentAlgo = algo
        if self.encoderType == algo:
            return
        elif algo == Algorithm.USE:
            # self.encoder = UniversalEncoder()
            self.encoder =UniversalEncoder()
            vectorIndex = VectorIndex()
            vectorIndex.load("./pickle_files/serializedIndex02")
            self.index = vectorIndex
            self.encoderType = Algorithm.USE
        elif algo == Algorithm.BERT:
            self.encoder = BERT()
            vectorIndex = VectorIndex()
            vectorIndex.load("./pickle_files/serializedIndex02")
            self.index = vectorIndex
            self.encoderType = Algorithm.BERT
