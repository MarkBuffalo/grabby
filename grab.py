import requests
from bs4 import BeautifulSoup
import sched
import time
import webbrowser
from playsound import playsound


class GrabBagGrabber:
    def __init__(self):
        self.request = None
        # Every X seconds. In this case, 15.
        self.interval = 15
        # The sound file to play.
        self.sound_file = "wake_up.wav"
        # The base rogue fitness url.
        self.base_url = "https://www.roguefitness.com/miscellaneous-barbells-used"
        pass

    def start(self, scheduler):
        # Don't follow redirects. This gets us the true status code.
        self.request = requests.get(self.base_url, allow_redirects=False)
        # This page is up! That means the used bars are available. Let's print.
        if self.request.status_code == 200:
            self.print_availability()
        # This is 301 or something else. There are no grab bag bars available.
        else:
            print("Not in stock")
        # Repeat this same function every X seconds.
        s.enter(self.interval, 1, self.start, (scheduler,))

    def print_availability(self):
        soup = BeautifulSoup(self.request.text)
        found_something = False

        # We're going to trawl through the options and ignore everything that isn't a product.
        for i in soup.findAll("option"):
            if "Choose a Selection" not in i.text:
                if "Out of stock" not in i.text:
                    print(f"In stock: {i.text.strip()}")
                    found_something = True
                else:
                    print(f"Out of stock: {i.text.strip().replace('(Out of stock)', '')}")
        # These are try/catch exceptions for all you folks on your failed pixel books
        # and other crap default python installs that don't work.
        if found_something:
            try:
                webbrowser.open(self.base_url)
            except Exception:
                print("Couldn't open web browser. This is all your fault")
            try:
                playsound(self.sound_file)
            except Exception as e:
                print("Couldn't play alarm. This is all your fault.")


if __name__ == "__main__":
    gb = GrabBagGrabber()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, gb.start, (s,))
    s.run()
