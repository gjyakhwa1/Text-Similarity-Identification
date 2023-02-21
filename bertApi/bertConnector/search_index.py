import faiss
import pickle
from sklearn.metrics.pairwise import cosine_similarity


class VectorIndex:
    def __init__(self,k=4):#k speicifies the number of nearest neighbour
        self.k = k

    def query(self, vector):
        D,I =self.index.search(vector,self.k)
        return I[0]

    def load(self, path):
        indexFile = open(path, 'rb')
        serializedIndex = pickle.load(indexFile)
        indexFile.close()
        self.index = faiss.deserialize_index(serializedIndex)

    # def build(self, vectors, labels, number_of_trees=5):
    #     self.vectors = vectors
    #     self.labels = labels

    #     for i, vec in enumerate(vectors):
    #         if not np.isnan(np.sum(vec)):
    #             self.index.add_item(i, vec)
    #     self.index.build(number_of_trees)

    # def save(self, path):
    #     label_path = path.split(".ann")[0] + ".labels"
    #     print(label_path)
    #     with open(label_path, "wb") as fp:
    #         pickle.dump(self.labels, fp)
    #     self.index.save(path)
