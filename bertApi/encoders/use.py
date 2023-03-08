import tensorflow_hub as hub
import numpy as np
from encoders.base import Encoder


class UniversalEncoder(Encoder):
    def __init__(
        self, model_path: str = "https://tfhub.dev/google/universal-sentence-encoder/4"
    ):
        self.embedding_size = 512
        self.model = hub.load(model_path)
        # pass

    # @property
    def encode(self, sentence):
        embeddings = self.model([sentence])
        return embeddings[0]

    def encode_array(self, sentences):
        embeddings = self.model(sentences)
        return embeddings
