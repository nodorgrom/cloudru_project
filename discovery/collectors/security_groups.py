from discovery.config import Config
import logging
import asyncio

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


    async def get_sg_rules(self, security_groups):
        """Асинхронно получает правила для списка SG"""
        tasks = []
        for sg in security_groups:
            sg_id = sg['id']
            # Формируем URL согласно документации
            url = f"{Config.API_COMPUTE}{Config.ENDPOINTS['security_groups']}/{sg_id}/rules"
            tasks.append(self._fetch_rules(sg_id, url))

        # Запускаем все запросы параллельно
        results = await asyncio.gather(*tasks)
        
        # Превращаем в словарь {sg_id: rules}
        return {res['id']: res['rules'] for res in results if res}


    async def _fetch_rules(self, sg_id, url):
        data = await self.client.perform_async_request("GET", url)
        if data and 'items' in data:
            return {'id': sg_id, 'rules': data['items']}
        return {'id': sg_id, 'rules': []}
