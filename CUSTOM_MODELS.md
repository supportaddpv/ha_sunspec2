# Custom Models und Automatische Sensoren

## 1. Custom SunSpec Models hinzufügen

### Wo finde ich Models?

Offizielle SunSpec Models: https://github.com/sunspec/models/tree/master/smdx

### Models hinzufügen

1. **Model-Datei herunterladen** (z.B. `smdx_64110.xml` für SMA-spezifische Models)

2. **In das Add-on kopieren:**
   - Öffne Home Assistant
   - Gehe zu Settings → Add-ons → pySunSpec2
   - Klicke auf "Show in Sidebar" (falls noch nicht aktiv)
   - Im Dateibrowser: `/addon_configs/xxx_pysunspec2/models/smdx/`
   - Kopiere die `.xml` Datei dorthin

3. **Add-on neu starten**

### Alternative: Models direkt im Repository

Füge Models vor dem Build hinzu:

```
pysunspec2/
  sunspec2/
    models/
      smdx/
        smdx_64110.xml    <- Deine Custom Models hier
        smdx_64111.xml
      json/
        model_12345.json
```

Dann neu committen und pushen.

## 2. Automatische Sensoren in Home Assistant

Das Add-on nutzt jetzt **MQTT Discovery** - Sensoren werden automatisch erstellt!

### Was passiert automatisch:

1. ✅ Add-on liest alle SunSpec Models vom Gerät
2. ✅ Erstellt automatisch Home Assistant Sensoren via MQTT Discovery
3. ✅ Erkennt automatisch den Typ (Power, Energy, Voltage, Current, etc.)
4. ✅ Weist die richtigen Units zu (W, Wh, V, A, Hz, °C, etc.)
5. ✅ Gruppiert alle Sensoren unter einem Device

### Wo finde ich die Sensoren?

Nach dem Start des Add-ons:

1. Gehe zu **Settings** → **Devices & Services** → **MQTT**
2. Suche nach "SunSpec Device" oder dem Hersteller-Namen
3. Klicke drauf → Du siehst alle automatisch erstellten Sensoren

### Beispiel Sensoren:

- `common_0 Mn` - Manufacturer (Hersteller)
- `common_0 Md` - Model
- `common_0 SN` - Serial Number
- `inverter_0 W` - Active Power (W) ⚡
- `inverter_0 A` - Current (A)
- `inverter_0 V` - Voltage (V)
- `inverter_0 WH` - Energy (Wh) 📊
- `inverter_0 Hz` - Frequency (Hz)
- `inverter_0 TmpCab` - Temperature (°C) 🌡️

### Auto-Erkennung der Sensor-Typen:

Das Add-on erkennt automatisch anhand des Point-Namens:

| Point Name | Device Class | Unit |
|------------|--------------|------|
| W, DCW, ACW | power | W |
| WH, DCWh, ACWh | energy | Wh |
| A, DCA, ACA | current | A |
| V, DCV, ACV | voltage | V |
| Hz | frequency | Hz |
| Tmp, Temp | temperature | °C |
| PF | power_factor | - |
| Var | reactive_power | var |

### Manuelle Anpassungen (optional)

Falls du Sensoren manuell anpassen willst, kannst du das in der Home Assistant UI machen:

1. Settings → Devices & Services → MQTT → Dein Device
2. Klicke auf einen Sensor
3. Zahnrad-Symbol oben rechts
4. Ändere Name, Icon, Area, etc.

## 3. Sensoren in Dashboards nutzen

Die Sensoren können direkt in Dashboards verwendet werden:

```yaml
type: entities
title: Solar Inverter
entities:
  - sensor.common_0_mn
  - sensor.inverter_0_w
  - sensor.inverter_0_wh
  - sensor.inverter_0_a
  - sensor.inverter_0_v
```

Oder als Energie-Dashboard:

```yaml
type: energy-distribution
entities:
  - sensor.inverter_0_wh
```

## 4. Beispiel: Vollständiger Workflow

### SMA Inverter mit Custom Model 64110

1. **Model herunterladen:**
   ```
   https://github.com/sunspec/models/blob/master/smdx/smdx_64110.xml
   ```

2. **In Repository kopieren:**
   ```
   pysunspec2/sunspec2/models/smdx/smdx_64110.xml
   ```

3. **Committen und pushen:**
   ```bash
   git add pysunspec2/sunspec2/models/smdx/smdx_64110.xml
   git commit -m "Add SMA model 64110"
   git push
   ```

4. **Add-on aktualisieren in Home Assistant:**
   - Settings → Add-ons → pySunSpec2
   - Rebuild/Update

5. **Add-on neu starten**

6. **Sensoren erscheinen automatisch:**
   - Settings → Devices & Services → MQTT
   - "SunSpec Device" oder "SMA ..."
   - Alle Datenpunkte aus Model 64110 sind als Sensoren verfügbar!

## 5. Troubleshooting

### Sensoren erscheinen nicht

1. **MQTT aktiviert?**
   - Prüfe Add-on Konfiguration: `mqtt_enabled: true`

2. **MQTT Broker läuft?**
   - Settings → Add-ons → Mosquitto broker
   - Sollte "Running" sein

3. **Logs prüfen:**
   ```
   Settings → Add-ons → pySunSpec2 → Log
   ```
   Suche nach: "Published MQTT Discovery configs"

4. **MQTT Integration aktiv?**
   - Settings → Devices & Services
   - MQTT sollte konfiguriert sein

### Custom Model wird nicht gefunden

1. **Datei-Name korrekt?**
   - SMDX: `smdx_XXXXX.xml` (z.B. `smdx_64110.xml`)
   - JSON: `model_XXXXX.json`

2. **Datei im richtigen Verzeichnis?**
   - `/addon_configs/xxx_pysunspec2/models/smdx/`
   - Oder im Repository: `pysunspec2/sunspec2/models/smdx/`

3. **Add-on neu gebaut?**
   - Nach Änderungen im Repository: Add-on neu installieren
   - Bei Runtime-Änderungen: Add-on neu starten

## Support

Bei Problemen:
- Check Logs: Settings → Add-ons → pySunSpec2 → Log
- GitHub Issues: https://github.com/supportaddpv/ha_sunspec2/issues
