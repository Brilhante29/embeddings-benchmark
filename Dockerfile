FROM python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FASTEMBED_CACHE_PATH=/opt/fastembed-cache

WORKDIR /app

COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock \
    && python -m pip check

COPY benchmarks/config ./benchmarks/config
COPY tools/prefetch-models.py ./tools/prefetch-models.py
COPY tools/verify-model-cache.py ./tools/verify-model-cache.py
RUN python tools/prefetch-models.py \
    && python tools/verify-model-cache.py

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --no-build-isolation --no-deps .

COPY data ./data
COPY benchmarks ./benchmarks
RUN useradd --create-home --uid 10001 app \
    && chown -R app:app /app /opt/fastembed-cache

USER app

ENTRYPOINT ["python", "-m", "embeddings_benchmark"]
CMD ["benchmark", "--profile", "dense", "--k", "3", "--repeat", "5", "--warmup", "1", "--output", "benchmarks/results/embeddings-baseline.json"]
