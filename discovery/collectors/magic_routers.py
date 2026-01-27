from discovery.config import Config
import logging

RESOURCE = "Magic Routers"

class MagicRouterCollector:
    def __init__(self, client):
        self.client = client

    def get(self, vpc_map):
        logging.info(f"Begin discovery {RESOURCE} for project: {self.client.project_id}")
        endpoint = Config.API_MAGIC_ROUTER + Config.ENDPOINTS["magic_routers"]
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)

        # Используем словарь для группировки вместо списка table_rows
        grouped_routes = {} 

        if data and 'magicRouters' in data:
            for mr_item in data['magicRouters']:
                mr_id = mr_item['id']
                mr_name = mr_item.get('name', 'N/A')

                connections = self.get_vpc_connections(mr_id)
                routes = self.get_by_id(mr_id)

                for conn in connections:
                    vpc_id = conn.get('vpcId') or conn.get('vpc_id')
                    src_info = vpc_map.get(vpc_id, f"ID: {vpc_id}")

                    # Если ключа (VPC Name) еще нет в словаре, создаем пустой список
                    if src_info not in grouped_routes:
                        grouped_routes[src_info] = []

                    for route in routes:
                      dst = route.get('subnet') or "0.0.0.0/0"
                      n_hop = route.get('nextHopVpcId') or route.get('nextHopType')
                      descr = route.get('description', '')

                      # Добавляем маршрут к соответствующему SRC в словаре
                      grouped_routes[src_info].append({
                          "src": src_info,
                          "mr": mr_name,
                          "dst": dst,
                          "next_hop": n_hop, 
                          "description": descr
                      })
        return grouped_routes # Возвращаем сгруппированный словарь

    def get_by_id(self, magic_router_id):
        # ... (методы get_by_id и get_vpc_connections остаются без изменений)
        logging.info(f"Begin discovery {RESOURCE} [id] for project: {self.client.project_id}")
        endpoint = Config.API_MAGIC_ROUTER + Config.ENDPOINTS["magic_routers"] + "/" + magic_router_id + "/routes/static"
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)
        if data and 'routes' in data:
            resources = data['routes']
            logging.info(f"Success {RESOURCE} discovered: {len(resources)}")
            return resources
        logging.warning(f"{RESOURCE} discovery list is empty or error occured")
        return []

    def get_vpc_connections(self, magic_router_id):
        logging.info(f"Begin discovery {RESOURCE} [vpc connections] for project: {self.client.project_id}")
        endpoint = Config.API_MAGIC_ROUTER + Config.ENDPOINTS["magic_routers"] + "/" + magic_router_id + "/connections/vpc"
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)
        if data and 'vpcConnections' in data:
            resources = data['vpcConnections']
            logging.info(f"Success {RESOURCE} discovered: {len(resources)}")
            return resources
        logging.warning(f"{RESOURCE} discovery list is empty or error occured")
        return []
