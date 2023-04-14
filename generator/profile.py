import random
from pathlib import Path


class ProfileGenerator:
    __base_dir = Path(__file__).resolve().parent.parent

    @staticmethod
    def canvasHashGenerator():
        hash = {"r": random.randint(-100, 100), "g": random.randint(-100, 100),
                "b": random.randint(-100, 100), "a": random.randint(-100, 100)}
        return hash

    @staticmethod
    def webGLHash():
        return random.uniform(0.9, 0)

    @staticmethod
    def name():
        # db = DataBase()
        string = 'qwertyuiopasdfghjklzxcvbnm'
        name = ''
        while True:
            for _ in range(15):
                name += random.choice(string)
            return name


    @staticmethod
    def hardware():
        setNumbers = [number for number in range(2, 32, 2)]
        number = random.choice(setNumbers)
        del setNumbers
        return number

    def webGLVendor(self):
        with open(f'{self.__base_dir}/generator/data/gpu.txt', 'r') as file:
            values = file.read().split('\n')
        return random.choice(values)

    def screens(self):
        with open(f'{self.__base_dir}/generator/data/screens.txt', 'r') as file:
            values = file.read().split('\n')
        return random.choice(values)

    @staticmethod
    def userAgent():
        agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.38 Safari/532.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.221.7 Safari/532.2',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13']
        agent = random.choice(agents)
        del agents
        return agent

    def make(self, server):
        profile = {'name': self.name(),
                   'user_agent': self.userAgent(),
                   'screenResolution': self.screens(),
                   'platform': 'Win32',
                   'deviceMemory': self.hardware(),
                   'hardwareConcurrency': self.hardware(),
                   'webGLHash': self.webGLHash(),
                   'webGLVendor': self.webGLVendor(),
                   'CanvasHash': self.canvasHashGenerator(),
                   'server': server}
        return profile
