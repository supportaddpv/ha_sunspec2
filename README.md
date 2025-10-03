# pySunSpec2 Home Assistant Add-on

Home Assistant Add-on for reading SunSpec compliant devices (solar inverters, battery systems, etc.) via Modbus TCP/RTU and publishing data to MQTT.

## About

This add-on uses the pySunSpec2 library to communicate with SunSpec compliant devices using Modbus protocol. It automatically discovers all available SunSpec models on the device and publishes the data to MQTT for integration with Home Assistant.

## Features

- Support for Modbus TCP and Modbus RTU connections
- Automatic SunSpec model discovery
- Publishes data to MQTT with configurable topics
- Configurable polling interval
- Works with solar inverters, battery systems, and other SunSpec devices

## Installation

### Step 1: Add Repository to Home Assistant

1. Go to **Settings** > **Add-ons** > **Add-on Store**
2. Click the **⋮** (three dots) in the top right corner
3. Select **Repositories**
4. Add this URL:
   ```
   https://github.com/supportaddpv/ha_sunspec2
   ```
5. Click **Add**

### Step 2: Install the Add-on

1. Refresh the Add-on Store page
2. Find "pySunSpec2 SunSpec Modbus Client" in the list
3. Click on it and click **Install**
4. Wait for the installation to complete

### Step 3: Configure

1. Go to the **Configuration** tab
2. Set your Modbus connection details (TCP or RTU)
3. Configure MQTT settings
4. Save the configuration

### Step 4: Start

1. Go to the **Info** tab
2. Click **Start**
3. Check the **Log** tab for any errors

## Configuration

### Modbus TCP Example

```yaml
modbus_type: tcp
modbus_host: 192.168.1.100
modbus_port: 502
modbus_slave_id: 1
polling_interval: 30
mqtt_enabled: true
mqtt_broker: core-mosquitto
mqtt_port: 1883
mqtt_topic_prefix: sunspec
```

### Modbus RTU Example

```yaml
modbus_type: rtu
modbus_slave_id: 1
serial_port: /dev/ttyUSB0
serial_baudrate: 9600
polling_interval: 30
mqtt_enabled: true
mqtt_broker: core-mosquitto
mqtt_port: 1883
mqtt_topic_prefix: sunspec
```

## Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `modbus_type` | list | Yes | `tcp` | Connection type: `tcp` or `rtu` |
| `modbus_host` | string | Yes (TCP) | `192.168.1.100` | IP address of Modbus TCP device |
| `modbus_port` | int | Yes (TCP) | `502` | Port of Modbus TCP device |
| `modbus_slave_id` | int | Yes | `1` | Modbus slave ID (1-247) |
| `serial_port` | string | Yes (RTU) | `/dev/ttyUSB0` | Serial port for RTU connection |
| `serial_baudrate` | int | Yes (RTU) | `9600` | Baudrate for serial connection |
| `polling_interval` | int | Yes | `30` | Seconds between polls (5-3600) |
| `mqtt_enabled` | bool | Yes | `true` | Enable MQTT publishing |
| `mqtt_broker` | string | Yes | `core-mosquitto` | MQTT broker hostname |
| `mqtt_port` | int | Yes | `1883` | MQTT broker port |
| `mqtt_username` | string | No | - | MQTT username (if required) |
| `mqtt_password` | password | No | - | MQTT password (if required) |
| `mqtt_topic_prefix` | string | Yes | `sunspec` | MQTT topic prefix |

## MQTT Topics

Data is published to MQTT in two formats:

1. **Complete data dump**: `sunspec/data` (JSON)
2. **Individual values**: `sunspec/{model_name}_{index}/{point_name}`

Example topics:
- `sunspec/data` - Full JSON payload
- `sunspec/common_0/Mn` - Manufacturer name
- `sunspec/common_0/Md` - Model name
- `sunspec/inverter_0/W` - Active power (W)
- `sunspec/inverter_0/A` - Current (A)

## Supported Devices

This add-on supports all SunSpec compliant devices, including:
- Solar inverters (SMA, Fronius, SolarEdge, Huawei, etc.)
- Battery systems
- Meters
- Weather stations
- Any device implementing SunSpec models

## Support

For issues and questions:
- GitHub Issues: [Your Repository URL]
- pySunSpec2 Documentation: https://github.com/sunspec/pysunspec2

## License

Copyright (c) 2020 SunSpec Alliance - See LICENSE file

## Credits

Based on pySunSpec2 by SunSpec Alliance
