#!/usr/bin/env python3
"""
Test script for the updated DaikinClient class.
"""

import sys
import os

# Add the custom_components directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'custom_components'))

from daikin_local.daikin_client import DaikinClient

def test_client():
    """Test the DaikinClient class."""
    print("Testing DaikinClient...")
    
    # Create client
    client = DaikinClient(
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
