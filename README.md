# AlphaBot2-Pi API

Friendly API implementation for AlphaBot2-Pi KIT  

* Motors power control with frequency width modulation
* Line sensors analog to digital converter TLC1543 control
* Led strip WS2812B control
* Beeper control
* GPIO wrapper for PC environment development and unit testing

# Usage

## Truck control

```python

from alphabot.truck.truck_module import Truck

# power from -100 to 100
power = 50
truck = Truck(gpio)
truck.setSpeedPower(power)
truck.setTurnPower(0)
```

## Motor control

```python
from alphabot.truck.hardware.motor_module import LeftMotor, RightMotor

# power from 0 to 100
power = 50
left_motor = LeftMotor(gpio)
right_motor = RightMotor(gpio)
left_motor.forward(power)
right_motor.forward(power)
# ..some logic
left_motor.stop()
right_motor.stop()
```

## Sensors

```python
from alphabot.truck.hardware.line_sensor_module import LineSensorsAdc

sensors_adc = LineSensorsAdc(gpio)
all_sensors_values = sensors_adc.readSensors()
```

## Beeper

```python
from alphabot.truck.hardware.beeper_module import Beeper

beeper = Beeper(gpio)
beeper.beepOn()
beeper.beepOff()
```
or

```python
from alphabot.truck.hardware.beeper_module import Beeper

beeper = Beeper(gpio)
time_in_milliseconds = 1000
beeper.beepOn(time_in_milliseconds)
```

## Led strip

```python
from alphabot.truck.hardware import LedStrip

strip = LedStrip()
strip.setPixelColourRgb(0, 255, 0, 0)
```
