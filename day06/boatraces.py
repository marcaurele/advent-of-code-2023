import re
import click


from functools import reduce
from operator import mul


@click.group(help="Advent of code day 6")
def cli():
    pass


@cli.command(help="Day 6 - part 1")
@click.pass_context
# @click.argument("input", type=click.File("r"))
def day6_part1(ctx):
    # times = [7, 15, 30]
    # distances = [9, 40, 200]

    times = [40, 82, 84, 92]
    distances = [233, 1011, 1110, 1487]

    winnings = []

    for i, time in enumerate(times):
        winning = []
        for t in range(1, time + 1):
            if (time - t) * t > distances[i]:
                winning.append(t)
        if ctx.obj["DEBUG"]:
            click.echo(f"For distance={distances[i]}: {winning}")
        winnings.append(len(winning))

    multi = reduce(mul, winnings)

    click.secho(f"Winning: {winnings} -> {multi}", fg="green")


@cli.command(help="Day 6 - part 2")
@click.pass_context
def day6_part2(ctx):
    # time = 71530
    # distance = 940200

    time = 40828492
    distance = 233101111101487

    winning = []
    winning = [t for t in range(1, time + 1) if (time - t) * t > distance]

    if ctx.obj["DEBUG"]:
        click.echo(f"For distance={distance}: {winning}")

    click.secho(f"Winning -> {len(winning)}", fg="green")
