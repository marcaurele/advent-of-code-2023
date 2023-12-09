import re
import click

from functools import reduce
from operator import mul


@click.group(help="Advent of code day 9")
def cli():
    pass


@cli.command(help="Day 9 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day9_part1(ctx, input):
    p = re.compile(r"(-?\d+)")
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    total = 0

    for line in lines:
        levels = []
        numbers = [int(t) for t in p.findall(line)]
        levels.append(numbers)
        count = sum(numbers)
        i = 0
        while count != 0:
            numbers = [
                levels[i][a] - levels[i][a - 1] for a in range(1, len(levels[i]))
            ]
            levels.append(numbers)
            count = sum(numbers)
            i += 1

        num = 0
        for l in reversed(levels):
            num += l[-1]
            l.append(num)

        total += levels[0][-1]

        if ctx.obj["DEBUG"]:
            for i, l in enumerate(levels):
                for j, ll in enumerate(l):
                    if i == 0 and j == len(l) - 1:
                        click.secho(f"{ll}", fg="blue", nl=False)
                    elif j == len(l) - 1:
                        click.secho(f"{ll}", fg="red", nl=False)
                    else:
                        click.echo(f"{ll} ", nl=False)
                click.echo("")
            click.echo("-" * 50)

    click.secho(f"Total: {total}", fg="green")


@cli.command(help="Day 9 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day9_part2(ctx, input):
    p = re.compile(r"(-?\d+)")
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    total = 0

    for line in lines:
        levels = []
        numbers = [int(t) for t in p.findall(line)]
        levels.append(numbers)
        count = sum(numbers)
        i = 0
        while count != 0:
            numbers = [
                levels[i][a] - levels[i][a - 1] for a in range(1, len(levels[i]))
            ]
            levels.append(numbers)
            count = sum(numbers)
            i += 1

        num = 0
        for l in reversed(levels):
            num = l[0] - num
            l.insert(0, num)

        total += levels[0][0]

        if ctx.obj["DEBUG"]:
            for i, l in enumerate(levels):
                for j, ll in enumerate(l):
                    if i == 0 and j == 0:
                        click.secho(f"{ll}", fg="blue", nl=False)
                    elif j == 0:
                        click.secho(f"{ll}", fg="red", nl=False)
                    else:
                        click.echo(f" {ll}", nl=False)
                click.echo("")
            click.echo("-" * 50)

    click.secho(f"Total: {total}", fg="green")
