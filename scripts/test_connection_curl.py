#!/usr/bin/env python3
"""
Test script for Daikin AC connection using curl.
This script tests the connection to your Daikin AC unit and displays basic information.
"""

import argparse
import sys
import os
import tempfile
import subprocess
import json

def create_ssl_config():
    """Create temporary OpenSSL configuration for legacy renegotiation."""
    config_content = """openssl_conf = openssl_init

[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
Options = UnsafeLegacyRenegotiation
"""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
        f.write(config_content)
        return f.name

def make_curl_request(url, ssl_config_file):
    """Make a request using curl with SSL configuration."""
    try:
        # Set environment variable for OpenSSL legacy renegotiation
        env = os.environ.copy()
        env['OPENSSL_CONF'] = ssl_config_file
        
        result = subprocess.run([
            'curl', '--insecure', '--silent', '--show-error',
            '-H', 'X-Daikin-uuid: faac01b6a3e54e9e99a5f8242d9c8283',
            url
        ], capture_output=True, text=True, env=env, timeout=10)
        
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception(f"curl failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception("Request timed out")
    except FileNotFoundError:
        raise Exception("curl command not found")

def test_connection(ip_address, uuid, key, port=443):
    """Test connection to Daikin AC unit."""
    base_url = f"https://{ip_address}:{port}"
    ssl_config_file = create_ssl_config()
    
    try:
        print(f"Testing connection to {base_url}")
        print(f"UUID: {uuid}")
        print(f"Key: {key}")
        print("-" * 50)
        
        # Test basic info endpoint
        try:
            url = f"{base_url}/common/basic_info?key={key}"
            response = make_curl_request(url, ssl_config_file)
            
            print("✅ Basic Info:")
            for line in response.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except Exception as e:
            print(f"❌ Basic info failed: {e}")
            return False
        
        # Test control info endpoint
        try:
            url = f"{base_url}/aircon/get_control_info?key={key}"
            response = make_curl_request(url, ssl_config_file)
            
            print("\n✅ Control Info:")
            for line in response.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except Exception as e:
            print(f"❌ Control info failed: {e}")
            return False
        
        # Test sensor info endpoint
        try:
            url = f"{base_url}/aircon/get_sensor_info?key={key}"
            response = make_curl_request(url, ssl_config_file)
            
            print("\n✅ Sensor Info:")
            for line in response.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except Exception as e:
            print(f"❌ Sensor info failed: {e}")
            return False
        
        print("\n✅ All tests passed! Your Daikin AC is ready for Home Assistant integration.")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        # Clean up SSL config file
        try:
            os.unlink(ssl_config_file)
        except OSError:
            pass

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Daikin AC connection")
    parser.add_argument("ip_address", help="IP address of the Daikin AC unit")
    parser.add_argument("uuid", help="UUID of the Daikin AC unit")
    parser.add_argument("key", help="Key for the Daikin AC unit")
    parser.add_argument("--port", type=int, default=443, help="Port number (default: 443)")
    
    args = parser.parse_args()
    
    success = test_connection(args.ip_address, args.uuid, args.key, args.port)
    
    if success:
        print("\n🎉 Connection test successful!")
        print("You can now add this device to Home Assistant using the Daikin Local integration.")
        sys.exit(0)
    else:
        print("\n💥 Connection test failed!")
        print("Please check your IP address, UUID, and key.")
        sys.exit(1)

if __name__ == "__main__":
    main()
