import re
import click

from functools import reduce
from operator import mul


@click.group(help="Advent of code day 3")
def cli():
    pass


@cli.command(help="Day 3 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day3_part1(ctx, input):
    p = re.compile(r"(?P<number>\d+)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    non_matchings = []

    for i in range(number_of_lines):
        # [:-1] to remove the trailing '\n'
        previous = lines[i - 1][:-1] if i - 1 >= 0 else "." * line_length
        current = lines[i][:-1]
        next = lines[i + 1][:-1] if i + 1 < number_of_lines else "." * line_length

        non_matching = []

        for finding in p.finditer(current):
            value = int(finding.group("number"))
            found_symbol = False
            start, end = finding.span()
            if (
                start > 0
                and current[start - 1] != "."
                or end < len(current)
                and current[end] != "."
            ):
                found_symbol = True
            elif search_symbol_on_line(previous, start, end) or search_symbol_on_line(
                next, start, end
            ):
                found_symbol = True
            else:
                non_matching.append((start, end))

            sum += value if found_symbol else 0

        non_matchings.append(non_matching)

    for i in range(number_of_lines):
        line_matches = non_matchings[i]
        for j, c in enumerate(lines[i]):
            if color := colorize(j, line_matches):
                click.secho(c, fg=color, nl=False)
            else:
                click.echo(c, nl=False)

    click.secho(f"Engine parts sum: {sum}", fg="green")


def search_symbol_on_line(line, start, end):
    if not line:
        return False
    p = re.compile(r"(?!\.|\d|$)")
    return p.search(line[start - 1 : end + 1]) != None


def colorize(i, current):
    for start, end in current:
        if i >= start - 1 and i <= end:
            return "red"
    return False


@cli.command(help="Day 3 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day3_part2(ctx, input):
    p = re.compile(r"(\*)")
    n = re.compile(r"(?P<number>\d+)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    matching_lines = []
    non_matching_lines = []

    for i in range(number_of_lines):
        # [:-1] to remove the trailing '\n'
        previous = lines[i - 1][:-1] if i - 1 >= 0 else "." * line_length
        current = lines[i][:-1]
        next = lines[i + 1][:-1] if i + 1 < number_of_lines else "." * line_length
        matchings = []
        non_matchings = []

        for finding in p.finditer(current):
            values = []
            star = finding.start()
            for m in n.finditer(previous):
                start, end = m.span()
                if start <= star + 1 and star <= end:
                    values.append(int(m.group()))
            for m in n.finditer(next):
                start, end = m.span()
                if start <= star + 1 and star <= end:
                    values.append(int(m.group()))
            for m in n.finditer(current):
                start, end = m.span()
                if start == star + 1 or end == star:
                    values.append(int(m.group()))

            if len(values) > 2:
                click.echo("more than 2 items")
            elif len(values) == 2:
                sum += reduce(mul, values)
                matchings.append(star)
            else:
                non_matchings.append(star)

        matching_lines.append(matchings)
        non_matching_lines.append(non_matchings)

    if ctx.obj["DEBUG"]:
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if j in matching_lines[i]:
                    click.secho(c, fg="yellow", nl=False)
                elif j in non_matching_lines[i]:
                    click.secho(c, fg="red", nl=False)
                else:
                    click.echo(c, nl=False)

    click.secho(f"Gear ratio: {sum}", fg="green")
