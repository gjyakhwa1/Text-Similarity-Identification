import faiss
import pickle

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

    def createNewIndex(self,embeddings):
        index = faiss.IndexFlatL2(embeddings.shape[1])  # 768
        index.add(embeddings)
        return index
    
    def dumpSerializeIndex(self,buffer,fileList):
        if fileList=="serializedIndex":
            self._helperDumpSerializeIndex("serializedIndex","serializedIndex01",buffer)
            return "serializedIndex01"
        if fileList == "serializedIndex01":
            self._helperDumpSerializeIndex("serializedIndex01","serializedIndex",buffer)
            return "serializedIndex"
    
    def _helperDumpSerializeIndex(self,currentfilePath,newFilePath,buffer):
        indexFile = open(f"./pickle_files/indexFiles/{currentfilePath}", 'rb')
        serializedIndex = pickle.load(indexFile)
        indexFile.close()
        buf = faiss.deserialize_index(serializedIndex)
        buf.add(buffer)
        index1 = faiss.serialize_index(buf)
        indexFile = open(f"./pickle_files/indexFiles/{newFilePath}", "wb")
        pickle.dump(index1, indexFile)
        indexFile.close()

