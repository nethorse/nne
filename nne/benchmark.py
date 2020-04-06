import time
import matplotlib.pyplot as plt

class Save:
    def __init__(self, name):
        self.ave = []
        self.min = []
        self.max = []
        self.name = name

class Benchmark:
    def __init__(self, counter=10, name='sample'):
        self.ave = []
        self.min = []
        self.max = []
        self.counter = counter
        self.saves = []

    def measure(self, func, name):
        save = Save(name)
        def inner(*args, **kwargs):
            durations = []
            for i in range(self.counter):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                durations.append((end - start) * 1000)
            ave = sum(durations) / self.counter
            min_value = min(durations)
            max_value = max(durations)
            save.ave.append(ave)
            save.min.append(min_value)
            save.max.append(max_value)
            print(f'{name},average[ms],{round(ave, 4)},min[ms],{round(min_value, 4)},max[ms],{round(max_value, 4)}')
            return func(*args, **kwargs)
        self.saves.append(save)
        return inner


class Plot:
    def __init__(self, benchmark):
        self.benchmark = benchmark

    def plot(self, x, xlabl, title, savefile):
        for save in self.benchmark.saves:
            plt.plot(x, save.ave, label=save.name)
        plt.title(title)
        plt.legend()
        plt.xlabel('batch size')
        plt.ylabel('inference time[ms]')
        plt.savefig(savefile)

def benchmark(func):
    counter = 100
    def inner(*args, **kwargs):
        durations = []
        for i in range(counter):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            durations.append((end - start) * 1000)
        durations.pop(0)
        ave = sum(durations) / counter
        min_value = min(durations)
        max_value = max(durations)
        print(f'average[ms],{round(ave, 4)},min[ms],{round(min_value, 4)},max[ms],{round(max_value, 4)}')
        return func(*args, **kwargs)
    return inner
