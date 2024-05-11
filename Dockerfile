FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mkl-fft==1.3.8

EXPOSE 7864

CMD ["python", "app.py"]