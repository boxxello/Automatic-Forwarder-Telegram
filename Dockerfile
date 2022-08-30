FROM python:3.9
ADD . /app
WORKDIR /app
COPY ./requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install --user -r requirements.txt
COPY . .
