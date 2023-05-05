# FROM python:3.8-alpine

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev
# RUN pip install --upgrade cython
# RUN pip install --upgrade pip

FROM python:3

RUN pip install typing fastapi pydantic uvicorn bs4 numpy pandas nltk matplotlib scikit-learn SoMaJo python-multipart lxml redis

RUN python -m nltk.downloader wordnet

WORKDIR /app

COPY main.py model_predict.py utils_functions.py file_parsing.py ./

ENTRYPOINT ["python", "main.py"]