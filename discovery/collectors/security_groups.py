from discovery.config import Config
import logging

RESOURCE = "SecurityGroups"

class SecurityGroupsCollector:
    def __init__(self, client):
        self.client = client

    def get(self):
        logging.info(f"Begin discovery {RESOURCE} for project: {self.client.project_id}")

        endpoint = Config.API_COMPUTE + Config.ENDPOINTS["security_groups"]
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)

        if data and 'items' in data:
            resources = data['items']
            logging.info(f"Success {RESOURCE} discovered: {len(resources)}")
            return resources

        logging.warning(f"{RESOURCE} discovery list is empty or error occured")
        return []
