FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --index-url https://pypi.anaconda.org/intel/simple --extra-index-url https://pypi.org/simple mkl_fft

EXPOSE 7864

CMD ["python", "app.py"]