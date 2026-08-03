from __future__ import annotations

import hashlib
import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Protocol

SparseVector = dict[int, float]
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class EncoderInfo:
    name: str
    family: str
    scope: str
    description: str
    model_ref: str | None = None
    license: str | None = None
    model_size_mb: int | None = None


class Vectorizer(Protocol):
    info: EncoderInfo

    @property
    def feature_count(self) -> int: ...

    def fit_transform(self, texts: list[str]) -> list[SparseVector]: ...

    def transform_many(self, texts: list[str]) -> list[SparseVector]: ...


def _word_features(text: str) -> list[str]:
    words = TOKEN_PATTERN.findall(text.lower())
    return words + [f"{left} {right}" for left, right in zip(words, words[1:])]


def _character_features(text: str) -> list[str]:
    normalized = " ".join(TOKEN_PATTERN.findall(text.lower()))
    return [
        normalized[index : index + size]
        for size in range(3, 6)
        for index in range(max(len(normalized) - size + 1, 0))
    ]


def _normalize(values: SparseVector) -> SparseVector:
    norm = math.sqrt(sum(value * value for value in values.values()))
    if norm == 0:
        return {}
    return {index: value / norm for index, value in values.items()}


def cosine_similarity(left: SparseVector, right: SparseVector) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(index, 0.0) for index, value in left.items())


class TfidfVectorizer:
    def __init__(
        self,
        info: EncoderInfo,
        analyzer: Callable[[str], list[str]],
    ) -> None:
        self.info = info
        self._analyzer = analyzer
        self._vocabulary: dict[str, int] = {}
        self._idf: dict[int, float] = {}

    @property
    def feature_count(self) -> int:
        return len(self._vocabulary)

    def fit_transform(self, texts: list[str]) -> list[SparseVector]:
        analyzed = [self._analyzer(text) for text in texts]
        document_frequency: Counter[str] = Counter()
        for features in analyzed:
            document_frequency.update(set(features))

        self._vocabulary = {
            feature: index
            for index, feature in enumerate(sorted(document_frequency))
        }
        document_count = len(texts)
        self._idf = {
            self._vocabulary[feature]: math.log(
                (1 + document_count) / (1 + frequency)
            )
            + 1.0
            for feature, frequency in document_frequency.items()
        }
        return [self._encode(features) for features in analyzed]

    def transform(self, text: str) -> SparseVector:
        if not self._vocabulary:
            raise RuntimeError("vectorizer must be fitted before transform")
        return self._encode(self._analyzer(text))

    def transform_many(self, texts: list[str]) -> list[SparseVector]:
        return [self.transform(text) for text in texts]

    def _encode(self, features: Iterable[str]) -> SparseVector:
        counts = Counter(features)
        weighted = {
            index: count * self._idf[index]
            for feature, count in counts.items()
            if (index := self._vocabulary.get(feature)) is not None
        }
        return _normalize(weighted)


class HashingVectorizer:
    info = EncoderInfo(
        name="feature-hashing",
        family="hashing-vectorizer",
        scope="non-neural",
        description="Signed deterministic word unigram/bigram hashing.",
    )

    def __init__(self, feature_count: int = 512) -> None:
        if feature_count <= 0:
            raise ValueError("feature_count must be positive")
        self._feature_count = feature_count

    @property
    def feature_count(self) -> int:
        return self._feature_count

    def fit_transform(self, texts: list[str]) -> list[SparseVector]:
        return [self.transform(text) for text in texts]

    def transform(self, text: str) -> SparseVector:
        values: SparseVector = {}
        for feature in _word_features(text):
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=9).digest()
            index = int.from_bytes(digest[:8], "big") % self._feature_count
            sign = 1.0 if digest[8] & 1 else -1.0
            values[index] = values.get(index, 0.0) + sign
        return _normalize({index: value for index, value in values.items() if value})

    def transform_many(self, texts: list[str]) -> list[SparseVector]:
        return [self.transform(text) for text in texts]


class FastEmbedVectorizer:
    """Lazy FastEmbed adapter; model loading stays outside benchmark policy."""

    def __init__(
        self,
        model_name: str,
        *,
        license_name: str,
        model_size_mb: int,
        model_factory: Callable[[str], Any] | None = None,
    ) -> None:
        self.info = EncoderInfo(
            name=model_name,
            family="dense-onnx",
            scope="neural-local",
            description="Quantized dense text embeddings executed locally with ONNX Runtime.",
            model_ref=model_name,
            license=license_name,
            model_size_mb=model_size_mb,
        )
        self._model_name = model_name
        self._model_factory = model_factory
        self._model: Any | None = None
        self._feature_count = 0

    @property
    def feature_count(self) -> int:
        return self._feature_count

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        if self._model_factory is not None:
            self._model = self._model_factory(self._model_name)
            return self._model

        from fastembed import TextEmbedding

        cache_dir = os.environ.get("FASTEMBED_CACHE_PATH")
        options: dict[str, Any] = {"model_name": self._model_name}
        if cache_dir:
            options["cache_dir"] = cache_dir
        self._model = TextEmbedding(**options)
        return self._model

    def _convert(self, values: Any) -> SparseVector:
        dense = values.tolist() if hasattr(values, "tolist") else list(values)
        if not dense:
            raise ValueError(f"{self._model_name} returned an empty vector")
        self._feature_count = len(dense)
        return _normalize(
            {index: float(value) for index, value in enumerate(dense) if value}
        )

    def fit_transform(self, texts: list[str]) -> list[SparseVector]:
        model = self._load_model()
        return [self._convert(vector) for vector in model.passage_embed(texts)]

    def transform_many(self, texts: list[str]) -> list[SparseVector]:
        model = self._load_model()
        return [self._convert(vector) for vector in model.query_embed(texts)]


def default_vectorizers() -> list[Vectorizer]:
    return [
        TfidfVectorizer(
            EncoderInfo(
                name="word-tfidf",
                family="tf-idf",
                scope="non-neural",
                description="Word unigram/bigram TF-IDF fitted on the corpus.",
            ),
            _word_features,
        ),
        TfidfVectorizer(
            EncoderInfo(
                name="character-tfidf",
                family="tf-idf",
                scope="non-neural",
                description="Character 3-5 gram TF-IDF fitted on the corpus.",
            ),
            _character_features,
        ),
        HashingVectorizer(),
    ]


def default_dense_vectorizers() -> list[Vectorizer]:
    return [
        FastEmbedVectorizer(
            "BAAI/bge-small-en-v1.5",
            license_name="MIT",
            model_size_mb=67,
        ),
        FastEmbedVectorizer(
            "sentence-transformers/all-MiniLM-L6-v2",
            license_name="Apache-2.0",
            model_size_mb=90,
        ),
    ]
