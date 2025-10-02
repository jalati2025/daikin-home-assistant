# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
