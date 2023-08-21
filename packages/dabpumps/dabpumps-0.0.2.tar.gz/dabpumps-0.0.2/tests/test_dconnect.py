import os
from datetime import UTC, datetime

import aiounittest
from aiohttp import ClientSession
from aioresponses import aioresponses

from dabpumps.auth import Auth
from dabpumps.const import (
    API_BASE_URL,
    API_GET_DUMSTATE,
    API_GET_INSTALLATION,
    API_GET_INSTALLATION_LIST,
    API_GET_TOKEN,
)
from dabpumps.dconnect import DConnect
from dabpumps.exceptions import InvalidAuthError
from dabpumps.pump import MeasureSystem, PumpState, PumpStatus, SystemStatus

ACCESS_TOKEN = "access-token"
INSTALLATION_ID = "installation-id"
PUMP_SERIAL = "pump-serial"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as file:
        return file.read()


class TestDConnect(aiounittest.AsyncTestCase):
    def setUp(self):
        """Setup things to be run when tests are started."""

    @aioresponses()
    async def test_authenticate_ok(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        auth = Auth(ClientSession(), "email", "password")
        await auth.authenticate()

        self.assertEqual(ACCESS_TOKEN, auth.access_token)
        self.assertGreaterEqual((auth.access_token_expires - datetime.now(UTC)).days, 364)

    @aioresponses()
    async def test_authenticate_wrong_credential(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_wrong_credential.json"),
        )

        auth = Auth(ClientSession(), "email", "password")
        with self.assertRaises(InvalidAuthError):
            await auth.authenticate()

    @aioresponses()
    async def test_get_installations_ok(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_INSTALLATION_LIST}",
            body=load_fixture("get_installations_ok.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        installations = await dconnect.get_installations()

        self.assertEqual(1, len(installations))

        first = installations[0]
        self.assertEqual("installation-id", first.installation_id)
        self.assertEqual("installation-name", first.name)
        self.assertEqual("installation-description", first.description)
        self.assertEqual("installation-address", first.address)
        self.assertEqual("OK", first.status)

    @aioresponses()
    async def test_get_installations_forbidden(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_INSTALLATION_LIST}",
            body=load_fixture("get_installations_forbidden.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        with self.assertRaises(InvalidAuthError):
            await dconnect.get_installations()

    @aioresponses()
    async def test_get_pumps(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_INSTALLATION}/{INSTALLATION_ID}",
            body=load_fixture("get_installation.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        pumps = await dconnect.get_pumps(INSTALLATION_ID)

        self.assertEqual(1, len(pumps))

        first = pumps[0]
        self.assertEqual("pump-name", first.name)
        self.assertEqual(PUMP_SERIAL, first.serial)
        self.assertEqual("OK", first.status)
        self.assertEqual("E.sybox Mini", first.product_name)

    @aioresponses()
    async def test_get_pump_state_international_standby(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_DUMSTATE}/{PUMP_SERIAL}",
            body=load_fixture("get_dumstate_international_standby.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        ps: PumpState = await dconnect.get_pump_state(PUMP_SERIAL)

        self.assertEqual(datetime.fromisoformat("2023-07-11T13:17:31.173+00:00"), ps.timestamp)
        self.assertEqual(20, ps.sample_rate)
        self.assertEqual("mac-wlan", ps.mac_wlan)
        self.assertEqual("essid", ps.essid)
        self.assertEqual(2.7, ps.setpoint_pressure_bar)
        self.assertEqual(None, ps.setpoint_pressure_psi)
        self.assertEqual(0.3, ps.restart_pressure_bar)
        self.assertEqual(None, ps.restart_pressure_psi)
        self.assertEqual(PumpStatus.STANDBY, ps.pump_status)
        self.assertEqual(MeasureSystem.INTERNATIONAL, ps.measure_system)
        self.assertEqual(0, ps.rotating_speed_rpm)
        self.assertEqual(2.5, ps.pressure_bar)
        self.assertEqual(None, ps.pressure_psi)
        self.assertEqual(5, len(ps.errors))
        self.assertEqual(SystemStatus.LOW_VOLTAGE_VSL, ps.errors[0].status)
        self.assertEqual(datetime.fromisoformat("2023-05-28 07:59:15+00:00"), ps.errors[0].time)

    @aioresponses()
    async def test_get_pump_state_anglo_american_standby(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_DUMSTATE}/{PUMP_SERIAL}",
            body=load_fixture("get_dumstate_anglo_american_standby.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        ps = await dconnect.get_pump_state(PUMP_SERIAL)

        self.assertEqual(datetime.fromisoformat("2023-07-31T06:17:15.241+00:00"), ps.timestamp)
        self.assertEqual(None, ps.setpoint_pressure_bar)
        self.assertEqual(39.2, ps.setpoint_pressure_psi)
        self.assertEqual(None, ps.restart_pressure_bar)
        self.assertEqual(4.4, ps.restart_pressure_psi)
        self.assertEqual(MeasureSystem.ANGLO_AMERICAN, ps.measure_system)
        self.assertEqual(None, ps.pressure_bar)
        self.assertEqual(38.5, ps.pressure_psi)

    @aioresponses()
    async def test_get_pump_state_anglo_american_go(self, mock):
        mock.post(
            f"{API_BASE_URL}/{API_GET_TOKEN}",
            body=load_fixture("get_token_ok.json"),
        )

        mock.get(
            f"{API_BASE_URL}/{API_GET_DUMSTATE}/{PUMP_SERIAL}",
            body=load_fixture("get_dumstate_anglo_american_go.json"),
        )

        dconnect = DConnect(Auth(ClientSession(), "email", "password"))
        ps = await dconnect.get_pump_state(PUMP_SERIAL)

        self.assertEqual(PumpStatus.GO, ps.pump_status)
        self.assertEqual(2577, ps.rotating_speed_rpm)
