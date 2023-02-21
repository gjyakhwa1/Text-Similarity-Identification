from encoders.use import UniversalEncoder
from encoders.bert import BERT
from enum import Enum
from .search_index import VectorIndex


class Algorithm(Enum):
    USE = 1
    BERT = 2


class Runtime:
    def __init__(self):
        self.currentAlgo = Algorithm.BERT
        self.encoder = BERT()
        vectorIndex = VectorIndex()
        vectorIndex.load("./pickle_files/serializedIndex02")
        self.index = vectorIndex
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
