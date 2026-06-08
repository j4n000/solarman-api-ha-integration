"""Constants for the Solarman Custom integration."""
from __future__ import annotations

from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

DOMAIN = "solarman_custom"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes
TOKEN_EXPIRY_BUFFER = 300  # Refresh token 5 min before expiry

CONF_APP_ID = "app_id"
CONF_APP_SECRET = "app_secret"
CONF_DEVICE_SN = "device_sn"

BASE_URL = "https://globalapi.solarmanpv.com"

# API Endpoints
ENDPOINT_TOKEN = "/account/v1.0/token"
ENDPOINT_STATION_LIST = "/station/v1.0/list"
ENDPOINT_STATION_BASE = "/station/v1.0/base"
ENDPOINT_STATION_REALTIME = "/station/v1.0/realTime"
ENDPOINT_STATION_DEVICE = "/station/v1.0/device"
ENDPOINT_STATION_HISTORY = "/station/v1.0/history"
ENDPOINT_DEVICE_CURRENT = "/device/v1.0/currentData"

PLATFORMS = ["sensor"]


# ─── Sensor Description Dataclass ────────────────────────────────────────────


@dataclass(frozen=True)
class SolarmanSensorDescription(SensorEntityDescription):
    """Describe a Solarman sensor."""

    api_key: str
    source: str = "inverter"  # inverter, battery, collector, station


# ─── Inverter Sensors ────────────────────────────────────────────────────────

