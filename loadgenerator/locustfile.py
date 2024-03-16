from locust import HttpUser, task, between
import random


class Deportologo(HttpUser):
    wait_time = between(5, 10)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDYwNzgxMiwianRpIjoiODFjZTExYWYtMTU4ZS00MDgxLWFkMzQtNjQyMTk1OTY0MDdiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzEwNjA3ODEyLCJjc3JmIjoiODczZjRjNTctNGQxZC00MWFlLThmY2ItNGMxMDFmNzhiZTBiIiwiZXhwIjoxNzEwNjA4NzEyLCJyb2xlIjoidXNlciIsIm5hbWUiOiJ1c3VhcmlvMSIsImVtYWlsIjoidXN1YXJpbzFAZ21haWwuY29tIiwidXNlciI6InVzdWFyaW8xIn0.EoNt5NYg6rCVE2P6rOTBmaO5GRe7sTdNKBpDQoE_ncA"

    @task
    def eventos_naturales(self):
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        self.client.get("/naturales", headers=headers)
        self.wait()


class Deportista(HttpUser):
    wait_time = between(1, 5)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDYwNzgxMiwianRpIjoiODFjZTExYWYtMTU4ZS00MDgxLWFkMzQtNjQyMTk1OTY0MDdiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzEwNjA3ODEyLCJjc3JmIjoiODczZjRjNTctNGQxZC00MWFlLThmY2ItNGMxMDFmNzhiZTBiIiwiZXhwIjoxNzEwNjA4NzEyLCJyb2xlIjoidXNlciIsIm5hbWUiOiJ1c3VhcmlvMSIsImVtYWlsIjoidXN1YXJpbzFAZ21haWwuY29tIiwidXNlciI6InVzdWFyaW8xIn0.EoNt5NYg6rCVE2P6rOTBmaO5GRe7sTdNKBpDQoE_ncA"

    @task
    def eventos_naturales(self):
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        self.client.get("/naturales", headers=headers)
        self.wait()
