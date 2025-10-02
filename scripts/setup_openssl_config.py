#!/usr/bin/env python3
"""
Setup script for OpenSSL configuration.
This script creates the necessary OpenSSL configuration file for legacy renegotiation.
"""

import os
import sys
import argparse

def create_openssl_config(output_path="/tmp/openssl_legacy.conf"):
    """Create OpenSSL configuration file for legacy renegotiation."""
    config_content = """openssl_conf = openssl_init

[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
Options = UnsafeLegacyRenegotiation
"""
    
    try:
        with open(output_path, 'w') as f:
            f.write(config_content)
        
        print(f"✅ OpenSSL configuration created at: {output_path}")
        print("This configuration enables legacy SSL renegotiation for Daikin AC units.")
        print("\nTo use this configuration:")
        print(f"export OPENSSL_CONF={output_path}")
        print("curl --insecure -H \"X-Daikin-uuid: YOUR_UUID\" \"https://YOUR_IP/common/basic_info?key=YOUR_KEY\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create OpenSSL configuration: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create OpenSSL configuration for Daikin AC")
    parser.add_argument("--output", "-o", default="/tmp/openssl_legacy.conf", 
                       help="Output path for the configuration file (default: /tmp/openssl_legacy.conf)")
    
    args = parser.parse_args()
    
    success = create_openssl_config(args.output)
    
    if success:
        print("\n🎉 OpenSSL configuration setup complete!")
        sys.exit(0)
    else:
        print("\n💥 OpenSSL configuration setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
