# Solarman API - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/j4n000/solarman-api-ha-integration)](https://github.com/j4n000/solarman-api-ha-integration/releases)

Egyedi Home Assistant integráció a **Solarman Cloud API**-hoz, Deye hibrid inverterekhez.

> A hivatalos Solarman integráció alig olvas ki adatot. Ez az integráció **76 szenzort** biztosít a teljes napelemes rendszeredből.

## ✨ Funkciók

- ☀️ **PV termelés** — String szintű (PV1/PV2) feszültség, áram, teljesítmény
- 🔋 **Akkumulátor** — SoC, teljesítmény, feszültség, hőmérséklet (pack szinten!)
- ⚡ **AC / Grid** — 3 fázisú feszültség, áram, teljesítmény, frekvencia
- 🏠 **Fogyasztás** — Valós idejű háztartási fogyasztás
- 🔌 **PCC & Off-Grid** — Csatlakozási pont és off-grid kimenetek
- 🌡️ **Hőmérsékletek** — Inverter, radiátor, akkumulátor, környezeti
- 📊 **Energia összesítők** — Napi/összes termelés, grid feed-in, töltés/kisütés
- 📈 **Station áttekintés** — Erőmű szintű valós idejű adatok

## 📦 Támogatott eszközök

| Eszköz | Típus |
|:---|:---|
| Deye HYD 5KTL-3PH | Hibrid inverter (3 fázis) |
| Deye BTS 5K | Akkumulátor csomag |
| Solarman WiFi Logger | Adatgyűjtő |

## 📊 Szenzorok

| Kategória | Darab | Példák |
|:---|:---|:---|
| Inverter | ~50 | PV power, AC fázisok, SoC, grid, hőmérsékletek |
| Akkumulátor | 10 | Pack 1 & 2 SoC, feszültség, áram, teljesítmény, hőm. |
| Station | 9 | Összesített termelés, fogyasztás, grid, akku |
| Collector | 3 | WiFi jelszint, SSID |
| **Összesen** | **76** | |

## 🚀 Telepítés

### HACS-on keresztül (ajánlott)

1. Nyisd meg a **HACS**-ot a Home Assistant-ban
2. Kattints a jobb felső sarokban a **⋮** menüre → **Custom repositories**
3. Add hozzá:
   - **Repository**: `https://github.com/j4n000/solarman-api-ha-integration`
   - **Category**: Integration
4. Kattints az **Add** gombra
5. Keresd meg: **Solarman API** → **Download**
6. **Indítsd újra** a Home Assistant-ot
7. Menj a **Beállítások → Eszközök és szolgáltatások → Integráció hozzáadása**
8. Keresd meg: **Solarman API**

### Manuális telepítés

```bash
# Klónozd a repót
git clone https://github.com/j4n000/solarman-api-ha-integration.git

# Másold a custom_components mappát a HA config-ba
cp -r solarman-api-ha-integration/custom_components/solarman_custom /config/custom_components/
```

Indítsd újra a Home Assistant-ot, majd add hozzá az integrációt.

## ⚙️ Konfiguráció

Az integráció hozzáadásakor add meg:

| Mező | Leírás |
|:---|:---|
| **Email** | Solarman fiók email cím |
| **Password** | Solarman jelszó (a rendszer hash-eli) |
| **Application ID** | Solarman API App ID |
| **Application Secret** | Solarman API App Secret |
| **Inverter Serial Number** | Az inverter sorozatszáma |

### API hozzáférés megszerzése

Ha még nincs Application ID-d:
1. Regisztrálj a [Solarman](https://www.solarmanpv.com) oldalon
2. Kérd az API hozzáférést: `service@solarmanpv.com`
3. Megkapod az `App ID`-t és `App Secret`-et

## 🔧 Technikai részletek

- **API**: `https://globalapi.solarmanpv.com` (nemzetközi szerver)
- **Frissítés**: 5 percenként
- **Token**: Automatikus frissítés (2 óránként)
- **Device discovery**: Automatikusan megtalálja az összes eszközt

## 🔍 Hibaelhárítás

| Hiba | Megoldás |
|:---|:---|
| "appId or api is locked" | Várj 15-30 percet, vagy ellenőrizd az API adatokat |
| Nem jelenik meg adat | Nézd a HA logokat: `solarman_custom` |
| PV értékek 0 | Éjszaka normális |

## 📄 Licensz

MIT
