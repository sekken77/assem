FROM python:3.10

WORKDIR /src

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY . /src
