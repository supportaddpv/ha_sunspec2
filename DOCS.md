# Documentation

## Overview

The pySunSpec2 Home Assistant Add-on enables communication with SunSpec compliant devices (such as solar inverters, battery systems, and meters) using the Modbus protocol. The add-on automatically discovers all SunSpec models present on the device and publishes the data to MQTT for easy integration with Home Assistant.

## Quick Start

1. **Install the Add-on**: Follow the installation instructions in the README
2. **Configure**: Set up your Modbus connection (TCP or RTU) and MQTT settings
3. **Start**: Launch the add-on and check the logs
4. **Integrate**: Use MQTT sensors in Home Assistant to display the data

## Configuration Details

### Modbus TCP Configuration

For devices connected via Ethernet/WiFi:

```yaml
modbus_type: tcp
modbus_host: 192.168.1.100  # IP address of your device
modbus_port: 502             # Standard Modbus TCP port
modbus_slave_id: 1           # Usually 1, check device documentation
```

**Common TCP Ports:**
- 502 (standard Modbus TCP)
- 1502 (some manufacturers)
- Check your device's manual for the correct port

### Modbus RTU Configuration

For devices connected via RS485/serial:

```yaml
modbus_type: rtu
modbus_slave_id: 1           # Check device DIP switches or settings
serial_port: /dev/ttyUSB0    # USB-to-RS485 adapter
serial_baudrate: 9600        # Common: 9600, 19200, 38400
```

**Finding Serial Ports:**
- USB adapters: `/dev/ttyUSB0`, `/dev/ttyUSB1`, etc.
- Built-in serial: `/dev/ttyAMA0`, `/dev/ttyS0`, etc.
- Check Home Assistant hardware page for available ports

### MQTT Configuration

```yaml
mqtt_enabled: true
mqtt_broker: core-mosquitto  # Use Home Assistant's Mosquitto add-on
mqtt_port: 1883
mqtt_username: ""            # Optional, leave empty if not needed
mqtt_password: ""            # Optional, leave empty if not needed
mqtt_topic_prefix: sunspec   # Customize to avoid conflicts
```

**MQTT Broker Options:**
- `core-mosquitto` - Home Assistant's built-in MQTT broker (recommended)
- Custom broker IP - If using external MQTT server

### Polling Configuration

```yaml
polling_interval: 30  # Seconds between reads
```

**Recommended Intervals:**
- Solar inverters: 5-30 seconds
- Battery systems: 10-60 seconds
- Meters: 30-300 seconds

⚠️ **Warning**: Too frequent polling may overload the device or Modbus network

## MQTT Data Structure

### Full Data Topic

`sunspec/data` contains complete JSON dump:

```json
{
  "common_0": {
    "Mn": "Manufacturer",
    "Md": "Model",
    "SN": "SerialNumber"
  },
  "inverter_0": {
    "W": 5000,
    "A": 23.5,
    "V": 230.1
  }
}
```

### Individual Topics

Each point is published separately for easy Home Assistant integration:

```
sunspec/common_0/Mn → "SMA"
sunspec/common_0/Md → "STP 10000TL-20"
sunspec/inverter_0/W → 5000
sunspec/inverter_0/A → 23.5
```

## Home Assistant Integration

### MQTT Sensors

Add sensors to your `configuration.yaml`:

```yaml
mqtt:
  sensor:
    # Power output
    - name: "Solar Power"
      state_topic: "sunspec/inverter_0/W"
      unit_of_measurement: "W"
      device_class: power
      state_class: measurement

    # Current
    - name: "Solar Current"
      state_topic: "sunspec/inverter_0/A"
      unit_of_measurement: "A"
      device_class: current
      state_class: measurement

    # Voltage
    - name: "Solar Voltage"
      state_topic: "sunspec/inverter_0/V"
      unit_of_measurement: "V"
      device_class: voltage
      state_class: measurement

    # Energy (if available)
    - name: "Solar Energy Today"
      state_topic: "sunspec/inverter_0/WH"
      unit_of_measurement: "Wh"
      device_class: energy
      state_class: total_increasing
```

