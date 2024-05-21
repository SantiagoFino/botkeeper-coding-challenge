FROM python:3.11.9-bookworm AS compile-image


WORKDIR /src/consumer


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


COPY ./requirements.txt /src/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

    
COPY . /src/


CMD ["python3", "consumer_main.py"]
