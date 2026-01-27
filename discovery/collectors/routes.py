from discovery.config import Config
import logging

RESOURCE = "Static Routes"

class RouteCollector:
    def __init__(self, client):
        self.client = client

    def get(self, vpc_map):
        """
        Собирает статические маршруты через Magic Routers и группирует их по имени VPC.
        vpc_map: словарь {vpc_id: vpc_name}
        """
        logging.info(f"Begin discovery {RESOURCE} for project: {self.client.project_id}")
        
        # 1. Получаем список всех Magic Routers
        mr_endpoint = Config.API_MAGIC_ROUTER + Config.ENDPOINTS["magic_routers"]
        params = {"project_id": self.client.project_id}
        mr_data = self.client.perform_request("GET", mr_endpoint, params)

        grouped_routes = {}

        if mr_data and 'magicRouters' in mr_data:
            for mr_item in mr_data['magicRouters']:
                mr_id = mr_item['id']
                mr_name = mr_item.get('name', 'N/A')

                # 2. Получаем связи MR с VPC и сами маршруты
                connections = self._get_vpc_connections(mr_id)
                static_routes = self._get_static_routes(mr_id)

                for conn in connections:
                    vpc_id = conn.get('vpcId') or conn.get('vpc_id')
                    # Определяем имя VPC из мапы или оставляем ID
                    vpc_name = vpc_map.get(vpc_id, f"ID: {vpc_id}")

                    if vpc_name not in grouped_routes:
                        grouped_routes[vpc_name] = []

                    for route in static_routes:
                        dst = route.get('subnet') or "0.0.0.0/0"
                        # Пытаемся определить понятный Next Hop
                        n_hop = route.get('nextHopVpcId') or route.get('nextHopType') or "N/A"
                        descr = route.get('description', '')

                        grouped_routes[vpc_name].append({
                            "vpc_name": vpc_name,
                            "mr_name": mr_name,
                            "dst": dst,
                            "next_hop": n_hop,
                            "description": descr
                        })
        
        logging.info(f"Total VPCs with routes discovered: {len(grouped_routes)}")
        return grouped_routes

    def _get_static_routes(self, magic_router_id):
        endpoint = f"{Config.API_MAGIC_ROUTER}{Config.ENDPOINTS['magic_routers']}/{magic_router_id}/routes/static"
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)
        return data.get('routes', []) if data else []

    def _get_vpc_connections(self, magic_router_id):
        endpoint = f"{Config.API_MAGIC_ROUTER}{Config.ENDPOINTS['magic_routers']}/{magic_router_id}/connections/vpc"
        params = {"project_id": self.client.project_id}
        data = self.client.perform_request("GET", endpoint, params)
        return data.get('vpcConnections', []) if data else []
