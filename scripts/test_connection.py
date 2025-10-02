#!/usr/bin/env python3
"""
Test script for Daikin AC connection.
This script tests the connection to your Daikin AC unit and displays basic information.
"""

import argparse
import sys
import os
import tempfile
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

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

def make_request(session, url, params, ssl_config_file):
    """Make a request with SSL configuration."""
    # Set environment variable for OpenSSL legacy renegotiation
    old_openssl_conf = os.environ.get('OPENSSL_CONF')
    os.environ['OPENSSL_CONF'] = ssl_config_file
    
    try:
        response = session.get(
            url,
            params=params,
            verify=False,  # Self-signed certificate
            timeout=10
        )
        response.raise_for_status()
        return response
    finally:
        # Restore original OpenSSL config
        if old_openssl_conf:
            os.environ['OPENSSL_CONF'] = old_openssl_conf
        else:
            os.environ.pop('OPENSSL_CONF', None)

def test_connection(ip_address, uuid, key, port=443):
    """Test connection to Daikin AC unit."""
    base_url = f"https://{ip_address}:{port}"
    ssl_config_file = create_ssl_config()
    
    try:
        # Create session
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers
        session.headers.update({
            "X-Daikin-uuid": uuid,
            "User-Agent": "Daikin-Test-Script/1.0"
        })
        
        print(f"Testing connection to {base_url}")
        print(f"UUID: {uuid}")
        print(f"Key: {key}")
        print("-" * 50)
        
        # Test basic info endpoint
        try:
            response = make_request(
                session,
                f"{base_url}/common/basic_info",
                {"key": key},
                ssl_config_file
            )
            
            print("✅ Basic Info:")
            for line in response.text.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Basic info failed: {e}")
            return False
        
        # Test control info endpoint
        try:
            response = make_request(
                session,
                f"{base_url}/aircon/get_control_info",
                {"key": key},
                ssl_config_file
            )
            
            print("\n✅ Control Info:")
            for line in response.text.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Control info failed: {e}")
            return False
        
        # Test sensor info endpoint
        try:
            response = make_request(
                session,
                f"{base_url}/aircon/get_sensor_info",
                {"key": key},
                ssl_config_file
            )
            
            print("\n✅ Sensor Info:")
            for line in response.text.strip().split(','):
                if '=' in line:
                    key_val, value = line.split('=', 1)
                    print(f"   {key_val}: {value}")
            
        except requests.exceptions.RequestException as e:
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