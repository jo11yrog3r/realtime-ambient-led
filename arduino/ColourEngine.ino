#include <FastLED.h>

#define LED_PIN     3       // This is the data pin used by the Arduino
#define NUM_LEDS    60
#define BRIGHTNESS  40      // Controls the brightness of the LEDs

CRGB leds[NUM_LEDS];

String input = "";
bool outputEnabled = false;

void setup() {
  Serial.begin(115200);

  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void loop() {
  while(Serial.available() > 0) {
    char c = Serial.read();

    if(c == '\n') {
      processLine(input);
      input = "";
    } else {
      input += c;
    }
  }
}

void processLine(String line) {
  if (line == "ON") {
    outputEnabled = true;
    flashSignal(CRGB::Green, 2, 500);
    return;
  }

  if (line == "OFF") {
    outputEnabled = false;
    flashSignal(CRGB::Red, 2, 500);
    return;
  }

  if (!outputEnabled) {
    return;
  }

  int r, g, b;
  if (sscanf(line.c_str(), "%d,%d,%d", &r, &g, &b) == 3) {
    r = constrain(r, 0, 255);
    g = constrain(g, 0, 255);
    b = constrain(b, 0, 255);

    fill_solid(leds, NUM_LEDS, CRGB(r, g, b));
    FastLED.show();
  }
}

void flashSignal(CRGB colour, int flashes, int totalDurationMs) {
  int intervals = flashes * 2;
  int timeDelay = totalDurationMs / intervals;

  for (int i = 0; i < flashes; i++) {
    FastLED.setBrightness(5);
    fill_solid(leds, NUM_LEDS, colour);
    FastLED.show();
    delay(timeDelay);

    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
    delay(timeDelay);
  }

  FastLED.setBrightness(BRIGHTNESS);
}
