import re
import click


@click.group(help="Advent of code day 4")
def cli():
    pass


@cli.command(help="Day 4 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day4_part1(ctx, input):
    p = re.compile(
        r"^Card\s+(?P<card_number>\d+): (?P<winning_numbers>[\d|\s]+) \| (?P<scratching_numbers>[\d|\s]+)\n$"
    )
    n = re.compile(r"(\d+)")
    sum = 0
    lines = input.readlines()
    for line in lines:
        m = p.search(line)
        card_number = int(m.group("card_number"))
        winning_numbers = {int(a) for a in n.findall(m.group("winning_numbers"))}
        scratching_numbers = {int(a) for a in n.findall(m.group("scratching_numbers"))}

        if ctx.obj["DEBUG"]:
            click.echo(f"{card_number} - {winning_numbers} {scratching_numbers}")

        matching_numbers = winning_numbers.intersection(scratching_numbers)
        matching_count = len(matching_numbers)
        if ctx.obj["DEBUG"]:
            if matching_count > 0:
                click.echo(
                    f"{card_number} - {matching_numbers} -> +{pow(2, len(matching_numbers) - 1)}"
                )
            else:
                click.echo(f"{card_number} - {matching_numbers} -> +0")

        sum += pow(2, len(matching_numbers) - 1) if matching_count > 0 else 0

    click.secho(f"Scratchcards points: {sum}", fg="green")


@cli.command(help="Day 4 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day4_part2(ctx, input):
    p = re.compile(
        r"^Card\s+(?P<card_number>\d+): (?P<winning_numbers>[\d|\s]+) \| (?P<scratching_numbers>[\d|\s]+)\n$"
    )
    n = re.compile(r"(\d+)")
    sum = 0
    lines = input.readlines()
    number_of_lines = len(lines)
    cards = {i + 1: 1 for i in range(number_of_lines)}
    for line in lines:
        m = p.search(line)
        # click.echo(f"{m.groups()}")
        card_number = int(m.group("card_number"))
        winning_numbers = {int(a) for a in n.findall(m.group("winning_numbers"))}
        scratching_numbers = {int(a) for a in n.findall(m.group("scratching_numbers"))}
        # click.echo(f"{card_number} - {winning_numbers} {scratching_numbers}")
        matching_numbers = winning_numbers.intersection(scratching_numbers)
        matching_count = len(matching_numbers)
        for i in range(matching_count):
            cards[card_number + 1 + i] += 1 * cards[card_number]
        if ctx.obj["DEBUG"]:
            click.echo(
                f"{card_number} with {cards[card_number]} copies -> {matching_count} matches => +{[card_number + i + 1 for i in range(matching_count)]}"
            )

        sum += cards[card_number]

    click.secho(f"Scratchcards points: {sum}", fg="green")
