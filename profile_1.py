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
            # if db.checkName(name) == ():
            #     del string, db
            #     return name

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
        agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36']
        agent = random.choice(agents)
        del agents
        return agent

    def make(self):
        profile = {'name': self.name(),
                   'user_agent': self.userAgent(),
                   'screenResolution': self.screens(),
                   'platform': 'Win32',
                   'deviceMemory': self.hardware(),
                   'hardwareConcurrency': self.hardware(),
                   'webGLHash': self.webGLHash(),
                   'webGLVendor': self.webGLVendor(),
                   'CanvasHash': self.canvasHashGenerator()
                   }

        return profile
