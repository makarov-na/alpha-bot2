from rpi_ws281x import Adafruit_NeoPixel, Color


class LedStrip:

    def __init__(self):
        # LED strip configuration:
        self._LED_COUNT = 4  # Number of LED pixels.
        self._LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
        self._LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self._LED_DMA = 5  # DMA channel to use for generating signal (try 5)
        self._LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        self._LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        self._LED_CHANNEL = 0
        self._strip = Adafruit_NeoPixel(self._LED_COUNT, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, self._LED_BRIGHTNESS)
        self._strip.begin()
        self.switchOffStrip()

    def setPixelColourRgb(self, position, red, green, blue):
        self._strip.setPixelColor(position, Color(red, green, blue))
        self._strip.show()

    def setStripBrightness(self, brightness):
        self._strip.setBrightness(brightness)

    def switchOffPixel(self, position):
        self._strip.setPixelColor(position, Color(0, 0, 0))
        self._strip.show()

    def switchOffStrip(self):
        for n in range(0, self._LED_COUNT):
            self._strip.setPixelColor(n, Color(0, 0, 0))
        self._strip.show()
