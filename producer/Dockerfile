FROM python:3.11-bookworm AS compile-image


WORKDIR /dist


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


COPY ./requirements.txt /dist
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /dist/


ENTRYPOINT ["python3", "producer_main.py"]



