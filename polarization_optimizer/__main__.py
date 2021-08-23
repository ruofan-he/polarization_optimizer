from . import Random_Walk_Handler
from . import normal_metric_factory, visibility_metric_factory, max_min_difference_metric_factory, power_ratio_metric_factory
from . import write_channel_integer
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
def random_walk(method, channel1 , channel2, ground_level):
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
    while True:
        random_walk_handler.step()
        sleep(0.001)

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


