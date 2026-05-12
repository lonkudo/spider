from internet_now import is_time_hit
from vivo_spider import vivo_spider
from time import sleep

while not is_time_hit("9:59:59"):
    sleep(0.1)

vivo_spider()

