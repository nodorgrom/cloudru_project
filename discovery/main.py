from discovery.base import CloudEvoClient
from discovery.collectors.vpcs import VPCCollector
from discovery.collectors.subnets import SubnetCollector
from discovery.collectors.security_groups import SecurityGroupsCollector
from discovery.collectors.flavors import FlavorsCollector
from discovery.config import Config
import json


def run_discovery():
    client = CloudEvoClient()

    vpcs = VPCCollector(client).get()
    subnets = SubnetCollector(client).get()
    security_groups = SecurityGroupsCollector(client).get()
    flavors = FlavorsCollector(client).get()

    discovered_resources = {
        "vpcs": vpcs,
        "security_groups": security_groups,
        "flavors": flavors,
        "subnets": subnets
    }


    with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(discovered_resources, f, indent=4, ensure_ascii=False)

    print("Discovery complete. Data saved to discovery_output.json")

if __name__ == "__main__":
    run_discovery()
