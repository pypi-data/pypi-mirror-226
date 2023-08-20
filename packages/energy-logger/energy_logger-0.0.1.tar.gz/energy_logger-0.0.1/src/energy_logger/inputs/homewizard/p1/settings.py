from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings


class HomeWizardP1Settings(BaseSettings):
    ipaddress: IPvAnyAddress
