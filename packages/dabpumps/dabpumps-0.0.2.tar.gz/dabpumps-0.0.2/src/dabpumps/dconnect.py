import json
from datetime import datetime

from dabpumps.auth import Auth
from dabpumps.const import API_GET_DUMSTATE, API_GET_INSTALLATION, API_GET_INSTALLATION_LIST
from dabpumps.installation import Installation
from dabpumps.pump import Pump, PumpState


class DConnect:
    """API for interacting with the DAB Pumps DConnect service."""

    def __init__(self, auth: Auth) -> None:
        self._auth = auth

    async def get_installations(self) -> list[Installation]:
        json_dict = await self._auth.request("get", API_GET_INSTALLATION_LIST)
        return [Installation(data) for data in json_dict["rows"]]

    async def get_pumps(self, installation_id: str) -> list[Pump]:
        json_dict = await self._auth.request("get", f"{API_GET_INSTALLATION}/{installation_id}")
        return [Pump(data) for data in json.loads(json_dict["data"])["dumlist"]]

    async def get_pump_state(self, pump_serial: str) -> PumpState:
        json_dict = await self._auth.request("get", f"{API_GET_DUMSTATE}/{pump_serial}")
        timestamp = datetime.fromisoformat(json_dict["statusts"].replace("Z", "+00:00"))
        data = json.loads(json_dict["status"])
        return PumpState(timestamp, data)
