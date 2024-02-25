from locust import HttpUser, task, between


class SportApp(HttpUser):
    host = "http://localhost:8081"
    wait_time = between(5, 15)  # Tiempo de espera entre las solicitudes, en segundos

    @task
    def micro_seguridad_health_check(self):
        self.client.get("/ping")
