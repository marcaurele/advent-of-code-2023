import click

from day01 import trebuchet as day1


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


cli.add_command(day1.day1_part1)
cli.add_command(day1.day1_part2)

if __name__ == "__main__":
    cli()
