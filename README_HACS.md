# Daikin Local

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom component for controlling Daikin air conditioners that use self-signed SSL certificates and require legacy SSL renegotiation.

## Features

- **Climate Entity**: Full temperature control, mode switching (Auto, Cool, Heat, Dry, Fan), and fan speed control
- **Sensor Entities**: Current temperature, humidity, error status, and firmware version monitoring
- **Switch Entities**: Power control and fan direction swing toggle
- **SSL Support**: Handles self-signed certificates and legacy SSL renegotiation automatically
- **Secure Communication**: Uses UUID and key-based authentication

## Supported Devices

This integration is designed for Daikin air conditioners that:
- Use self-signed SSL certificates
- Require legacy SSL renegotiation (OpenSSL 3.0+ compatibility)
- Support the local API endpoints

**Tested with**: DaikinAP64081 (Firmware 1_16_0)

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Search for "Daikin Local" in HACS
3. Install the integration
4. Restart Home Assistant
5. Add the integration via Settings → Devices & Services

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/daikin_local` folder to your Home Assistant config directory
3. Restart Home Assistant
4. Add the integration via Settings → Devices & Services

## Configuration

You need three pieces of information from your Daikin AC unit:

1. **IP Address**: The local IP address of your AC unit
2. **UUID**: The device's unique identifier  
3. **Key**: The authentication key

### Finding Your Device Information

- Check your router's device list for the AC unit's IP
- Use the Daikin mobile app to find the UUID and key
- Or use the test script provided in this repository

### Test Connection

Before adding to Home Assistant, test your connection:

```bash
cd scripts
python3 test_connection_curl.py YOUR_IP_ADDRESS YOUR_UUID YOUR_KEY
```

## Usage

After installation, you'll have:

- **Climate Entity**: `climate.daikin_ac` - Main AC control
- **Temperature Sensor**: `sensor.daikin_ac_temperature` - Current room temperature
- **Humidity Sensor**: `sensor.daikin_ac_humidity` - Current room humidity
- **Error Status Sensor**: `sensor.daikin_ac_error_status` - Device error status
- **Firmware Version Sensor**: `sensor.daikin_ac_firmware_version` - Device firmware version
- **Power Switch**: `switch.daikin_ac_power` - Direct power control
- **Fan Direction Switch**: `switch.daikin_ac_fan_direction` - Fan swing on/off

## HVAC Modes

- **Off**: AC Off
- **Auto**: Automatic temperature control
- **Cool**: Cooling mode
- **Heat**: Heating mode  
- **Dry**: Dehumidifier mode
- **Fan Only**: Fan only mode

## Fan Speeds

- **Auto**: Automatic fan speed
- **Quiet**: Quiet/Low fan speed
- **Low**: Low fan speed
- **Medium**: Medium fan speed
- **High**: High fan speed
- **Max**: Maximum fan speed

## Temperature Range

- **Minimum**: 16°C
- **Maximum**: 32°C
- **Step**: 0.5°C

## Troubleshooting

### Connection Issues

1. **Check IP Address**: Ensure the AC unit is accessible on your network
2. **Test with Script**: Use the provided test script to verify connectivity
3. **Check Home Assistant Logs**: Look for error messages in the logs

### SSL Issues

The integration automatically handles SSL configuration for legacy renegotiation. If you encounter issues:

1. Ensure your AC unit is powered on and connected
2. Check that the IP address, UUID, and key are correct
3. Verify the unit is accessible on port 443

## Security Considerations

- **Local Network Only**: This integration is designed for local network use only
- **Self-Signed Certificates**: The integration bypasses SSL verification for self-signed certificates
- **Legacy SSL**: Uses legacy SSL renegotiation which is disabled by default in modern OpenSSL
- **Authentication**: Uses UUID and key-based authentication

## Support

- **Documentation**: See the main README.md for complete details
- **Issues**: Create a GitHub issue with detailed information about your problem
- **Testing**: Use the provided test scripts to verify your setup

## License

This project is licensed under the MIT License.
