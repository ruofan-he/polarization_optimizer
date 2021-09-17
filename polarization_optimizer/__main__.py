from . import Random_Walk_Handler
from . import normal_metric_factory, visibility_metric_factory, max_min_difference_metric_factory, power_ratio_metric_factory
from . import write_channel_integer
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import click

"""
cmd
|
|-metric
|   |
|   |-normal
|   |-visibility
|   |-power_ratio
|   |-max_min_diff
|
|-random_walk [normal, visibility, power_ratio, max_min_diff]
|   

"""

@click.group()
def cmd():
    pass


metric_group    = cmd.group('metric')(lambda: None)
@metric_group.command('normal')
@click.option('-c', '--channel', type=int, default=1)
def metric_normal(channel):
    func = normal_metric_factory(channel)
    for i in range(10):
        print(func())
        sleep(0.5)
        

@metric_group.command('visibility')
@click.option('-c', '--channel', type=int, default=1)
@click.option('-g', '--ground_level', type=float, default=0)
def metric_visibility(channel, ground_level):
    func = visibility_metric_factory(channel, ground_level=ground_level)
    for i in range(10):
        print(func())
        sleep(0.5)

@metric_group.command('power_ratio')
@click.option('-p', '--primary', type=int, default=1)
@click.option('-s', '--secondary', type=int, default=2)
def metric_power_ratio(primary, secondary):
    func = power_ratio_metric_factory(primary, secondary)
    for i in range(10):
        print(func())
        sleep(0.5)

@metric_group.command('max_min_diff')
@click.option('-ch', '--channel', type=int, default=1)
def metric_max_min_diff(channel):
    func = max_min_difference_metric_factory(channel)
    for i in range(10):
        print(func())
        sleep(0.5)


@cmd.command('random_walk')
@click.argument('method')
@click.option('-c1', '--channel1', type=int, default=1)
@click.option('-c2', '--channel2', type=int, default=2)
@click.option('-g', '--ground_level', type=float, default=0)
@click.option('-i','--interactive', is_flag=True, default=False)
def random_walk(method, channel1 , channel2, ground_level, interactive):
    assert method in ['normal', 'visibility', 'power_ratio', 'max_min_diff']
    func = None
    if method == 'normal':
        assert channel1 is not None
        func = normal_metric_factory(channel1)
    elif method == 'visibility':
        assert channel1 is not None
        func = visibility_metric_factory(channel1, ground_level=ground_level) if ground_level is not None\
            else visibility_metric_factory(channel1)
    elif method == 'power_ratio':
        assert channel1 is not None
        assert channel2 is not None
        func = power_ratio_metric_factory(channel1, channel2)
    elif method == 'max_min_diff':
        assert channel1 is not None
        func = max_min_difference_metric_factory(channel1)
    else:
        return
    
    random_walk_handler = Random_Walk_Handler(metric=func)
    
    if interactive:
        with thread_handler(random_walk_handler) as th:
            thread = th.start()
            while not thread.done():
                order = input()
                if order == 'start':
                    th.start()
                if order == 'stop':
                    th.end()
                if order == 'exit':
                    th.end()
                    break
            thread.result() #waiting thread end, this is blocking
            print(f'error: {thread.exception()}')
    else:
        while True:
            random_walk_handler.step()
            sleep(0.001)


class thread_handler:
    def __init__(self, random_walk_handler):
        self.random_walk_handler = random_walk_handler
        self.thread = None
        self.thread_running = False
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='threading')
    def start(self):
        if not self.thread_running:
            self.thread_running = True
            self.thread = self.executor.submit(self.thread_func)
        return self.thread
    def end(self):
        self.thread_running = False
    def thread_func(self):
        while self.thread_running:
            self.random_walk_handler.step()
            sleep(0.001)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print('--error---------------------')
            print(exc_type, exc_value, traceback)
            print('--error---------------------')
        self.end()
        self.executor.shutdown(wait=False, cancel_futures=True)
    def __del__(self):
        self.end()
        self.executor.shutdown(wait=False, cancel_futures=True)



@cmd.command('direct')
def direct_write_integer():
    while True:
        order = input()
        if 'exit' in order:
            return
        integers = list(map(int,order.split(' ')))
        assert len(integers) == 3
        for ch, value in enumerate(integers):
            write_channel_integer(ch, value)


if __name__ == '__main__':
    cmd()