### Finding Available Topics

1. Open MQTT Explorer or similar tool
2. Connect to your MQTT broker
3. Browse topics under your prefix (e.g., `sunspec/`)
4. Identify the topics you want to use

Or check the add-on logs:

```
Published data to MQTT (X models)
```

## SunSpec Models

Common SunSpec models you may encounter:

| Model ID | Name | Description |
|----------|------|-------------|
| 1 | Common | Basic device info (manufacturer, model, serial) |
| 101-103 | Inverter | Single/Split/Three phase inverter |
| 111-113 | Inverter | Extended inverter models |
| 120-126 | Nameplate | Nameplate ratings |
| 124 | Storage | Battery storage system |
| 160 | MPPT | Maximum Power Point Tracker |
| 201-204 | Meter | Single/Split/Wye/Delta meter |
| 701-715 | DER | Distributed Energy Resource controls |

The add-on automatically detects all available models on your device.

## Troubleshooting

### Connection Issues

**"Failed to connect to device"**
- Verify IP address and port (TCP) or serial port (RTU)
- Check firewall settings
- Ensure device is powered on and network-accessible
- Try increasing the slave ID (some devices use 2, 3, etc.)

**"No models found"**
- Device may not support SunSpec
- Try different Modbus addresses in the device settings
- Check device documentation for SunSpec support

### MQTT Issues

**"Failed to connect to MQTT"**
- Ensure Mosquitto add-on is running
- Verify MQTT credentials if authentication is enabled
- Check MQTT broker accessibility

**"No data in Home Assistant"**
- Check MQTT topics using MQTT Explorer
- Verify sensor configuration in `configuration.yaml`
- Restart Home Assistant after adding sensors

### Performance Issues

**Device becomes unresponsive**
- Increase `polling_interval` to reduce load
- Check Modbus network quality (RTU)
- Reduce concurrent Modbus connections

**High CPU usage**
- Increase polling interval
- Disable MQTT if not needed for testing

## Advanced Usage

### Custom Models

If you have custom SunSpec models, place model definition files in:
- `/opt/sunspec2/models/smdx/` (SMDX format)
- `/opt/sunspec2/models/json/` (JSON format)

### Multiple Devices

To monitor multiple devices:
1. Install multiple instances of the add-on
2. Configure different MQTT topic prefixes
3. Use different slave IDs or connections

Example:
- Instance 1: `mqtt_topic_prefix: sunspec/inverter1`
- Instance 2: `mqtt_topic_prefix: sunspec/inverter2`

### Logging

Check add-on logs for detailed information:
- Device connection status
- Models discovered
- Data read/published
- Errors and warnings

## Examples

### SMA Sunny Boy Inverter (TCP)

```yaml
modbus_type: tcp
modbus_host: 192.168.1.50
modbus_port: 502
modbus_slave_id: 3
polling_interval: 10
```

### Fronius Inverter (TCP)

```yaml
modbus_type: tcp
modbus_host: 192.168.1.60
modbus_port: 502
modbus_slave_id: 1
polling_interval: 5
```

### Generic RTU Device

```yaml
modbus_type: rtu
modbus_slave_id: 1
serial_port: /dev/ttyUSB0
serial_baudrate: 19200
polling_interval: 30
```

## Support

- **Add-on Issues**: GitHub repository
- **pySunSpec2 Documentation**: https://github.com/sunspec/pysunspec2
- **SunSpec Alliance**: https://sunspec.org/

## References

- [SunSpec Alliance](https://sunspec.org/)
- [SunSpec Information Models](https://sunspec.org/information-models/)
- [pySunSpec2 GitHub](https://github.com/sunspec/pysunspec2)
- [Home Assistant MQTT Integration](https://www.home-assistant.io/integrations/mqtt/)
