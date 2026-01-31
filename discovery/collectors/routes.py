from discovery.config import Config
import logging

RESOURCE = "Static Routes"

class RouteCollector:
    def __init__(self, client):
        self.client = client

    def get(self, vpc_map):

        logging.info(f"Begin discovery {RESOURCE} for project: {self.client.project_id}")
        
        # 1. Получаем список всех Magic Routers
        mr_endpoint = Config.API_MAGIC_ROUTER + Config.ENDPOINTS["magic_routers"]
        params = {"project_id": self.client.project_id}
        mr_data = self.client.perform_request("GET", mr_endpoint, params)

        grouped_routes = {}

        logging.info(f">>> {mr_data} <<<")
        return mr_data