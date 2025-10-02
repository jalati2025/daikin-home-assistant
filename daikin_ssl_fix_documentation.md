# Daikin AC SSL Legacy Renegotiation Fix

## Problem Description

When attempting to connect to the Daikin AC unit (IP: 192.168.2.239) using curl, the following SSL error occurred:

```bash
curl: (35) OpenSSL/3.0.13: error:0A000152:SSL routines::unsafe legacy renegotiation disabled
```

## Root Cause

- **OpenSSL Version**: 3.0.13 (Ubuntu system)
- **Issue**: OpenSSL 3.0+ disabled unsafe legacy SSL renegotiation by default for security reasons
- **Daikin AC Firmware**: Uses older SSL/TLS implementation that requires legacy renegotiation
- **Device Info**: 
  - Model: DaikinAP64081
  - Firmware Version: 1_16_0
  - Revision: 182179A
  - MAC: 706655F8AF2E

## Solution Implemented

### 1. Created Custom OpenSSL Configuration

**File**: `/tmp/openssl_legacy.conf`

```ini
openssl_conf = openssl_init

[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
Options = UnsafeLegacyRenegotiation
```

### 2. Usage Method

To connect to the Daikin AC unit, use the custom OpenSSL configuration:

```bash
OPENSSL_CONF=/tmp/openssl_legacy.conf curl --insecure \
  -H "X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283" \
  "https://192.168.2.239/common/basic_info?key=0406600515542"
```

## Security Considerations

⚠️ **Important Security Notes**:

1. **Local Network Only**: This configuration should only be used for the local Daikin AC unit on your private network
2. **Temporary Solution**: The legacy renegotiation is disabled by default for security reasons
3. **Device-Specific**: This is required because the Daikin AC uses older firmware that hasn't been updated to support modern SSL/TLS standards
4. **Insecure Flag**: The `--insecure` flag is also required as the device likely uses self-signed certificates

## Working API Endpoints Discovered

After applying the fix, the following endpoints were confirmed working:

| Endpoint | Purpose | Response Status |
|----------|---------|-----------------|
| `/common/basic_info` | Device information | ✅ Working |
| `/common/get_datetime` | Current date/time | ✅ Working |
| `/common/get_notify` | Notification settings | ✅ Working |
| `/common/get_holiday` | Holiday mode status | ✅ Working |
| `/common/register_terminal` | Terminal registration | ✅ Working |

## Device Information Retrieved

```
Device Name: DaikinAP64081
Type: aircon
Region: th (Thailand)
Power Status: 0 (OFF)
Error Status: 0 (No errors)
Firmware Version: 1_16_0
Revision: 182179A
MAC Address: 706655F8AF2E
WiFi SSID: DaikinAP64081
Security Enabled: 1 (Yes)
Port: 30050
```

## Alternative Solutions (Not Implemented)

1. **System-wide OpenSSL Legacy Policy**: Would affect all SSL connections
2. **Older curl/OpenSSL Version**: Downgrading system packages (not recommended)
3. **Different HTTP Client**: Using tools like wget or python requests (may have same issue)

## Home Assistant Integration

This SSL fix has been integrated into a complete Home Assistant custom component:

- **Location**: `custom_components/daikin_local/`
- **Features**: Climate control, sensors, switches
- **Installation**: See `INSTALLATION.md` for detailed setup instructions
- **Testing**: Use `scripts/test_connection.py` to verify connectivity

The integration automatically handles the SSL configuration and provides a user-friendly interface for controlling your Daikin AC unit.

## Future Considerations

- Monitor for Daikin firmware updates that support modern SSL/TLS
- Consider using the configuration file only when needed
- Document any additional API endpoints discovered
- The Home Assistant integration provides a wrapper for easier access

## Command Reference

### Quick Connection Test
```bash
OPENSSL_CONF=/tmp/openssl_legacy.conf curl --insecure \
  -H "X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283" \
  "https://192.168.2.239/common/basic_info?key=0406600515542"
```

### Check Device Status
```bash
OPENSSL_CONF=/tmp/openssl_legacy.conf curl --insecure \
  -H "X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283" \
  "https://192.168.2.239/common/get_datetime?key=0406600515542"
```

---
*Documentation created: October 2, 2025*  
*System: Ubuntu Linux with OpenSSL 3.0.13*  
*Daikin AC Model: DaikinAP64081*