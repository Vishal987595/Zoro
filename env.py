
from typing import List

class Environment:
    envs: List

    def __init__(self):
        self.envs = [{}]

    def enter_scope(self):
        self.envs.append({})

    def exit_scope(self):
        assert self.envs
        self.envs.pop()

    # def add(self, name, value):
    #     assert name not in self.envs[-1]
    #     self.envs[-1][name] = value

    def add(self, name, value, dtype = None):
        assert name not in self.envs[-1]
        self.envs[-1][name] = [value, dtype]

    def get(self, name):
        for env in reversed(self.envs):
            if name in env:
                return env[name]
        raise KeyError()

    def update(self, name, value):
        for env in reversed(self.envs):
            if name in env:
                env[name][0] = value
                return
        raise KeyError()
    
    def find(self, name):
        for env in reversed(self.envs):
            if name in env:
                return True
        return False