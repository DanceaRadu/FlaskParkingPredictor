FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5566

EXPOSE 5566

CMD ["python", "app.py"]