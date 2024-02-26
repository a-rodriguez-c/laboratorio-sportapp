from locust import HttpUser, task

class SportApp(HttpUser):
    @task
    def eventos_naturales(self):
        self.client.get(":8083/notificaciones")
        self.client.get(":8082/eventos-naturales")
        self.client.get(":8081/eventos-seguridad")
        self.client.get(":8082/ping")
        self.client.get(":8081/ping")

