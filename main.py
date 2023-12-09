#!/bin/python3
import click

from day01 import trebuchet as day1
from day02 import cube_conundrum as day2
from day03 import gear_ratios as day3
from day04 import scratchcards as day4
from day05 import gardener as day5
from day06 import boatraces as day6
from day07 import camelcards as day7
from day08 import wastelands as day8
from day09 import mirage as day9


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
cli.add_command(day4.day4_part1)
cli.add_command(day4.day4_part2)
cli.add_command(day5.day5_part1)
cli.add_command(day5.day5_part2)
cli.add_command(day6.day6_part1)
cli.add_command(day6.day6_part2)
cli.add_command(day7.day7_part1)
cli.add_command(day7.day7_part2)
cli.add_command(day8.day8_part1)
cli.add_command(day8.day8_part2)
cli.add_command(day9.day9_part1)
cli.add_command(day9.day9_part2)

if __name__ == "__main__":
    cli()
