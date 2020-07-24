import requests
from bs4 import BeautifulSoup
import sched
import time
import webbrowser
import simpleaudio as sa


class GrabBagGrabber:
    def __init__(self):
        self.request = None
        self.interval = 15
        self.sound_file = "wake_up.wav"
        self.base_url = "https://www.roguefitness.com/miscellaneous-barbells-used"
        pass

    def start(self, scheduler):
        self.request = requests.get(self.base_url, allow_redirects=False)
        if self.request.status_code == 200:
            self.print_availability()
        else:
            print("Not in stock")
        s.enter(self.interval, 1, self.start, (scheduler,))

    def print_availability(self):
        soup = BeautifulSoup(self.request.text)
        found_something = False
        for i in soup.findAll("option"):
            if "Choose a Selection" not in i.text:
                if "Out of stock" not in i.text:
                    print(f"In stock: {i.text.strip()}")
                    found_something = True
                else:
                    print(f"Out of stock: {i.text.strip().replace('(Out of stock)', '')}")
        if found_something:
            try:
                webbrowser.open(self.base_url)
            except Exception:
                print("Couldn't open web browser. This is all your fault")
            try:
                wave_obj = sa.WaveObject.from_wave_file(self.sound_file)
                play_obj = wave_obj.play()
            except Exception as e:
                print("Couldn't play alarm. This is all your fault.")


if __name__ == "__main__":
    gb = GrabBagGrabber()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, gb.start, (s,))
    s.run()
