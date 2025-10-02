# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2025-01-02

### Fixed
- SSL connection robustness with multiple fallback configurations
- SSL unexpected EOF errors (0A000126) with enhanced error handling
- Improved compatibility with OpenSSL 3.5.2+ in Home Assistant environment
- Added retry logic and better timeout handling for unreliable connections

### Improved
- Enhanced OpenSSL configuration with MinProtocol and MaxProtocol settings
- Multiple SSL configuration fallbacks (TLSv1.2 → TLSv1)
- Comprehensive error logging and debugging information
- Better reliability across different OpenSSL versions

## [1.0.3] - 2025-01-02

### Fixed
- Home Assistant compatibility issue with FanMode import
- ImportError: cannot import name 'FanMode' from 'homeassistant.components.climate'
- Improved compatibility with different Home Assistant versions

## [1.0.2] - 2025-01-02

### Fixed
- SSL connection issues in Home Assistant environment
- SSL signature type error (0A000172) by adding CipherString configuration
- Improved SSL compatibility with additional curl flags (--tlsv1.2, --ciphers)
- Updated OpenSSL configuration to include SECLEVEL=0 for legacy devices

## [1.0.1] - 2025-01-02

### Added
- HACS support and configuration files
- README_HACS.md for HACS display
- hacs.json configuration file
- Updated manifest.json with HACS requirements

## [1.0.0] - 2025-01-02

### Added
- Initial release of Daikin Local Home Assistant integration
- Complete climate entity with temperature control and mode switching
- Sensor entities for temperature, humidity, error status, and firmware version
- Switch entities for power control and fan direction
- SSL support with legacy renegotiation for self-signed certificates
- Configuration flow for easy setup
- Comprehensive documentation and installation guides
- Test scripts for connection verification
- Support for DaikinAP64081 and similar models
- Automatic SSL configuration handling
- curl-based API client for reliable SSL connections

### Features
- **Climate Control**: Full temperature range (16-32°C), all HVAC modes (Auto, Cool, Heat, Dry, Fan)
- **Fan Control**: Multiple fan speeds (Auto, Quiet, Low, Medium, High, Max)
- **Sensor Monitoring**: Real-time temperature, humidity, and device status
- **Switch Controls**: Power on/off and fan direction swing
- **SSL Security**: Handles self-signed certificates and legacy SSL renegotiation
- **Authentication**: Secure UUID and key-based authentication
- **Error Handling**: Comprehensive error handling and logging
- **Documentation**: Complete installation and usage guides

### Technical Details
- Uses port 443 (standard HTTPS) for communication
- Implements OpenSSL legacy renegotiation for compatibility
- curl subprocess calls for reliable SSL connections
- Home Assistant 2023.1.0+ compatibility
- Python 3.9+ support

### Documentation
- README.md with complete setup instructions
- INSTALLATION.md with step-by-step guide
- QUICK_REFERENCE.md for common operations
- API command reference in daikin_ac_commands.txt
- SSL fix documentation in daikin_ssl_fix_documentation.md

### Scripts
- test_connection_curl.py for connection testing
- setup_openssl_config.py for SSL configuration
- test_daikin_client_simple.py for client testing
