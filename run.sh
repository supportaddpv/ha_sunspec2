#!/usr/bin/with-contenv bashio

bashio::log.info "Starting pySunSpec2 SunSpec Modbus Client..."

# Export configuration as environment variables
export MODBUS_TYPE=$(bashio::config 'modbus_type')
export MODBUS_HOST=$(bashio::config 'modbus_host')
export MODBUS_PORT=$(bashio::config 'modbus_port')
export MODBUS_SLAVE_ID=$(bashio::config 'modbus_slave_id')
export SERIAL_PORT=$(bashio::config 'serial_port')
export SERIAL_BAUDRATE=$(bashio::config 'serial_baudrate')
export POLLING_INTERVAL=$(bashio::config 'polling_interval')
export MQTT_ENABLED=$(bashio::config 'mqtt_enabled')
export MQTT_BROKER=$(bashio::config 'mqtt_broker')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_USERNAME=$(bashio::config 'mqtt_username')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')
export MQTT_TOPIC_PREFIX=$(bashio::config 'mqtt_topic_prefix')

bashio::log.info "Configuration loaded:"
bashio::log.info "- Modbus Type: ${MODBUS_TYPE}"
bashio::log.info "- Polling Interval: ${POLLING_INTERVAL}s"
bashio::log.info "- MQTT Enabled: ${MQTT_ENABLED}"

# Start the Python application
python3 /app.py
