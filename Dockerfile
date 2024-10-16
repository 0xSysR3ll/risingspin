FROM python:alpine

COPY . /app

WORKDIR /app

ENV DEBUG_COLORS=True
ENV TERM=xterm-256color
ENV COLORTERM=truecolor

RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]