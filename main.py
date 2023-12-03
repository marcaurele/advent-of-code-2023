#!/bin/python3
import click

from day01 import trebuchet as day1
from day02 import cube_conundrum as day2
from day03 import gear_ratios as day3


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


cli.add_command(day1.day1_part1)
cli.add_command(day1.day1_part2)
cli.add_command(day2.day2_part1)
cli.add_command(day2.day2_part2)
cli.add_command(day3.day3_part1)
cli.add_command(day3.day3_part2)

if __name__ == "__main__":
    cli()
