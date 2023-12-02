import re
import click

SWITCH = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


@click.group(help="Advent of code day 1")
def cli():
    pass


@cli.command(help="Day 1 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day1_part1(ctx, input):
    p = re.compile(r"(\d)")
    sum = 0
    for line in input.readlines():
        try:
            if ctx.obj["DEBUG"]:
                click.echo(line[:-1], nl=False)
            m = p.findall(line)
            if len(m) == 0:
                continue
            else:
                sum += int(f"{m[0]}{m[-1]}")
                val = int(f"{m[0]}{m[-1]}")
            if ctx.obj["DEBUG"]:
                click.echo(f" -> {m} -> {val} -> {sum}")
        except ValueError:
            click.echo("Invalid number", err=True, fg="red")
    click.secho(f"Calibration value: {sum}", fg="green")


@cli.command(help="Day 1 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day1_part2(ctx, input):
    p = re.compile("r(\d|one|two|three|four|five|six|seven|eight|nine)")
    sum = 0
    for line in input.readlines():
        try:
            if ctx.obj["DEBUG"]:
                click.echo(line[:-1], nl=False)
            m1 = p.search(line)
            for i in range(1, len(line) + 1):
                m2 = p.search(line[i * -1 :])
                if m2:
                    break

            sum += SWITCH.get(m1.group(0)) * 10 + SWITCH.get(m2.group(0))
            if ctx.obj["DEBUG"]:
                click.echo(f" -> {m1.group(0)}{m2.group(0)} -> {sum}")
        except ValueError:
            click.echo("Invalid number", err=True, fg="red")
    click.secho(f"Calibration value: {sum}", fg="green")
