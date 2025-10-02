# Quick Reference - Daikin Local Home Assistant Integration

## Installation Checklist

- [ ] Download the integration files
- [ ] Copy `custom_components/daikin_local` to Home Assistant config
- [ ] Restart Home Assistant
- [ ] Test connection: `python3 scripts/test_connection.py IP UUID KEY`
- [ ] Add integration via Settings → Devices & Services
- [ ] Verify entities are created

## Your Device Information

**IP Address**: `192.168.2.239`  
**UUID**: `faac01b6a3e54e9e99a5f8242d9c8283`  
**Key**: `0406600515542`  
**Model**: DaikinAP64081  
**Firmware**: 1_16_0  

## Quick Test Commands

```bash
# Test connection
python3 scripts/test_connection.py 192.168.2.239 faac01b6a3e54e9e99a5f8242d9c8283 0406600515542

# Setup OpenSSL config
python3 scripts/setup_openssl_config.py

# Manual curl test
OPENSSL_CONF=/tmp/openssl_legacy.conf curl --insecure \
  -H "X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283" \
  "https://192.168.2.239/common/basic_info?key=0406600515542"
```

## Entities Created

| Entity Type | Entity ID | Description |
|-------------|-----------|-------------|
| Climate | `climate.daikin_ac` | Main AC control |
| Sensor | `sensor.daikin_ac_temperature` | Current temperature |
| Sensor | `sensor.daikin_ac_humidity` | Current humidity |
| Sensor | `sensor.daikin_ac_error_status` | Error status |
| Sensor | `sensor.daikin_ac_firmware_version` | Firmware version |
| Switch | `switch.daikin_ac_power` | Power on/off |
| Switch | `switch.daikin_ac_fan_direction` | Fan swing |

## Common Operations

### Turn AC On (Auto Mode, 22°C)
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.daikin_ac
data:
  hvac_mode: auto
  temperature: 22
```

### Turn AC Off
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.daikin_ac
data:
  hvac_mode: off
```

### Set Cool Mode
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.daikin_ac
data:
  hvac_mode: cool
  temperature: 20
```

### Set Heat Mode
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.daikin_ac
data:
  hvac_mode: heat
  temperature: 24
```

### Change Fan Speed
```yaml
service: climate.set_fan_mode
target:
  entity_id: climate.daikin_ac
data:
  fan_mode: high
```

## HVAC Modes

| Mode | Description | Temperature Range |
|------|-------------|-------------------|
| `off` | AC Off | N/A |
| `auto` | Automatic | 16-32°C |
| `cool` | Cooling | 16-32°C |
| `heat` | Heating | 16-32°C |
| `dry` | Dehumidify | 16-32°C |
| `fan_only` | Fan Only | N/A |

## Fan Speeds

| Speed | Description |
|-------|-------------|
| `auto` | Automatic |
| `quiet` | Quiet/Low |
| `low` | Low |
| `medium` | Medium |
| `high` | High |
| `max` | Maximum |

## Troubleshooting

### Connection Failed
1. Check IP address: `ping 192.168.2.239`
2. Test with script: `python3 scripts/test_connection.py ...`
3. Check Home Assistant logs

### SSL Errors
1. Run: `python3 scripts/setup_openssl_config.py`
2. Test connection again
3. Check OpenSSL version

### Entities Not Updating
1. Check device connectivity
2. Restart integration
3. Check Home Assistant logs

### 403 Forbidden
1. Run register_terminal command first
2. Check UUID and key
3. Verify device is powered on

## File Locations

```
daikin-home-assistant/
├── custom_components/daikin_local/    # Home Assistant integration
├── scripts/                           # Test and utility scripts
├── README.md                          # Full documentation
├── INSTALLATION.md                    # Installation guide
├── daikin_ac_commands.txt             # Manual API commands
└── daikin_ssl_fix_documentation.md    # SSL fix documentation
```

## Support

- **Documentation**: See README.md for complete details
- **Installation**: See INSTALLATION.md for step-by-step setup
- **Testing**: Use scripts/test_connection.py to verify setup
- **Issues**: Check Home Assistant logs and test scripts first
