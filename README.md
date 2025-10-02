# Daikin Local Home Assistant Integration

A custom Home Assistant integration for controlling Daikin air conditioners that use self-signed SSL certificates and require legacy SSL renegotiation.

## Features

- **Climate Entity**: Full temperature control, mode switching (Auto, Cool, Heat, Dry, Fan), and fan speed control
- **Sensor Entities**: Current temperature, humidity, error status, and firmware version monitoring
- **Switch Entities**: Power control and fan direction swing toggle
- **SSL Support**: Handles self-signed certificates and legacy SSL renegotiation
- **Secure Communication**: Uses UUID and key-based authentication

## Supported Devices

This integration is designed for Daikin air conditioners that:
- Use self-signed SSL certificates
- Require legacy SSL renegotiation (OpenSSL 3.0+ compatibility)
- Support the local API endpoints documented in this repository

**Tested with**: DaikinAP64081 (Firmware 1_16_0)

## Prerequisites

- Home Assistant 2023.1.0 or later
- Python 3.9 or later
- Your Daikin AC unit's IP address, UUID, and key
- The unit must be accessible on your local network
- curl command available (usually pre-installed on most systems)

## Installation

### Method 1: Manual Installation (Recommended)

1. **Download the integration**:
   ```bash
   git clone https://github.com/josh/repos/daikin-home-assistant.git
   cd daikin-home-assistant
   ```

2. **Copy to Home Assistant**:
   ```bash
   # Copy the custom_components directory to your Home Assistant config directory
   cp -r custom_components/daikin_local /path/to/homeassistant/config/custom_components/
   ```

3. **Restart Home Assistant**:
   - Go to Settings → System → Restart
   - Or restart your Home Assistant instance

### Method 2: HACS Installation (Future)

This integration will be available through HACS in a future release.

## Configuration

### Step 1: Find Your Device Information

You need three pieces of information from your Daikin AC unit:

1. **IP Address**: The local IP address of your AC unit
2. **UUID**: The device's unique identifier
3. **Key**: The authentication key

You can find these by:
- Checking your router's device list for the AC unit's IP
- Using the Daikin mobile app to find the UUID and key
- Or using the test script provided in this repository

### Step 2: Test Connection

Before adding to Home Assistant, test your connection:

```bash
cd scripts
python3 test_connection_curl.py YOUR_IP_ADDRESS YOUR_UUID YOUR_KEY
```

Example:
```bash
python3 test_connection_curl.py 192.168.2.239 faac01b6a3e54e9e99a5f8242d9c8283 0406600515542
```

**Note**: The integration uses port 443 by default (not 30050) as this is where your Daikin unit is accessible.

### Step 3: Add Integration in Home Assistant

1. **Go to Settings → Devices & Services**
2. **Click "Add Integration"**
3. **Search for "Daikin Local"**
4. **Enter your device information**:
   - IP Address: `192.168.2.239`
   - UUID: `faac01b6a3e54e9e99a5f8242d9c8283`
   - Key: `0406600515542`
   - Name: `Daikin AC` (optional)

5. **Click "Submit"**

The integration will test the connection and create the entities.

## Entities Created

### Climate Entity
- **Name**: `climate.daikin_ac` (or your custom name)
- **Features**:
  - Temperature control (16°C - 32°C)
  - HVAC modes: Off, Auto, Cool, Heat, Dry, Fan Only
  - Fan speeds: Auto, Quiet, Low, Medium, High, Max
  - Power on/off

### Sensor Entities
- **Temperature Sensor**: Current room temperature
- **Humidity Sensor**: Current room humidity
- **Error Status Sensor**: Device error status
- **Firmware Version Sensor**: Device firmware version

### Switch Entities
- **Power Switch**: Direct power control
- **Fan Direction Switch**: Fan swing on/off

## Usage Examples

### Automations

```yaml
# Turn on AC when temperature is high
automation:
  - alias: "Turn on AC when hot"
    trigger:
      - platform: numeric_state
        entity_id: sensor.daikin_ac_temperature
        above: 25
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.daikin_ac
        data:
          hvac_mode: cool
      - service: climate.set_temperature
        target:
          entity_id: climate.daikin_ac
        data:
          temperature: 22

# Turn off AC when leaving home
automation:
  - alias: "Turn off AC when leaving"
    trigger:
      - platform: state
        entity_id: person.your_name
        to: "not_home"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.daikin_ac
        data:
          hvac_mode: off
```

