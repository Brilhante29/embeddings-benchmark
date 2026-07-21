from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

SparseVector = dict[int, float]
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class EncoderInfo:
    name: str
    family: str
    scope: str
    description: str


class Vectorizer(Protocol):
    info: EncoderInfo

    @property
    def feature_count(self) -> int: ...

    def fit_transform(self, texts: list[str]) -> list[SparseVector]: ...

    def transform(self, text: str) -> SparseVector: ...


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
