FROM python:3.12.13-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

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
RUN python tools/prefetch-models.py

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
