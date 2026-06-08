# Solarman API - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/j4n000/solarman-api-ha-integration)](https://github.com/j4n000/solarman-api-ha-integration/releases)

Custom Home Assistant integration for the **Solarman Cloud API**, designed for Deye hybrid inverters with battery storage.

> The official Solarman integration barely reads any data. This integration provides **76 sensors** covering your entire solar system.

## ✨ Features

- ☀️ **PV Production** — String-level (PV1/PV2) voltage, current, power
- 🔋 **Battery Monitoring** — SoC, power, voltage, temperature (per pack!)
- ⚡ **AC / Grid** — 3-phase voltage, current, power, frequency
- 🏠 **Consumption** — Real-time household consumption
- 🔌 **PCC & Off-Grid** — Point of common coupling and off-grid outputs
- 🌡️ **Temperatures** — Inverter, radiator, battery, ambient
- 📊 **Energy Totals** — Daily/cumulative production, grid feed-in, charge/discharge
- 📈 **Station Overview** — Plant-level real-time summary data

## 📦 Supported Devices

| Device | Type |
|:---|:---|
| Deye HYD 5KTL-3PH | Hybrid inverter (3-phase) |
| Deye BTS 5K | Battery pack |
| Solarman WiFi Logger | Data collector |

## 📊 Sensors

| Category | Count | Examples |
|:---|:---|:---|
| Inverter | ~50 | PV power, AC phases, SoC, grid, temperatures |
| Battery | 10 | Pack 1 & 2 SoC, voltage, current, power, temperature |
| Station | 9 | Aggregated generation, consumption, grid, battery |
| Collector | 3 | WiFi signal strength, SSID |
| **Total** | **76** | |

## 🚀 Installation

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click the **⋮** menu (top right) → **Custom repositories**
3. Add:
   - **Repository**: `https://github.com/j4n000/solarman-api-ha-integration`
   - **Category**: Integration
4. Click **Add**
5. Search for **Solarman API** → **Download**
6. **Restart** Home Assistant
7. Go to **Settings → Devices & Services → Add Integration**
8. Search for **Solarman API**

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/j4n000/solarman-api-ha-integration.git

# Copy the custom_components folder to your HA config directory
cp -r solarman-api-ha-integration/custom_components/solarman_custom /config/custom_components/
```

Restart Home Assistant, then add the integration.

## ⚙️ Configuration

When adding the integration, provide the following:

| Field | Description |
|:---|:---|
| **Email** | Your Solarman account email |
| **Password** | Your Solarman password (hashed automatically) |
| **Application ID** | Solarman API App ID |
| **Application Secret** | Solarman API App Secret |
| **Inverter Serial Number** | Your inverter's serial number |

### Getting API Access

If you don't have an Application ID yet:
1. Register at [Solarman](https://www.solarmanpv.com)
2. Request API access via `service@solarmanpv.com`
3. You'll receive your `App ID` and `App Secret`

## 🔧 Technical Details

- **API Base URL**: `https://globalapi.solarmanpv.com` (international server)
- **Polling Interval**: Every 5 minutes
- **Token Management**: Automatic refresh (every 2 hours)
- **Device Discovery**: Automatically detects all devices (inverter, battery, collector)

## 🏗️ Architecture

The integration fetches data from 4 sources every 5 minutes:

| Source | Endpoint | Data |
|:---|:---|:---|
| Inverter | `/device/v1.0/currentData` | ~50 real-time data points |
| Battery | `/device/v1.0/currentData` | Per-pack SoC, power, temperature |
| Collector | `/device/v1.0/currentData` | WiFi signal, firmware info |
| Station | `/station/v1.0/realTime` | Aggregated plant overview |

## 🔍 Troubleshooting

| Issue | Solution |
|:---|:---|
| "appId or api is locked" | Wait 15-30 minutes, or verify your API credentials |
| No data showing | Check HA logs: filter for `solarman_custom` |
| PV values are 0 | Normal at night |
| Token expired | Tokens refresh automatically every 2 hours |

## 📄 License

MIT
