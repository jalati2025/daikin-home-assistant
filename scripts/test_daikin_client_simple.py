#!/usr/bin/env python3
"""
Simple test script for the DaikinClient class without Home Assistant dependencies.
"""

import sys
import os
import tempfile
import subprocess
from typing import Any, Dict, Optional

# Constants (copied from const.py)
DEFAULT_TIMEOUT = 10
ENDPOINT_BASIC_INFO = "/common/basic_info"
ENDPOINT_CONTROL_INFO = "/aircon/get_control_info"
ENDPOINT_SENSOR_INFO = "/aircon/get_sensor_info"

class SimpleDaikinClient:
    """Simplified DaikinClient for testing."""
    
    def __init__(self, ip_address: str, uuid: str, key: str, port: int = 443):
        """Initialize the Daikin client."""
        self.ip_address = ip_address
        self.uuid = uuid
        self.key = key
        self.port = port
        self.base_url = f"https://{ip_address}:{port}"
        self._ssl_config_file = None

    def _create_ssl_config(self) -> str:
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

    def _get_ssl_config(self) -> str:
        """Get or create SSL configuration file."""
        if self._ssl_config_file is None:
            self._ssl_config_file = self._create_ssl_config()
        return self._ssl_config_file

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Daikin API using curl."""
        url = f"{self.base_url}{endpoint}"
        
        # Add key to parameters
        if params is None:
            params = {}
        params["key"] = self.key
        
        # Build query string
        query_parts = []
        for key, value in params.items():
            query_parts.append(f"{key}={value}")
        query_string = "&".join(query_parts)
        
        if query_string:
            url = f"{url}?{query_string}"
        
        ssl_config_file = self._get_ssl_config()
        
        try:
            # Set environment variable for OpenSSL legacy renegotiation
            env = os.environ.copy()
            env['OPENSSL_CONF'] = ssl_config_file
            
            cmd = [
                'curl', '--insecure', '--silent', '--show-error',
                '-H', f'X-Daikin-uuid: {self.uuid}',
                '-H', 'User-Agent: HomeAssistant-DaikinLocal/1.0',
                url
            ]
            print(f"Running command: {' '.join(cmd)}")
            print(f"OPENSSL_CONF: {env.get('OPENSSL_CONF')}")
            print(f"SSL config file exists: {os.path.exists(ssl_config_file)}")
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=DEFAULT_TIMEOUT)
            
            if result.returncode != 0:
                raise Exception(f"curl failed: {result.stderr}")
            
            # Parse response
            data = {}
            for line in result.stdout.strip().split(','):
                if '=' in line:
                    key, value = line.split('=', 1)
                    data[key] = value
            
            return data
            
        except subprocess.TimeoutExpired:
            raise Exception("Request timed out")
        except FileNotFoundError:
            raise Exception("curl command not found")
        except Exception as err:
            print(f"Request failed: {err}")
            raise

    def test_connection(self) -> bool:
        """Test connection to the Daikin unit."""
        try:
            data = self._make_request(ENDPOINT_BASIC_INFO)
            return "ret" in data and data["ret"] == "OK"
        except Exception as err:
            print(f"Connection test failed: {err}")
            return False

    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic device information."""
        return self._make_request(ENDPOINT_BASIC_INFO)

    def get_control_info(self) -> Dict[str, Any]:
        """Get current control settings."""
        return self._make_request(ENDPOINT_CONTROL_INFO)

    def get_sensor_info(self) -> Dict[str, Any]:
        """Get current sensor data."""
        return self._make_request(ENDPOINT_SENSOR_INFO)

    def close(self):
        """Close the client and cleanup resources."""
        if self._ssl_config_file:
            try:
                os.unlink(self._ssl_config_file)
            except OSError:
                pass
            self._ssl_config_file = None

def test_client():
    """Test the SimpleDaikinClient class."""
    print("Testing SimpleDaikinClient...")
    
    # Create client
    client = SimpleDaikinClient(
        ip_address="192.168.2.239",
        uuid="faac01b6a3e54e9e99a5f8242d9c8283",
        key="0406600515542",
        port=443
    )
    
    try:
        # Test connection
        print("Testing connection...")
        if client.test_connection():
            print("✅ Connection test passed!")
        else:
            print("❌ Connection test failed!")
            return False
        
        # Test basic info
        print("Getting basic info...")
        basic_info = client.get_basic_info()
        print(f"✅ Basic info: {basic_info.get('name', 'Unknown')} - {basic_info.get('ver', 'Unknown')}")
        
        # Test control info
        print("Getting control info...")
        control_info = client.get_control_info()
        print(f"✅ Control info: Power={control_info.get('pow', 'Unknown')}, Mode={control_info.get('mode', 'Unknown')}")
        
        # Test sensor info
        print("Getting sensor info...")
        sensor_info = client.get_sensor_info()
        print(f"✅ Sensor info: Temp={sensor_info.get('htemp', 'Unknown')}°C, Humidity={sensor_info.get('hhum', 'Unknown')}%")
        
        print("\n🎉 All tests passed! The DaikinClient is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = test_client()
    sys.exit(0 if success else 1)
