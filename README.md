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

**Tested with**: BRP072C42 Australia model (Firmware 1.16)

## Prerequisites

- Home Assistant 2023.1.0 or later
- Python 3.9 or later
- curl command available (usually pre-installed on most systems)
- Access to your local network where the Daikin AC unit will be installed

## Complete Setup Guide

### Step 1: Get Device Information from Sticker

**Before installing the module in your AC unit**, locate the sticker on your Daikin AC unit and record the following information:

1. **Device Key**: This is printed on the sticker attached to your Daikin AC unit
   - Example: `0406600515542`
   - **Important**: Keep this key safe - you'll need it for all API communications

2. **Model Information**: Note your model number for reference
   - Example: BRP072C42

### Step 2: Install Module in AC Unit

1. **Physical Installation**: Install the WiFi module in your Daikin AC unit following the manufacturer's instructions
2. **Power On**: Ensure the AC unit is powered on and the module is active

### Step 3: Join Module to WiFi Network

1. **Connect to WiFi**: Use the Daikin mobile app or web interface to connect the module to your local WiFi network
2. **Note the IP Address**: Record the IP address assigned to your AC unit (check your router's device list)
   - Example: `192.168.2.239`
3. **Critical Warning**: **Do not update the firmware** when first joining to WiFi, as this may disable the local API functionality

### Step 4: Generate and Register UUID

1. **Generate a UUID**:
   - Visit [UUIDgenerator.net](https://www.uuidgenerator.net/)
   - Generate a UUID and copy it **without the hyphens**
   - Example: `faac01b6a3e54e9e99a5f8242d9c8283`

2. **Register the UUID with your device**:
   ```bash
   curl --insecure -H "X-Daikin-uuid: YOUR_GENERATED_UUID" -v "https://YOUR_IP_ADDRESS/common/register_terminal?key=YOUR_DEVICE_KEY"
   ```
   
   Replace the placeholders:
   - `YOUR_GENERATED_UUID`: The UUID you generated (without hyphens)
   - `YOUR_IP_ADDRESS`: Your Daikin AC unit's IP address from Step 3
   - `YOUR_DEVICE_KEY`: Your device's authentication key from Step 1

   Example:
   ```bash
   curl --insecure -H "X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283" -v "https://192.168.2.239/common/register_terminal?key=0406600515542"
   ```

3. **Verify Registration**: You should receive a successful response indicating the UUID has been registered

### Step 5: Test API Access

Before proceeding to Home Assistant installation, verify that the API is accessible:

```bash
curl --insecure -H "X-Daikin-uuid: YOUR_GENERATED_UUID" "https://YOUR_IP_ADDRESS/common/basic_info?key=YOUR_DEVICE_KEY"
```

You should receive device information in response. If you get a 403 Forbidden error, repeat Step 4 to ensure the UUID is properly registered.

### Step 6: Install Integration in Home Assistant

1. **Download the integration**:
   ```bash
   git clone https://github.com/jalati2025/daikin-home-assistant.git
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

### Step 7: Configure Integration in Home Assistant

1. **Go to Settings → Devices & Services**
2. **Click "Add Integration"**
3. **Search for "Daikin Local"**
4. **Enter your device information**:
   - IP Address: The IP address from Step 3
   - UUID: The UUID you generated in Step 4
   - Key: The device key from Step 1
   - Name: `Daikin AC` (optional)

5. **Click "Submit"**

The integration will test the connection and create the entities.

### Step 8: Verify Installation

1. **Check Entities**: Verify that the following entities are created:
   - Climate entity for temperature and mode control
   - Sensor entities for temperature, humidity, and device status
   - Switch entities for power and fan direction

2. **Test Basic Functions**: Try turning the AC on/off and changing temperature to ensure everything works

## Troubleshooting

### Connection Issues

1. **Check IP Address**: Ensure the AC unit is accessible on your network
   ```bash
   ping YOUR_IP_ADDRESS
   ```

2. **Test with curl**: Use the basic info command to verify API access
   ```bash
   curl --insecure -H "X-Daikin-uuid: YOUR_UUID" "https://YOUR_IP/common/basic_info?key=YOUR_KEY"
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

### Common Error Messages

- **"Cannot connect"**: Check IP address, UUID, and key
- **"SSL Error"**: Ensure OpenSSL configuration is set up correctly
- **"403 Forbidden"**: Try running the register_terminal command again (Step 4)

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
python3 test_connection.py YOUR_IP YOUR_UUID YOUR_KEY
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Roadmap

### Auto UUID Generation
- **Streamlined Setup**: Implement automatic UUID generation functionality to simplify device setup
- **Reduced Manual Steps**: Users will only need to provide device key and IP address
- **Enhanced User Experience**: Eliminate the need for manual UUID generation and registration steps
- **Integration Enhancement**: Build UUID generation directly into the Home Assistant configuration flow

## Support

For support and questions:

1. Check the troubleshooting section above
2. Review the Home Assistant logs
3. Test with the provided scripts
4. Open an issue on GitHub with detailed information