INVERTER_SENSORS: tuple[SolarmanSensorDescription, ...] = (
    # ── PV Production ──
    SolarmanSensorDescription(
        key="pv_total_power",
        name="PV Total Power",
        api_key="DPi_t1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
    ),
    SolarmanSensorDescription(
        key="pv1_voltage",
        name="PV1 Voltage",
        api_key="PV1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SolarmanSensorDescription(
        key="pv1_current",
        name="PV1 Current",
        api_key="C_PV1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SolarmanSensorDescription(
        key="pv1_power",
        name="PV1 Power",
        api_key="PVi_P1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SolarmanSensorDescription(
        key="pv2_voltage",
        name="PV2 Voltage",
        api_key="PV4",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SolarmanSensorDescription(
        key="pv2_current",
        name="PV2 Current",
        api_key="C_PV4",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SolarmanSensorDescription(
        key="pv2_power",
        name="PV2 Power",
        api_key="PVi_P4",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    # ── AC Output ──
    SolarmanSensorDescription(
        key="ac_voltage_r",
        name="AC Voltage R",
        api_key="AV1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_voltage_s",
        name="AC Voltage S",
        api_key="AV2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_voltage_t",
        name="AC Voltage T",
        api_key="AV3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_current_r",
        name="AC Current R",
        api_key="AC1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_current_s",
        name="AC Current S",
        api_key="AC2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_current_t",
        name="AC Current T",
        api_key="AC3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_power_r",
        name="AC Power R",
        api_key="AP1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_power_s",
        name="AC Power S",
        api_key="AP2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_power_t",
        name="AC Power T",
        api_key="AP3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="ac_frequency",
        name="AC Frequency",
        api_key="A_Fo1",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:sine-wave",
    ),
    SolarmanSensorDescription(
        key="total_ac_output_power",
        name="Total AC Output Power",
        api_key="T_AC_OP",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    # ── Energy Totals ──
    SolarmanSensorDescription(
        key="cumulative_production",
        name="Cumulative Production",
        api_key="Et_ge0",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    SolarmanSensorDescription(
        key="daily_production",
        name="Daily Production",
        api_key="Etdy_ge1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:solar-power-variant",
    ),
    SolarmanSensorDescription(
        key="cumulative_grid_feed_in",
        name="Cumulative Grid Feed-in",
        api_key="Et_ge_ep0",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:transmission-tower-export",
    ),
    SolarmanSensorDescription(
        key="total_charging_energy",
        name="Total Charging Energy",
        api_key="t_cg_n1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="total_discharging_energy",
        name="Total Discharging Energy",
        api_key="t_dcg_n1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-arrow-down",
    ),
    # ── Battery (from inverter) ──
    SolarmanSensorDescription(
        key="battery_soc",
        name="Battery SoC",
        api_key="B_left_cap1",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="battery_power",
        name="Battery Power",
        api_key="B_P1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="battery_voltage",
        name="Battery Total Voltage",
        api_key="TV",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="battery_current",
        name="Battery Total Current",
        api_key="TC",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="battery_power_l1",
        name="Battery Power L1",
        api_key="BT_P_L1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="battery_power_l2",
        name="Battery Power L2",
        api_key="BT_P_L2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="battery_power_l3",
        name="Battery Power L3",
        api_key="BT_P_L3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    # ── Grid / Consumption ──
    SolarmanSensorDescription(
        key="total_consumption_power",
        name="Total Consumption Power",
        api_key="E_Puse_t1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
    ),
    SolarmanSensorDescription(
        key="total_grid_power",
        name="Total Grid Power",
        api_key="PG_Pt1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower",
    ),
    SolarmanSensorDescription(
        key="total_power_generation",
        name="Total Power Generation",
        api_key="TPG",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power-variant",
    ),
    # ── PCC (Point of Common Coupling) ──
    SolarmanSensorDescription(
        key="pcc_current_r",
        name="PCC Current R",
        api_key="PCC_AC1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    SolarmanSensorDescription(
        key="pcc_current_s",
        name="PCC Current S",
        api_key="PCC_AC2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    SolarmanSensorDescription(
        key="pcc_current_t",
        name="PCC Current T",
        api_key="PCC_AC3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    SolarmanSensorDescription(
        key="pcc_power_r",
        name="PCC Power R",
        api_key="PCC_AP1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    SolarmanSensorDescription(
        key="pcc_power_s",
        name="PCC Power S",
        api_key="PCC_AP2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    SolarmanSensorDescription(
        key="pcc_power_t",
        name="PCC Power T",
        api_key="PCC_AP3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    # ── Off-Grid ──
    SolarmanSensorDescription(
        key="offgrid_voltage_r",
        name="Off-Grid Voltage R",
        api_key="Vog_o1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:power-plug-off",
    ),
    SolarmanSensorDescription(
        key="offgrid_voltage_s",
        name="Off-Grid Voltage S",
        api_key="Vog_o2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:power-plug-off",
    ),
    SolarmanSensorDescription(
        key="offgrid_voltage_t",
        name="Off-Grid Voltage T",
        api_key="Vog_o3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:power-plug-off",
    ),
    # ── Temperatures ──
    SolarmanSensorDescription(
        key="module_temperature",
        name="Module Temperature",
        api_key="T_MDU1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SolarmanSensorDescription(
        key="radiator_temperature",
        name="Radiator Temperature",
        api_key="T_RDT2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SolarmanSensorDescription(
        key="ambient_temperature",
        name="Ambient Temperature",
        api_key="SPAT",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SolarmanSensorDescription(
        key="battery_temperature",
        name="Battery Temperature",
        api_key="T_BAP1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SolarmanSensorDescription(
        key="cell_average_temperature",
        name="Cell Average Temperature",
        api_key="CAT",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    # ── System Info ──
    SolarmanSensorDescription(
        key="inverter_status",
        name="Inverter Status",
        api_key="INV_ST1",
        icon="mdi:information-outline",
    ),
    SolarmanSensorDescription(
        key="bus_voltage",
        name="Bus Voltage",
        api_key="Bus_V1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SolarmanSensorDescription(
        key="insulation_resistance",
        name="Insulation Resistance",
        api_key="IPV",
        native_unit_of_measurement="kΩ",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:resistor",
    ),
    SolarmanSensorDescription(
        key="total_running_hours",
        name="Total Running Hours",
        api_key="t_w_hou1",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:clock-outline",
    ),
    SolarmanSensorDescription(
        key="generation_time_today",
        name="Generation Time Today",
        api_key="GE_T_TODAY",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:clock-outline",
    ),
    SolarmanSensorDescription(
        key="fan_speed",
        name="Fan Speed",
        api_key="SP_Fa",
        native_unit_of_measurement="rpm",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
)


# ─── Battery Pack Sensors (from separate battery device) ─────────────────────

BATTERY_SENSORS: tuple[SolarmanSensorDescription, ...] = (
    # Pack 1
    SolarmanSensorDescription(
        key="pack1_soc",
        name="Pack 1 SoC",
        api_key="BA_P_S1",
        source="battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack1_voltage",
        name="Pack 1 Voltage",
        api_key="BA_P_V1",
        source="battery",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack1_current",
        name="Pack 1 Current",
        api_key="BA_P_C1",
        source="battery",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack1_power",
        name="Pack 1 Power",
        api_key="BA_P_E1",
        source="battery",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="pack1_temperature",
        name="Pack 1 Temperature",
        api_key="BA_P_T1",
        source="battery",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    # Pack 2
    SolarmanSensorDescription(
        key="pack2_soc",
        name="Pack 2 SoC",
        api_key="BA_P_S2",
        source="battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack2_voltage",
        name="Pack 2 Voltage",
        api_key="BA_P_V2",
        source="battery",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack2_current",
        name="Pack 2 Current",
        api_key="BA_P_C2",
        source="battery",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="pack2_power",
        name="Pack 2 Power",
        api_key="BA_P_E2",
        source="battery",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="pack2_temperature",
        name="Pack 2 Temperature",
        api_key="BA_P_T2",
        source="battery",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
)


# ─── Station Overview Sensors ────────────────────────────────────────────────

STATION_SENSORS: tuple[SolarmanSensorDescription, ...] = (
    SolarmanSensorDescription(
        key="station_battery_soc",
        name="Station Battery SoC",
        api_key="batterySoc",
        source="station",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    SolarmanSensorDescription(
        key="station_generation_power",
        name="Station Generation Power",
        api_key="generationPower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
    ),
    SolarmanSensorDescription(
        key="station_generation_total",
        name="Station Total Generation",
        api_key="generationTotal",
        source="station",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    SolarmanSensorDescription(
        key="station_consumption_power",
        name="Station Consumption Power",
        api_key="usePower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
    ),
    SolarmanSensorDescription(
        key="station_battery_power",
        name="Station Battery Power",
        api_key="batteryPower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SolarmanSensorDescription(
        key="station_charge_power",
        name="Station Charge Power",
        api_key="chargePower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-arrow-up",
    ),
    SolarmanSensorDescription(
        key="station_discharge_power",
        name="Station Discharge Power",
        api_key="dischargePower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-arrow-down",
    ),
    SolarmanSensorDescription(
        key="station_grid_power",
        name="Station Grid Power",
        api_key="gridPower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower",
    ),
    SolarmanSensorDescription(
        key="station_wire_power",
        name="Station Wire Power",
        api_key="wirePower",
        source="station",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower",
    ),
)


# ─── Collector Sensors ───────────────────────────────────────────────────────

COLLECTOR_SENSORS: tuple[SolarmanSensorDescription, ...] = (
    SolarmanSensorDescription(
        key="wifi_signal_strength",
        name="WiFi Signal Strength",
        api_key="SGits1",
        source="collector",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:wifi",
    ),
    SolarmanSensorDescription(
        key="data_acquisition_period",
        name="Data Acquisition Period",
        api_key="COLLECT_PERIOD1",
        source="collector",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        icon="mdi:update",
    ),
    SolarmanSensorDescription(
        key="wifi_ssid",
        name="WiFi SSID",
        api_key="R_SSID",
        source="collector",
        icon="mdi:wifi",
    ),
)


# ─── All Sensor Definitions ─────────────────────────────────────────────────

ALL_SENSORS = INVERTER_SENSORS + BATTERY_SENSORS + STATION_SENSORS + COLLECTOR_SENSORS
