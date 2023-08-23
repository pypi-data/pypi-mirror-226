from enum import Enum, auto


class Operate(Enum):
    ABORT_NODE = auto()
    ABORT_PRE_PROCESSES = auto()


class ChainContext(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = []

    @property
    def result(self):
        try:
            return self.results[-1]
        except IndexError:
            return None

    @result.setter
    def result(self, new_result):
        self.results.append(new_result)

    def __repr__(self):
        return repr(self.result)
