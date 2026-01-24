from discovery.base import CloudEvoClient
from discovery.collectors.vpcs import VPCCollector
from discovery.collectors.subnets import SubnetCollector
from discovery.collectors.security_groups import SecurityGroupsCollector
from discovery.collectors.flavors import FlavorsCollector
from discovery.collectors.magic_routers import MagicRouterCollector
from discovery.config import Config
import json


def run_discovery():
    client = CloudEvoClient()

    vpcs = VPCCollector(client).get()
    subnets = SubnetCollector(client).get()

    vpc_map = {}

    for v in vpcs:
      v_id = v['id']
      v_name = v['name']
      v_cidrs = [s['subnet_address'] for s in subnets if s.get('vpc_id')]
      cidr_str = ", ".join(v_cidrs) if v_cidrs else "no-cidr"

      vpc_map[v_id] = f"{v_name} [{cidr_str}]"


    topology = MagicRouterCollector(client).get(vpc_map)
    security_groups = SecurityGroupsCollector(client).get()
    flavors = FlavorsCollector(client).get()


    discovered_resources = {
        "vpcs": vpcs,
        "subnets": subnets,
        "security_groups": security_groups,
        "flavors": flavors,
        "topology": topology
    }


    with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(discovered_resources, f, indent=4, ensure_ascii=False)

    print("Discovery complete. Data saved to discovery_output.json")

if __name__ == "__main__":
    run_discovery()
