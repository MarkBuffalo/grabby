import requests
from bs4 import BeautifulSoup
import sched
import time
import webbrowser
from playsound import playsound


class Grabby:
    def __init__(self):
        self.request = None
        # Every X seconds. In this case, 15.
        self.interval = 30
        # The sound file to play.
        self.sound_file = "wake_up.wav"
        # The base rogue fitness url.
        self.product_list = "products.txt"
        self.product_urls = []
        self.soup = None
        self.opened_urls = []
        self.opened_items = []
        pass

    def start(self, scheduler):
        # Don't follow redirects. This gets us the true status code.
        with open(self.product_list, "r") as f:
            self.product_urls = f.read().splitlines()

        for url in self.product_urls:
            self.request = requests.get(url, allow_redirects=False)
            # This page is up! That means the used bars are available. Let's print.
            if self.request.status_code == 200:
                # This one is for grab bags / available options.
                self.print_availability(url)
                # This one is for everything else.
                self.check_other_quantity(url)
            # This is 301 or something else. There are no grab bag bars available.
            else:
                pass
                #print("Not in stock")
            # Repeat this same function every X seconds.
            s.enter(self.interval, 1, self.start, (scheduler,))

    def print_availability(self, url):
        self.soup = BeautifulSoup(self.request.text, "html.parser")
        #print(f"Checking {url}")
        found_something = False
        new_item = None

        # We're going to trawl through the options and ignore everything that isn't a product.
        for i in self.soup.findAll("option"):
            new_item = i.text.strip()
            if "Choose a Selection" not in new_item:
                if "Out of stock" not in new_item:
                    found_something = True
                else:
                    pass
                    #print(f"Out of stock: {i.text.strip().replace('(Out of stock)', '')}")
        # These are try/catch exceptions for all you folks on your failed pixel books
        # and other crap default python installs that don't work.
        if found_something:
            self.announce(url, new_item)
            self.update_urls(url)
            self.update_items(new_item)

    def check_other_quantity(self, url):
        item = self.soup.findAll("div", {"class": "grouped-item"})[2].findAll("div", {"class", "item-name"})[0].text
        quantity = self.soup.findAll("div", {"class": "grouped-item"})[2].findAll("div", {"class", "item-qty"})

        if len(quantity) > 0:
            self.announce(url, item)
            self.update_urls(url)
            self.update_items(item)

    def update_urls(self, url):
        if not self.item_used(url, self.opened_urls):
            self.opened_urls.append(url)

    def update_items(self, item):
        if not self.item_used(item, self.opened_items):
            print(f"In stock: {item}")
            self.opened_items.append(item)

    @staticmethod
    def item_used(item, list_obj):
        for new_item in list_obj:
            if item == new_item:
                return True
        return False

    def announce(self, url, item):
        # We haven't already opened this browser. Let's do it
        if not self.item_used(url, self.opened_urls):
            self.play_sound(url)
        # We already opened the browser...
        else:
            # No need to open it again unless a new item comes in stock...
            if not self.item_used(item, self.opened_items):
                self.play_sound(url)

    def play_sound(self, url):
        try:
            webbrowser.open(url)
        except Exception:
            print("Couldn't open web browser. This is all your fault")
        try:
            playsound(self.sound_file)
        except Exception:
            print("Couldn't play alarm. This is all your fault.")


if __name__ == "__main__":
    gb = Grabby()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, gb.start, (s,))
    s.run()