### Scripts

```yaml
# Quick cool down script
script:
  quick_cool:
    alias: "Quick Cool Down"
    sequence:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.daikin_ac
        data:
          hvac_mode: cool
      - service: climate.set_temperature
        target:
          entity_id: climate.daikin_ac
        data:
          temperature: 18
      - service: climate.set_fan_mode
        target:
          entity_id: climate.daikin_ac
        data:
          fan_mode: high
```

## Troubleshooting

### Connection Issues

1. **Check IP Address**: Ensure the AC unit is accessible on your network
   ```bash
   ping 192.168.2.239
   ```

2. **Test with curl**: Use the provided commands in `daikin_ac_commands.txt`
   ```bash
   OPENSSL_CONF=/tmp/openssl_legacy.conf curl --insecure \
     -H "X-Daikin-uuid: YOUR_UUID" \
     "https://YOUR_IP/common/basic_info?key=YOUR_KEY"
   ```

3. **Check Home Assistant logs**: Look for error messages in the logs

### SSL Issues

If you encounter SSL errors:

1. **Setup OpenSSL configuration**:
   ```bash
   cd scripts
   python3 setup_openssl_config.py
   ```

2. **Verify the configuration works**:
   ```bash
   python3 test_connection.py YOUR_IP YOUR_UUID YOUR_KEY
   ```

### Entity Not Updating

1. **Check device connectivity**: Ensure the AC unit is powered on and connected
2. **Restart the integration**: Remove and re-add the integration
3. **Check Home Assistant logs**: Look for specific error messages

### Common Error Messages

- **"Cannot connect"**: Check IP address, UUID, and key
- **"SSL Error"**: Ensure OpenSSL configuration is set up correctly
- **"403 Forbidden"**: Try running the register_terminal command first

## API Reference

The integration uses the following Daikin API endpoints:

- `/common/basic_info` - Device information
- `/aircon/get_control_info` - Current control settings
- `/aircon/get_sensor_info` - Current sensor data
- `/aircon/set_control_info` - Set control parameters
- `/common/register_terminal` - Register terminal (if needed)

### Control Parameters

| Parameter | Description | Values |
|-----------|-------------|---------|
| `pow` | Power | 0=Off, 1=On |
| `mode` | Mode | 0=Fan, 1=Auto, 2=Dry, 3=Cool, 4=Heat |
| `stemp` | Set Temperature | 16.0 to 32.0 (°C) |
| `shum` | Set Humidity | 0 (usually 0 for auto) |
| `f_rate` | Fan Rate | A=Auto, B=Quiet, 3=Low, 4=Med, 5=High, 6=Max |
| `f_dir` | Fan Direction | 0=Default, 1=Swing |

## Security Considerations

- **Local Network Only**: This integration is designed for local network use only
- **Self-Signed Certificates**: The integration bypasses SSL verification for self-signed certificates
- **Legacy SSL**: Uses legacy SSL renegotiation which is disabled by default in modern OpenSSL
- **Authentication**: Uses UUID and key-based authentication

## Development

### Project Structure

```
daikin-home-assistant/
├── custom_components/
│   └── daikin_local/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── daikin_client.py
│       ├── climate.py
│       ├── sensor.py
│       └── switch.py
├── scripts/
│   ├── test_connection.py
│   └── setup_openssl_config.py
├── daikin_ac_commands.txt
├── daikin_ssl_fix_documentation.md
└── README.md
```

### Testing

Run the test script to verify your setup:

```bash
cd scripts
python3 test_connection.py 192.168.2.239 faac01b6a3e54e9e99a5f8242d9c8283 0406600515542
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

1. Check the troubleshooting section above
2. Review the Home Assistant logs
3. Test with the provided scripts
4. Open an issue on GitHub with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Climate entity with full temperature and mode control
- Sensor entities for temperature, humidity, and device status
- Switch entities for power and fan direction
- SSL support with legacy renegotiation
- Comprehensive documentation and test scripts

## Acknowledgments

- Based on the Daikin API documentation and testing
- SSL fix inspired by the OpenSSL legacy renegotiation workaround
- Home Assistant integration patterns from the official documentation
