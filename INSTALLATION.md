# Installation Guide - Daikin Local Home Assistant Integration

This guide will walk you through installing and configuring the Daikin Local integration for Home Assistant.

## Prerequisites

Before you begin, ensure you have:

- Home Assistant 2023.1.0 or later
- Your Daikin AC unit connected to your local network
- The following information from your Daikin AC unit:
  - IP Address (e.g., 192.168.2.239)
  - UUID (e.g., faac01b6a3e54e9e99a5f8242d9c8283)
  - Key (e.g., 0406600515542)

## Step 1: Download the Integration

### Option A: Clone the Repository
```bash
git clone https://github.com/josh/repos/daikin-home-assistant.git
cd daikin-home-assistant
```

### Option B: Download ZIP
1. Go to the repository page
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file

## Step 2: Install the Integration

### For Home Assistant OS/Supervised
1. Copy the `custom_components/daikin_local` folder to your Home Assistant config directory:
   ```bash
   cp -r custom_components/daikin_local /config/custom_components/
   ```

### For Home Assistant Core/Docker
1. Copy the `custom_components/daikin_local` folder to your Home Assistant config directory:
   ```bash
   cp -r custom_components/daikin_local /path/to/your/homeassistant/config/custom_components/
   ```

### For Home Assistant Container
1. Copy the `custom_components/daikin_local` folder to your Home Assistant config directory:
   ```bash
   docker cp custom_components/daikin_local homeassistant:/config/custom_components/
   ```

## Step 3: Restart Home Assistant

1. Go to **Settings** → **System** → **Restart**
2. Wait for Home Assistant to restart completely
3. The integration should now be available

## Step 4: Test Your Connection (Optional but Recommended)

Before adding the integration, test your connection:

```bash
cd scripts
python3 test_connection.py YOUR_IP_ADDRESS YOUR_UUID YOUR_KEY
```

Example:
```bash
python3 test_connection.py 192.168.2.239 faac01b6a3e54e9e99a5f8242d9c8283 0406600515542
```

If the test is successful, you'll see output like:
```
✅ Basic Info:
   ret: OK
   name: DaikinAP64081
   type: aircon
   ...

✅ All tests passed! Your Daikin AC is ready for Home Assistant integration.
```

## Step 5: Add the Integration

1. **Open Home Assistant** in your browser
2. **Go to Settings** → **Devices & Services**
3. **Click "Add Integration"** (bottom right)
4. **Search for "Daikin Local"**
5. **Click on "Daikin Local"** in the results
6. **Fill in the configuration form**:
   - **IP Address**: Enter your AC unit's IP address
   - **UUID**: Enter your AC unit's UUID
   - **Key**: Enter your AC unit's key
   - **Name**: Enter a friendly name (optional, defaults to "Daikin AC")
7. **Click "Submit"**

## Step 6: Verify Installation

After adding the integration, you should see:

1. **A new device** in Settings → Devices & Services
2. **Multiple entities** created:
   - `climate.daikin_ac` (or your custom name)
   - `sensor.daikin_ac_temperature`
   - `sensor.daikin_ac_humidity`
   - `sensor.daikin_ac_error_status`
   - `sensor.daikin_ac_firmware_version`
   - `switch.daikin_ac_power`
   - `switch.daikin_ac_fan_direction`

## Step 7: Test the Integration

1. **Go to Overview** in Home Assistant
2. **Find your climate entity** (it should appear as a climate card)
3. **Test basic functions**:
   - Turn the AC on/off
   - Change the temperature
   - Switch between modes (Auto, Cool, Heat, etc.)
   - Adjust fan speed

## Troubleshooting Installation

### Integration Not Found
- Ensure you copied the files to the correct location
- Check that the folder structure is correct: `custom_components/daikin_local/`
- Restart Home Assistant completely

### Connection Failed During Setup
- Verify your IP address, UUID, and key are correct
- Test the connection using the test script
- Check that your AC unit is powered on and connected to the network
- Ensure no firewall is blocking the connection

### SSL Errors
- Run the OpenSSL setup script:
  ```bash
  cd scripts
  python3 setup_openssl_config.py
  ```
- Test the connection again

### Entities Not Appearing
- Check the Home Assistant logs for errors
- Remove and re-add the integration
- Ensure the integration was added successfully

## Next Steps

Once the integration is working:

1. **Create automations** to control your AC based on temperature, time, or presence
2. **Add the climate entity to your dashboard** for easy access
3. **Set up scripts** for common AC operations
4. **Configure notifications** for errors or status changes

## Getting Help

If you encounter issues:

1. **Check the logs**: Go to Settings → System → Logs
2. **Test the connection**: Use the provided test script
3. **Review the documentation**: Check the README.md for detailed information
4. **Open an issue**: Create a GitHub issue with detailed information about your problem

## Uninstalling

To remove the integration:

1. **Go to Settings** → **Devices & Services**
2. **Find "Daikin Local"** in the integrations list
3. **Click on it** and then **"Delete"**
4. **Remove the files**:
   ```bash
   rm -rf /config/custom_components/daikin_local
   ```
5. **Restart Home Assistant**

## Security Notes

- This integration is designed for local network use only
- It bypasses SSL certificate verification for self-signed certificates
- The UUID and key provide authentication to your AC unit
- Keep your network secure and consider using a VPN for remote access
