FROM locustio/locust:1.5.3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY locustfile.py .

CMD ["locust", "-f", "locustfile.py"]
