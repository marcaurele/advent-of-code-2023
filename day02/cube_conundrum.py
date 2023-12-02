import re
import click

from functools import reduce
from operator import mul

CUBES = {
    "blue": 14,
    "green": 13,
    "red": 12,
}


@click.group(help="Advent of code day 2")
def cli():
    pass


@cli.command(help="Day 2 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day2_part1(ctx, input):
    p = re.compile(r"Game (?P<game>\d+): (?P<revealed>.*)")
    sum = 0
    for line in input.readlines():
        m = p.match(line)
        if ctx.obj["DEBUG"]:
            click.echo(line[:-1], nl=False)
            # click.echo(f"\n-> {m.group('game')}")
            # click.echo(f"--> {m.group('revealed')}")
        hands = m.group("revealed").split(";")
        sum += int(m.group("game")) if is_valid_game(ctx, hands) else 0

    click.secho(f"Puzzle: {sum}", fg="green")


def is_valid_game(ctx, hands):
    q = re.compile(r"(?P<count>\d+) (?P<color>blue|green|red)")
    for hand in hands:
        for match in q.finditer(hand):
            # if ctx.obj["DEBUG"]:
            #     click.echo(f"{match.group('color')}={match.group('count')}")
            if int(match.group("count")) > CUBES.get(match.group("color")):
                return False
    if ctx.obj["DEBUG"]:
        click.secho(" => Valid game", fg="blue")
    return True


@cli.command(help="Day 2 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day2_part2(ctx, input):
    p = re.compile(r"Game (?P<game>\d+): (?P<revealed>.*)")
    sum = 0
    for line in input.readlines():
        m = p.match(line)
        if ctx.obj["DEBUG"]:
            click.echo(line[:-1], nl=False)
        hands = m.group("revealed").split(";")
        sum += reduce(mul, minimal_set(ctx, hands))

    click.secho(f"Sum of power: {sum}", fg="green")


def minimal_set(ctx, hands):
    q = re.compile(r"(?P<count>\d+) (?P<color>blue|green|red)")
    min_cubes = {"blue": 0, "green": 0, "red": 0}
    for hand in hands:
        for match in q.finditer(hand):
            # if ctx.obj["DEBUG"]:
            #     click.echo(f"{match.group('color')}={match.group('count')}")
            count = int(match.group("count"))
            color = match.group("color")
            if count > min_cubes[color]:
                min_cubes[color] = count
    if ctx.obj["DEBUG"]:
        click.secho(f" => {min_cubes}", fg="blue")
    return min_cubes.values()
