FROM locustio/locust:1.5.3

COPY requirements.txt /mnt/locust/
RUN pip install --no-cache-dir -r /mnt/locust/requirements.txt

COPY app.py /mnt/locust/

CMD ["locust", "-f", "/mnt/locust/app.py"]
