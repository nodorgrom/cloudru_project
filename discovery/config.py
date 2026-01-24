import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  # auth
  CLIENT_ID = os.getenv("EVO_KEY_ID")
  CLIENT_SECRET = os.getenv("EVO_SECRET_KEY")
  PROJECT_ID = os.getenv("EVO_PROJECT_ID")
  GET_TIMEOUT = 4

  AUTH_URL = "https://iam.api.cloud.ru/api/v1/auth/token"
  API_BASE_URL = "https://api.cloud.ru"

  API_VPC = "https://vpc.api.cloud.ru"
  API_COMPUTE = "https://compute.api.cloud.ru"
  API_MAGIC_ROUTER = "https://magic-router.api.cloud.ru"

  ENDPOINTS = {
    "vpcs": "/v1/vpcs",
    "subnets": "/api/v1/subnets",
    "security_groups": "/api/v1/security-groups",
    "flavors": "/api/v1/flavors",
    "magic_routers": "/v1/magicRouters"
  }

  # discovery settings
  OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/discovery_output.json'))
  LOG_LEVEL = "INFO"

  @classmethod
  def validate(cls):
    # check all required keys loaded
    missing = [k for k in ["CLIENT_ID", "CLIENT_SECRET", "PROJECT_ID"] if not getattr(cls, k)]
    if missing:
      raise ValueError(f"Missing env var: {', '.join(missing)}")
