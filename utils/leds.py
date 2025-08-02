import subprocess
import json
import os
import logging
import configparser
import time
from dataclasses import dataclass, field

@dataclass
class LedController:
    config_path: str
    state_file: str = "/etc/enrg/utilitymanager/leds.init"
    logger: logging.Logger = None

    simple_leds: dict = field(init=False)
    state_led: dict = field(init=False)
    type_device: str = field(init=False)
    config: configparser.ConfigParser = field(init=False)
    max_brightness: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.simple_leds = {
            "Green_A": 0,
            "Green_B": 0,
            "Red_A": 0,
            "Red_B": 0,
        }

        self.state_led = {
            "PowerLED_Blue": {"trigger": "none", "brightness": 0},
            "PowerLED_Amber": {"trigger": "none", "brightness": 0}
        }

        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self._set_startup_variables()
        self._load_state()
        self._load_max_brightness()

    def _set_startup_variables(self):
        self.type_device = self.config.get("functioning", "type_device", fallback="IOT-GATE-iMX8")

    def _get_max_brightness(self, led):
        path = f"/sys/class/leds/{led}/max_brightness"
        try:
            with open(path, "r") as f:
                return int(f.read().strip())
        except Exception as e:
            self.logger.error(f"[Led] --> Could not read max_brightness for {led}: {e}")
            return 1

    def _load_max_brightness(self):
        if self.type_device != "IOT-GATE-iMX8":
            for led in list(self.simple_leds.keys()) + list(self.state_led.keys()):
                self.max_brightness[led] = self._get_max_brightness(led)

    def _write_sysfs(self, path, value):
        if self.type_device != "IOT-GATE-iMX8":
            try:
                subprocess.run(
                    ["sudo", "tee", path],
                    input=f"{value}\n".encode(),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                time.sleep(0.05)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"[Led] --> Could not write  {path} with sudo: {e}")

    def _save_state(self):
        if self.type_device != "IOT-GATE-iMX8":
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump({"simple_leds": self.simple_leds, "state_led": self.state_led}, f)

    def _load_state(self):
        if self.type_device != "IOT-GATE-iMX8" and os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                state = json.load(f)
                self.simple_leds = state.get("simple_leds", self.simple_leds)
                self.state_led = state.get("state_led", self.state_led)

    def set_simple_led(self, led, value):
        try:
            if self.type_device != "IOT-GATE-iMX8":
                if led not in self.simple_leds:
                    
                    self.logger.error(f"[Led] --> Unknow simple LED   : {led}")
                    return
                value = min(value, self.max_brightness.get(led, 1))
                if self.simple_leds[led] == value:
                    self.logger.debug(f"{led} It's already in that state {value},Nothing is being done.")
                    return
                self.logger.debug(f"Change {led} a status {value}")
                self._write_sysfs(f"/sys/class/leds/{led}/trigger", "none")
                self._write_sysfs(f"/sys/class/leds/{led}/brightness", value)
                self.simple_leds[led] = value
                self._save_state()
        except Exception as ex:
            self.logger.error(f"[Led] --> {ex}")

    def set_led_ab(self, led, value):
        path = f"/sys/class/leds/{led}/brightness"
       
        try:
            subprocess.run(
                ["sudo", "tee", path],
                input=f"{value}\n".encode(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.logger.error(f"[Led] -->  Error in {led}: {e}")

    def _disable_state_leds(self):
        for led in self.state_led:
            current = self.state_led[led]
            if current["trigger"] != "none" or current["brightness"] != 0:
                
                self.logger.debug(f"[Led] --> Turning off and deactivating {led}")
                self._write_sysfs(f"/sys/class/leds/{led}/trigger", "none")
                self._write_sysfs(f"/sys/class/leds/{led}/brightness", 0)
                self.state_led[led] = {"trigger": "none", "brightness": 0}
        self._save_state()

    def _turn_off_led(self, led_name):
        if led_name not in self.state_led:
            self.logger.error(f"[Led] --> Unknown status LED: {led_name}")
            return
        current = self.state_led[led_name]
        if current["brightness"] == 0 and current["trigger"] == "none":
            
            self.logger.debug(f"[Led] --> {led_name} It's already turned off.")
            return
        
        self.logger.debug(f"[Led] --> Turning off {led_name}")
        self._write_sysfs(f"/sys/class/leds/{led_name}/trigger", "none")
        self._write_sysfs(f"/sys/class/leds/{led_name}/brightness", 0)
        self.state_led[led_name] = {"trigger": "none", "brightness": 0}
        self._save_state()

    def set_state_led_blink(self, color):
        led_name = f"PowerLED_{color.capitalize()}"
        if led_name not in self.state_led:
            self.logger.error(f"[Led] --> Unknown status LED: {led_name}")
            return
        if self.state_led[led_name]["trigger"] == "heartbeat":
            self.logger.debug(f"[Led] --> {led_name} It's already flashing.")
            return
        self._disable_state_leds()
        self.logger.debug(f"[Led] --> Enabling blinking in {led_name}")
        self._write_sysfs(f"/sys/class/leds/{led_name}/trigger", "heartbeat")
        self.state_led[led_name] = {"trigger": "heartbeat", "brightness": 1}
        self._save_state()

    def set_state_led_fixed(self, color):
        led_name = f"PowerLED_{color.capitalize()}"
        if led_name not in self.state_led:
            self.logger.error(f"[Led] --> LED de estado desconocido: {led_name}")
            return
        if self.state_led[led_name]["trigger"] == "none" and self.state_led[led_name]["brightness"] == 1:
            self.logger.debug(f"[Led] --> {led_name} ya está encendido fijo.")
            return
        self._disable_state_leds()
        self.logger.debug(f"[Led] --> Activando luz fija en {led_name}")
        self._write_sysfs(f"/sys/class/leds/{led_name}/trigger", "none")
        self._write_sysfs(f"/sys/class/leds/{led_name}/brightness", 1)
        self.state_led[led_name] = {"trigger": "none", "brightness": 1}
        self._save_state()

    def set_state_leds_blink(self, blue=None, amber=None):
        leds_to_set = []
        if blue: leds_to_set.append("PowerLED_Blue")
        if amber: leds_to_set.append("PowerLED_Amber")

        if leds_to_set:
            self._disable_state_leds()

        for led in leds_to_set:
            self.logger.debug(f"[Led] --> Enabling blinking in {led}")
            self._write_sysfs(f"/sys/class/leds/{led}/trigger", "heartbeat")
            self.state_led[led] = {"trigger": "heartbeat", "brightness": 1}

        if blue is False:
            self._turn_off_led("PowerLED_Blue")
        if amber is False:
            self._turn_off_led("PowerLED_Amber")

        self._save_state()

    def set_state_leds_fixed(self, blue=None, amber=None):
        leds_to_set = []
        if blue: leds_to_set.append("PowerLED_Blue")
        if amber: leds_to_set.append("PowerLED_Amber")

        if leds_to_set:
            self._disable_state_leds()

        for led in leds_to_set:
            
            self._write_sysfs(f"/sys/class/leds/{led}/trigger", "none")
            self._write_sysfs(f"/sys/class/leds/{led}/brightness", 1)
            self.state_led[led] = {"trigger": "none", "brightness": 1}

        if blue is False:
            self._turn_off_led("PowerLED_Blue")
        if amber is False:
            self._turn_off_led("PowerLED_Amber")

        self._save_state()

    def turn_off_all_leds(self):
       
        for led in self.simple_leds:
            self._write_sysfs(f"/sys/class/leds/{led}/trigger", "none")
            self._write_sysfs(f"/sys/class/leds/{led}/brightness", 0)
            self.simple_leds[led] = 0
            time.sleep(0.05)

        for led in self.state_led:
            self._write_sysfs(f"/sys/class/leds/{led}/trigger", "none")
            self._write_sysfs(f"/sys/class/leds/{led}/brightness", 0)
            self.state_led[led] = {"trigger": "none", "brightness": 0}
            time.sleep(0.05)

        self._save_state()
        self.logger.debug("[Led] --> All LEDs have been turned off.")
