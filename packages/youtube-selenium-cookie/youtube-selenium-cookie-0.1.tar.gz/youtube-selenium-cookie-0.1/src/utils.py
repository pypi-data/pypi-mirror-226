import sys, random, time

class Utils:
    @staticmethod
    def console_loader(_progress):
        total = 100
        progress = _progress / total
        sys.stdout.write("\r[{:<50}] {:.1f}%".format("=" * int(progress * 50), progress * 100))
        sys.stdout.flush()
        
    @staticmethod
    def small_wait():
        time.sleep(random.randrange(1, 7))
        
    @staticmethod
    def big_wait():
        time.sleep(random.randrange(15, 30))