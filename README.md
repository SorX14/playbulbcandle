# PlayBulbCandle
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

## Usage

```python
  import playbulbcandle
  
  var candle1 = PlayBulbCandle('AA:AA:AA:AA:AA:AA')
  var candle2 = PlayBulbCandle('BB:BB:BB:BB:BB:BB')
  
  candle1.setColor(0, 255, 0, 0) # Set color to red
  candle1.setEffect(255, 0, 0, 0, 'candle', 0) # Candle flicker effect in white
  candle1.off() # There is no alternative for on
  
  print candle2.getBatteryLevel()
```  

## Acknowledgements
* http://colinkraft.com/candle/candle.php
* https://github.com/Phhere/Playbulb/blob/master/protocols/candle.md
