from discovery.config import Config
import logging

class SubnetCollector:
    def __init__(self, client):
        self.client = client

    def get(self):
        logging.info(f"Begin discovery Subnets for project: {self.client.project_id}")

        endpoint = Config.API_COMPUTE + Config.ENDPOINTS["subnets"]
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)

        if data and 'items' in data:
            subnets = data['items']
            logging.info(f"Success Subnets discovered: {len(subnets)}")
            return subnets

        logging.warning("Subnets discovery list is empty or error occured")
        return []
