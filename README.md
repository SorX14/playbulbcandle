# playbulbcandle
Python library for communicating with PlayBulb Candles.

[PlayBulb](http://www.playbulb.com/en/index.html) Candles are RGBW Bluetooth 4.0 candles which are controlled with a iOS/Android app. 

## Installation

Tested working on Raspberry Pi 3 with Noobs.

Install bluetooth and bluez

    sudo apt-get install bluetooth bluez

Find your PlayBulb Candles

    sudo hcitool lescan

This will stream all found devices on the screen. Use `Ctrl+c` to break the process, copy the MAC addresses for use later

The library is based on `gatttool` which allows you to send messages via command line

    gatttool -b [mac address] --char-write-req -a [register] -n [value]
    gatttool -b [mac address] --char-write -a [register] -n [value]
    gatttool -b [mac address] --char-read -a [register]
    
Get the library

    pip install playbulbcandle
    
## Usage

Look in `tester.py` for a working example. More information can be found in this [blob post](https://stevep.xyz/2016/12/controlling-playbulb-candles-with-python/).

```python
  from playbulbcandle import PlayBulbCandle
  
  candle1 = PlayBulbCandle('AA:AA:AA:AA:AA:AA')
  candle2 = PlayBulbCandle('BB:BB:BB:BB:BB:BB')
  
  candle1.setColor(0, 255, 0, 0) # Set color to red
  candle1.setEffect(255, 0, 0, 0, 'candle', 0) # Candle flicker effect in white
  candle1.off() # There is no alternative for on
  
  print candle2.getBatteryLevel()
```  

## Troubleshooting

### Bluetooth dongle
You can check whether your bluetooth dongle is connected

    lsusb
    
On my system, I see with a dongle marked 'CSR 4.0' (cheap from ebay)

    $ lsusb
    Bus 001 Device 004: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp.
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

### Cannot connect

Make sure you're not already connected with the app. Only one device can connect to the bulb at once

## Acknowledgements
* http://colinkraft.com/candle/candle.php
* https://github.com/Phhere/Playbulb/blob/master/protocols/candle.md
