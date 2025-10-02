"""Daikin Local API client."""
import logging
import os
import subprocess
import tempfile
from typing import Any, Dict, Optional

from .const import (
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    ENDPOINT_BASIC_INFO,
    ENDPOINT_CONTROL_INFO,
    ENDPOINT_SENSOR_INFO,
    ENDPOINT_SET_CONTROL,
    ENDPOINT_REGISTER_TERMINAL,
)

_LOGGER = logging.getLogger(__name__)


class DaikinClient:
    """Client for communicating with Daikin air conditioner."""

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
CipherString = DEFAULT@SECLEVEL=0
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
            
            result = subprocess.run([
                'curl', '--insecure', '--silent', '--show-error',
                '--tlsv1.2', '--ciphers', 'DEFAULT@SECLEVEL=0',
                '-H', f'X-Daikin-uuid: {self.uuid}',
                '-H', 'User-Agent: HomeAssistant-DaikinLocal/1.0',
                url
            ], capture_output=True, text=True, env=env, timeout=DEFAULT_TIMEOUT)
            
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
            _LOGGER.error("Request failed: %s", err)
            raise

    def _make_set_request(self, endpoint: str, params: Dict[str, Any]) -> bool:
        """Make a set request to the Daikin API using curl."""
        url = f"{self.base_url}{endpoint}"
        
        # Add key to parameters
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
            
            result = subprocess.run([
                'curl', '--insecure', '--silent', '--show-error',
                '--tlsv1.2', '--ciphers', 'DEFAULT@SECLEVEL=0',
                '-H', f'X-Daikin-uuid: {self.uuid}',
                '-H', 'User-Agent: HomeAssistant-DaikinLocal/1.0',
                url
            ], capture_output=True, text=True, env=env, timeout=DEFAULT_TIMEOUT)
            
            if result.returncode != 0:
                _LOGGER.error("Set request failed: %s", result.stderr)
                return False
            
            # Check response
            return "ret=OK" in result.stdout
            
        except subprocess.TimeoutExpired:
            _LOGGER.error("Set request timed out")
            return False
        except FileNotFoundError:
            _LOGGER.error("curl command not found")
            return False
        except Exception as err:
            _LOGGER.error("Unexpected error in set request: %s", err)
            return False

    def test_connection(self) -> bool:
        """Test connection to the Daikin unit."""
        try:
            data = self._make_request(ENDPOINT_BASIC_INFO)
            return "ret" in data and data["ret"] == "OK"
        except Exception as err:
            _LOGGER.error("Connection test failed: %s", err)
            return False

    def register_terminal(self) -> bool:
        """Register this terminal with the Daikin unit."""
        try:
            data = self._make_request(ENDPOINT_REGISTER_TERMINAL)
            return "ret" in data and data["ret"] == "OK"
        except Exception as err:
            _LOGGER.error("Terminal registration failed: %s", err)
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

    def set_control_info(self, **kwargs) -> bool:
        """Set control parameters."""
        # Ensure all required parameters are present
        required_params = ["pow", "mode", "stemp", "shum", "f_rate", "f_dir"]
        params = {}
        
        for param in required_params:
            if param in kwargs:
                params[param] = kwargs[param]
            else:
                # Set defaults if not provided
                if param == "pow":
                    params[param] = "1"
                elif param == "mode":
                    params[param] = "1"  # Auto mode
                elif param == "stemp":
                    params[param] = "22.0"
                elif param == "shum":
                    params[param] = "0"
                elif param == "f_rate":
                    params[param] = "A"  # Auto fan
                elif param == "f_dir":
                    params[param] = "0"
        
        return self._make_set_request(ENDPOINT_SET_CONTROL, params)

    def close(self):
        """Close the client and cleanup resources."""
        if self._ssl_config_file:
            try:
                os.unlink(self._ssl_config_file)
            except OSError:
                pass
            self._ssl_config_file = None
