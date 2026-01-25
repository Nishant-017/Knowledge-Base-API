
from fastembed import TextEmbedding


class EmbeddingGenerator:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.dimensions = None
        self._model = None  # lazy loading : that is model only loads for the first time

    def _load_model(self):
        if self._model is None:
            self._model = TextEmbedding(self.model_name)

    def embed_single(self, text: str):
        # validation
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.strip()
        if text == "":
            raise ValueError("text cannot be empty")

        self._load_model()

        vec = list(self._model.embed([text]))[0]

        if self.dimensions is None:
            self.dimensions = len(vec)

        return vec

    def embed_batch(self, texts: list[str]):
        
        if not isinstance(texts, list):
            raise TypeError("texts must be a list of strings")

        if len(texts) == 0:
            raise ValueError("texts list cannot be empty")

        cleaned_texts = []
        for i, t in enumerate(texts):
            if not isinstance(t, str):
                raise TypeError(f"texts[{i}] must be a string")
            t = t.strip()
            if t == "":
                raise ValueError(f"texts[{i}] cannot be empty")
            cleaned_texts.append(t)

        self._load_model()

        vectors = list(self._model.embed(cleaned_texts))

        if self.dimensions is None and len(vectors) > 0:
            self.dimensions = len(vectors[0])

        return vectors


    def get_dimensions(self) -> int:
        if self.dimensions is None:
            _ = self.embed_single("dimension check")
        return self.dimensions

