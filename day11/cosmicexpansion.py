import re
import click


@click.group(help="Advent of code day 11")
def cli():
    pass


@cli.command(help="Day 11 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day11_part1(ctx, input):
    total = compute_galaxy_distance(ctx, input, 1)
    click.secho(f"Sum of minimal distances: {total}", fg="green")


@cli.command(help="Day 11 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day11_part2(ctx, input):
    total = compute_galaxy_distance(ctx, input, 999999)
    click.secho(f"Sum of minimal distances: {total}", fg="green")


def compute_galaxy_distance(ctx, input, extra_columns):
    p = re.compile(r"(#)")
    lines = input.readlines()

    rows = set()
    columns = set()
    galaxies = []
    for i, line in enumerate(lines):
        for m in p.finditer(line):
            rows.add(i)
            columns.add(m.span()[0])
            galaxies.append((i, m.span()[0]))

    if ctx.obj["DEBUG"]:
        click.echo(f"Galaxies: {galaxies}")

    total = 0
    for i in range(len(galaxies)):
        distances = []
        for j in range(i + 1, len(galaxies)):
            distance = abs(galaxies[i][0] - galaxies[j][0]) + abs(
                galaxies[i][1] - galaxies[j][1]
            )
            distance += sum(
                [
                    extra_columns
                    for x in range(
                        min(galaxies[i][0], galaxies[j][0]) + 1,
                        max(galaxies[i][0], galaxies[j][0]),
                    )
                    if x not in rows
                ]
            )
            distance += sum(
                [
                    extra_columns
                    for x in range(
                        min(galaxies[i][1], galaxies[j][1]) + 1,
                        max(galaxies[i][1], galaxies[j][1]),
                    )
                    if x not in columns
                ]
            )
            distances.append(distance)

        if distances:
            total += sum(distances)

    return total
