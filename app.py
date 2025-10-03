#!/usr/bin/env python3
"""
pySunSpec2 Home Assistant Add-on
Reads SunSpec Modbus devices and publishes to MQTT
"""

import os
import sys
import time
import json
import logging
from typing import Optional, Dict, Any

# Add sunspec2 to path
sys.path.insert(0, '/opt')

import sunspec2.modbus.client as modbus_client
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SunSpecMQTTBridge:
    """Bridge between SunSpec Modbus device and MQTT"""

    def __init__(self):
        self.config = self._load_config()
        self.device = None
        self.mqtt_client = None
        self.running = True

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            'modbus_type': os.getenv('MODBUS_TYPE', 'tcp'),
            'modbus_host': os.getenv('MODBUS_HOST', '192.168.1.100'),
            'modbus_port': int(os.getenv('MODBUS_PORT', '502')),
            'modbus_slave_id': int(os.getenv('MODBUS_SLAVE_ID', '1')),
            'serial_port': os.getenv('SERIAL_PORT', '/dev/ttyUSB0'),
            'serial_baudrate': int(os.getenv('SERIAL_BAUDRATE', '9600')),
            'polling_interval': int(os.getenv('POLLING_INTERVAL', '30')),
            'mqtt_enabled': os.getenv('MQTT_ENABLED', 'true').lower() == 'true',
            'mqtt_broker': os.getenv('MQTT_BROKER', 'core-mosquitto'),
            'mqtt_port': int(os.getenv('MQTT_PORT', '1883')),
            'mqtt_username': os.getenv('MQTT_USERNAME', ''),
            'mqtt_password': os.getenv('MQTT_PASSWORD', ''),
            'mqtt_topic_prefix': os.getenv('MQTT_TOPIC_PREFIX', 'sunspec')
        }

    def connect_device(self) -> bool:
        """Connect to SunSpec Modbus device"""
        try:
            logger.info(f"Connecting to {self.config['modbus_type'].upper()} device...")

            if self.config['modbus_type'] == 'tcp':
                self.device = modbus_client.SunSpecModbusClientDeviceTCP(
                    slave_id=self.config['modbus_slave_id'],
                    ipaddr=self.config['modbus_host'],
                    ipport=self.config['modbus_port']
                )
            elif self.config['modbus_type'] == 'rtu':
                self.device = modbus_client.SunSpecModbusClientDeviceRTU(
                    slave_id=self.config['modbus_slave_id'],
                    name=self.config['serial_port'],
                    baudrate=self.config['serial_baudrate']
                )
            else:
                logger.error(f"Unknown modbus type: {self.config['modbus_type']}")
                return False

            # Scan for models
            logger.info("Scanning for SunSpec models...")
            self.device.scan()

            logger.info(f"Found models: {list(self.device.models.keys())}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to device: {e}")
            return False

    def connect_mqtt(self) -> bool:
        """Connect to MQTT broker"""
        if not self.config['mqtt_enabled']:
            logger.info("MQTT disabled in configuration")
            return False

        try:
            logger.info(f"Connecting to MQTT broker: {self.config['mqtt_broker']}:{self.config['mqtt_port']}")

            self.mqtt_client = mqtt.Client()

            if self.config['mqtt_username']:
                self.mqtt_client.username_pw_set(
                    self.config['mqtt_username'],
                    self.config['mqtt_password']
                )

            self.mqtt_client.on_connect = self._on_mqtt_connect
            self.mqtt_client.on_disconnect = self._on_mqtt_disconnect

            self.mqtt_client.connect(
                self.config['mqtt_broker'],
                self.config['mqtt_port'],
                60
            )

            self.mqtt_client.loop_start()
            return True

        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {e}")
            return False

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("Connected to MQTT broker")
        else:
            logger.error(f"MQTT connection failed with code: {rc}")

    def _on_mqtt_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        logger.warning(f"Disconnected from MQTT broker with code: {rc}")

    def read_device_data(self) -> Dict[str, Any]:
        """Read all data from device"""
        data = {}

        try:
            # Read all models
            for model_id, model_list in self.device.models.items():
                if isinstance(model_id, int):  # Only process numeric IDs
                    for idx, model in enumerate(model_list):
                        try:
                            model.read()
                            model_name = model.model_type.name if hasattr(model.model_type, 'name') else str(model_id)
                            model_data = self._extract_model_data(model)
                            data[f"{model_name}_{idx}"] = model_data
                        except Exception as e:
                            logger.warning(f"Failed to read model {model_id}[{idx}]: {e}")

            return data

        except Exception as e:
            logger.error(f"Failed to read device data: {e}")
            return {}

    def _extract_model_data(self, model) -> Dict[str, Any]:
        """Extract data from a model"""
        data = {}

        try:
            # Extract points
            if hasattr(model, 'points'):
                for point_name, point in model.points.items():
                    try:
                        # Use cvalue if available (computed value with scale factor)
                        if hasattr(point, 'cvalue') and point.cvalue is not None:
                            data[point_name] = point.cvalue
                        elif hasattr(point, 'value') and point.value is not None:
                            data[point_name] = point.value
                    except Exception as e:
                        logger.debug(f"Failed to read point {point_name}: {e}")

            # Extract groups
            if hasattr(model, 'groups'):
                for group_name, group_list in model.groups.items():
                    if isinstance(group_list, list):
                        for idx, group in enumerate(group_list):
                            group_data = self._extract_group_data(group)
                            data[f"{group_name}_{idx}"] = group_data

        except Exception as e:
            logger.debug(f"Failed to extract model data: {e}")

        return data

    def _extract_group_data(self, group) -> Dict[str, Any]:
        """Extract data from a group"""
        data = {}

        try:
            if hasattr(group, 'points'):
                for point_name, point in group.points.items():
                    try:
                        if hasattr(point, 'cvalue') and point.cvalue is not None:
                            data[point_name] = point.cvalue
                        elif hasattr(point, 'value') and point.value is not None:
                            data[point_name] = point.value
                    except Exception as e:
                        logger.debug(f"Failed to read group point {point_name}: {e}")

        except Exception as e:
            logger.debug(f"Failed to extract group data: {e}")

        return data

    def publish_to_mqtt(self, data: Dict[str, Any]):
        """Publish data to MQTT"""
        if not self.mqtt_client or not data:
            return

        try:
            # Publish full data as JSON
            topic = f"{self.config['mqtt_topic_prefix']}/data"
            payload = json.dumps(data, default=str)
            self.mqtt_client.publish(topic, payload, retain=True)

            # Publish individual values
            for model_name, model_data in data.items():
                if isinstance(model_data, dict):
                    for point_name, value in model_data.items():
                        topic = f"{self.config['mqtt_topic_prefix']}/{model_name}/{point_name}"
                        self.mqtt_client.publish(topic, str(value), retain=True)

            logger.info(f"Published data to MQTT ({len(data)} models)")

        except Exception as e:
            logger.error(f"Failed to publish to MQTT: {e}")

    def run(self):
        """Main loop"""
        logger.info("Starting pySunSpec2 MQTT Bridge")

        # Connect to device
        if not self.connect_device():
            logger.error("Failed to connect to device, exiting")
            return

        # Connect to MQTT
        self.connect_mqtt()

        # Main loop
        try:
            while self.running:
                logger.info("Reading device data...")
                data = self.read_device_data()

                if data:
                    logger.info(f"Read {len(data)} models from device")

                    if self.config['mqtt_enabled'] and self.mqtt_client:
                        self.publish_to_mqtt(data)
                    else:
                        # Just log the data if MQTT is disabled
                        logger.info(f"Data: {json.dumps(data, indent=2, default=str)}")
                else:
                    logger.warning("No data read from device")

                # Wait for next poll
                logger.info(f"Waiting {self.config['polling_interval']}s until next poll...")
                time.sleep(self.config['polling_interval'])

        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up...")

        if self.device:
            try:
                self.device.close()
            except Exception as e:
                logger.error(f"Error closing device: {e}")

        if self.mqtt_client:
            try:
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting MQTT: {e}")


if __name__ == '__main__':
    bridge = SunSpecMQTTBridge()
    bridge.run()
