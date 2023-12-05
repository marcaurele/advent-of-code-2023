import re
import click


@click.group(help="Advent of code day 5")
def cli():
    pass


@cli.command(help="Day 5 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day5_part1(ctx, input):
    p = re.compile(r"(\d+)")
    n = re.compile(r"(?P<source>\w+)-to-(?P<destination>\w+) map:")
    lines = input.readlines()
    number_of_lines = len(lines)
    seeds = [int(i) for i in p.findall(lines[0])]
    moves = []
    map = None
    source = None
    destination = None

    if ctx.obj["DEBUG"]:
        click.echo(seeds)

    for line_number in range(1, number_of_lines):
        line = lines[line_number]

        if m := n.match(line):
            source = m.group("source")
            destination = m.group("destination")
            if ctx.obj["DEBUG"]:
                click.echo(f"{source} -> {destination}")
            map = GardenerMap(source, destination)
            moves.append(map)
        elif m := p.findall(line):
            destination_range_start = int(m[0])
            source_range_start = int(m[1])
            range_length = int(m[2])
            if ctx.obj["DEBUG"]:
                click.echo(
                    f"{source_range_start}+{range_length} -> {destination_range_start}+{range_length}"
                )
            map.append(destination_range_start, source_range_start, range_length)
        else:
            # Emtpy line
            if ctx.obj["DEBUG"]:
                click.echo("---" * 15)

    locations = []
    for seed in seeds:
        next = None
        if ctx.obj["DEBUG"]:
            click.echo(f"Seed {seed}", nl=False)
        for m in moves:
            next = m.get_destination(next if next else seed)
            if ctx.obj["DEBUG"]:
                click.echo(f" -> {next}", nl=False)
        locations.append(next)
        if ctx.obj["DEBUG"]:
            click.echo("")

    locations_sorted = sorted(locations)
    if ctx.obj["DEBUG"]:
        click.echo(f"Locations: {locations_sorted}")

    if locations_sorted:
        click.secho(f"Lowest location number: {locations_sorted[0]}", fg="green")


class GardenerMap:
    def __init__(self, source_name, destination_name):
        self.source_name = source_name
        self.destination_name = destination_name
        self.source_range_start = []
        self.source_range_dict = {}
        self.destination_range_start = []
        self.destination_range_dict = {}

    def append(self, destination_range_start, source_range_start, range_length):
        self.source_range_start.append(source_range_start)
        self.source_range_start.sort()
        self.destination_range_start.append(destination_range_start)
        self.destination_range_start.sort()
        self.source_range_dict.update(
            {source_range_start: (destination_range_start, range_length)}
        )
        self.destination_range_dict.update(
            {destination_range_start: (source_range_start, range_length)}
        )

    def get_destination(self, seed) -> int:
        for start_range in self.source_range_start:
            destination_range_start, range_length = self.source_range_dict[start_range]
            if start_range <= seed and seed <= start_range + range_length - 1:
                return destination_range_start + (seed - start_range)

            if start_range > seed:
                return seed
        return seed

    def get_source(self, seed) -> int:
        for destination_range in self.destination_range_start:
            source_range_start, range_length = self.destination_range_dict[
                destination_range
            ]
            if destination_range <= seed and seed < destination_range + range_length:
                return source_range_start + (seed - destination_range)

            if destination_range > seed:
                return seed
        return seed


@cli.command(help="Day 5 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day5_part2(ctx, input):
    s = re.compile(r"(?P<start>\d+)\s+(?P<length>\d+)")
    p = re.compile(r"(\d+)")
    n = re.compile(r"(?P<source>\w+)-to-(?P<destination>\w+) map:")
    lines = input.readlines()
    number_of_lines = len(lines)
    seeds = []
    for f in s.finditer(lines[0]):
        start = int(f.group("start"))
        length = int(f.group("length"))
        if ctx.obj["DEBUG"]:
            click.echo(f"{start} + {length} -> {start + length - 1}")
        seeds.append((start, length))

    moves = []
    map = None
    source = None
    destination = None

    if ctx.obj["DEBUG"]:
        click.echo(seeds)

    for line_number in range(1, number_of_lines):
        line = lines[line_number]

        if m := n.match(line):
            source = m.group("source")
            destination = m.group("destination")
            if ctx.obj["DEBUG"]:
                click.echo(f"----- {source} <- {destination} -----")
            map = GardenerMap(source, destination)
            moves.append(map)
        elif m := p.findall(line):
            destination_range_start = int(m[0])
            source_range_start = int(m[1])
            range_length = int(m[2])
            if ctx.obj["DEBUG"]:
                click.echo(
                    f"{source_range_start}+{range_length} <- {destination_range_start}+{range_length}"
                )
            map.append(destination_range_start, source_range_start, range_length)

    if ctx.obj["DEBUG"]:
        click.echo("=" * 20)

    lowest_location = 0
    while True:
        source = lowest_location
        if ctx.obj["DEBUG"]:
            click.echo(f"-> {lowest_location}\r", nl=False)
        for m in reversed(moves):
            source = m.get_source(source)

        for start, length in seeds:
            if start <= source and source < start + length:
                break
        else:
            lowest_location += 1
            continue
        break

    click.secho(f"Lowest location number: {lowest_location}", fg="green")
