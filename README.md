# AlphaBot2-Pi API 

Friendly API implementation for AlphaBot2-Pi KIT [(View on Youtube)](https://www.youtube.com/playlist?list=PLKxQTQ3TZlLE8VYpjXAgBHHr27JPiKOji)

* Camera position control
* Motors power control with frequency width modulation
* Line sensors analog to digital converter TLC1543 control
* Led strip WS2812B control
* Beeper control
* GPIO wrapper for PC environment development and unit testing

[![DeepWiki](https://img.shields.io/badge/DeepWiki-makarov--na%2Falpha--bot2-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==)](https://deepwiki.com/makarov-na/alpha-bot2)

# Usage

## Camera position control

```python

from alphabot.bot.hardware.camera_module import CameraServo

# angle from -45 to 45
vertical_angle = 0
horizontal_angle = 45
camera_servo = CameraServo()
camera_servo.setVerticalPosition(vertical_angle)
camera_servo.setHorizontalPosition(horizontal_angle)

```

## Truck control

```python

from alphabot.bot.truck_module import Truck

# power from -100 to 100
power = 50
truck = Truck(gpio)
truck.setSpeedPower(power)
truck.setTurnPower(0)
```

## Motor control

```python
from alphabot.bot.hardware.motor_module import LeftMotor, RightMotor

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
from alphabot.bot.hardware.line_sensor_module import LineSensorsAdc

sensors_adc = LineSensorsAdc(gpio)
all_sensors_values = sensors_adc.readSensors()
```

## Beeper

```python
from alphabot.bot.hardware.beeper_module import Beeper

beeper = Beeper(gpio)
beeper.beepOn()
beeper.beepOff()
```
or

```python
from alphabot.bot.hardware.beeper_module import Beeper

beeper = Beeper(gpio)
time_in_milliseconds = 1000
beeper.beepOn(time_in_milliseconds)
```

## Led strip

```python
from alphabot.bot.hardware import LedStrip

strip = LedStrip()
strip.setPixelColourRgb(0, 255, 0, 0)
```
