from discovery.config import Config
import logging

RESOURCE = "VPC"

class VPCCollector:
    def __init__(self, client):
        self.client = client

    def get(self):
        logging.info(f"Begin discovery {RESOURCE} for project: {self.client.project_id}")

        endpoint = Config.API_VPC + Config.ENDPOINTS["vpcs"]
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)

        if data and 'vpcs' in data:
            resources = data['vpcs']
            logging.info(f"Success {RESOURCE} discovered: {len(resources)}")
            return resources

        logging.warning(f"{RESOURCE} discovery list is empty or error occured")
        return []
