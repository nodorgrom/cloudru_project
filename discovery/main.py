from discovery.base import CloudEvoClient
from discovery.collectors.vpcs import VPCCollector
from discovery.collectors.subnets import SubnetCollector
from discovery.collectors.security_groups import SecurityGroupsCollector
from discovery.collectors.flavors import FlavorsCollector
from discovery.config import Config
import json
import asyncio
import httpx


def run_discovery():
    client = CloudEvoClient()


    ### SECURITY GROUPS DATA
    # security_groups = SecurityGroupsCollector(client).get()
    sg_collector = SecurityGroupsCollector(client)
    security_groups = sg_collector.get()
    rules_map = asyncio.run(sg_collector.get_sg_rules(security_groups))

    for sg in security_groups:
        sg['rules'] = rules_map.get(sg['id'], [])


    ### VPCs DATA
    vpcs = VPCCollector(client).get()


    ### SUBNETS DATA
    subnets = SubnetCollector(client).get()


    ### FLAVORS DATA
    flavors = FlavorsCollector(client).get()


    ### FULL DATA
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
