import re
import click

from functools import reduce
from operator import mul


@click.group(help="Advent of code day 8")
def cli():
    pass


@cli.command(help="Day 8 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day8_part1(ctx, input):
    p = re.compile(r"(?P<position>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)

    moves = [c for c in lines[0]][:-1]
    if ctx.obj["DEBUG"]:
        click.echo(f"Moves: {moves}")

    map = {}
    for i in range(2, number_of_lines):
        m = p.match(lines[i])
        position = m.group("position")
        left = m.group("left")
        right = m.group("right")
        map[position] = (left, right)

    if ctx.obj["DEBUG"]:
        click.echo(map)

    pos = "AAA"
    while True:
        direction = moves[sum % len(moves)]
        sum += 1
        if ctx.obj["DEBUG"]:
            click.echo(f"{sum}: {pos} -{direction}> ", nl=False)

        pos = map.get(pos)[0 if direction == "L" else 1]

        if ctx.obj["DEBUG"]:
            click.echo(f"{pos}")

        if pos == "ZZZ":
            break

    click.secho(f"Number of moves: {sum}", fg="green")


@cli.command(help="Day 8 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day8_part2(ctx, input):
    p = re.compile(r"(?P<position>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)

    moves = [0 if c == "L" else 1 for c in lines[0]][:-1]
    # if ctx.obj["DEBUG"]:
    #     click.echo(f"Moves: {moves}")

    map = {}
    positions = []
    for i in range(2, number_of_lines):
        m = p.match(lines[i])
        position = m.group("position")
        left = m.group("left")
        right = m.group("right")
        map[position] = (left, right)
        if position.endswith("A"):
            positions.append(position)

    if ctx.obj["DEBUG"]:
        # click.echo(map)
        click.echo(f"{len(positions)} positions to navigate in parallel: {positions}")

    loops = []
    for i in range(len(positions)):
        count = 0
        mod = -1
        start = positions[i]
        next = start

        if ctx.obj["DEBUG"]:
            click.echo(f"{start} -> ", nl=False)

        while start != next or count == 0:
            direction = moves[count % len(moves)]
            count += 1
            next = map.get(next)[direction]

            mod = count % len(moves)

            if next[2] == "Z" and mod == 0:
                loop = int(count / len(moves))
                loops.append(loop)
                if ctx.obj["DEBUG"]:
                    click.echo(f"{next} in {count}, {loop} iter of the moves list")
                break

    if ctx.obj["DEBUG"]:
        click.echo(f"{loops}")

    sum = reduce(mul, loops)

    click.secho(f"Number of moves: {sum * 269}", fg="green")
