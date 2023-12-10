import re
import click


@click.group(help="Advent of code day 10")
def cli():
    pass


@cli.command(help="Day 10 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day10_part1(ctx, input):
    p = re.compile(r"(S)")
    lines = input.readlines()

    starting_position = (-1, -1)
    for i, line in enumerate(lines):
        if m := p.search(line):
            starting_position = (i, m.span()[0])
            break

    if ctx.obj["DEBUG"]:
        click.echo(f"Starting position at: {starting_position}")

    s1, s2 = starting_directions(lines, starting_position)

    if ctx.obj["DEBUG"]:
        click.echo(f"Starting positions: {s1} = {s2}")

    s1_previous = None
    s1_move = None
    s2_previous = None
    s2_move = None
    steps = 0
    while True:
        s1_previous = s1_move
        s1_move = s1.move()
        s2_previous = s2_move
        s2_move = s2.move()

        if s1_move == s2_move:
            steps = s1.counter
            click.echo("Joined same position")
            break

        if s1_previous == s2_move and s2_previous == s1_move:
            steps = s1.counter - 1
            click.echo("Passed their position")
            break

        next_s1 = lines[s1_move[0]][s1_move[1]]
        s1.update_letter(next_s1)
        next_s2 = lines[s2_move[0]][s2_move[1]]
        s2.update_letter(next_s2)

        if ctx.obj["DEBUG"]:
            click.echo(f"{next_s1} with {s1.direction}, {next_s2} with {s2.direction}")

    click.secho(f"Number of steps: {steps}", fg="green")


class Position:
    def __init__(self, x, y, letter, direction):
        self.x = x
        self.y = y
        self.letter = letter
        self.direction = direction
        self.counter = 0

    def __str__(self):
        return f"{self.letter} -> {self.direction}"

    def update_letter(self, letter):
        self.letter = letter

    def move(self):
        self.counter += 1
        if self.letter == "|" and self.direction == "U":
            self.x -= 1
            return (self.x, self.y)
        elif self.letter == "|" and self.direction == "D":
            self.x += 1
            return (self.x, self.y)

        elif self.letter == "-" and self.direction == "L":
            self.y -= 1
            return (self.x, self.y)
        elif self.letter == "-" and self.direction == "R":
            self.y += 1
            return (self.x, self.y)

        elif self.letter == "L" and self.direction == "D":
            self.direction = "R"
            self.y += 1
            return (self.x, self.y)
        elif self.letter == "L" and self.direction == "L":
            self.direction = "U"
            self.x -= 1
            return (self.x, self.y)

        elif self.letter == "J" and self.direction == "D":
            self.direction = "L"
            self.y -= 1
            return (self.x, self.y)
        elif self.letter == "J" and self.direction == "R":
            self.direction = "U"
            self.x -= 1
            return (self.x, self.y)

        elif self.letter == "7" and self.direction == "U":
            self.direction = "L"
            self.y -= 1
            return (self.x, self.y)
        elif self.letter == "7" and self.direction == "R":
            self.direction = "D"
            self.x += 1
            return (self.x, self.y)

        elif self.letter == "F" and self.direction == "U":
            self.direction = "R"
            self.y += 1
            return (self.x, self.y)
        elif self.letter == "F" and self.direction == "L":
            self.direction = "D"
            self.x += 1
            return (self.x, self.y)

        raise Exception(
            f"We have an issue at {self.x, self.y} with direction {self.direction}"
        )


def starting_directions(lines, starting_position):
    north = (
        lines[starting_position[0] - 1][starting_position[1]]
        if starting_position[0] > 0
        else "."
    )
    east = (
        lines[starting_position[0]][starting_position[1] + 1]
        if starting_position[1] < len(lines[0])
        else "."
    )
    south = (
        lines[starting_position[0] + 1][starting_position[1]]
        if starting_position[0] < len(lines)
        else "."
    )
    west = (
        lines[starting_position[0]][starting_position[1] - 1]
        if starting_position[1] > 0
        else "."
    )

    if north in ["7", "|", "F"] and south in ["J", "|", "L"]:
        return (
            Position(starting_position[0], starting_position[1], "|", "U"),
            Position(starting_position[0], starting_position[1], "|", "D"),
        )

    if west in ["L", "-", "F"] and east in ["J", "-", "7"]:
        return (
            Position(starting_position[0], starting_position[1], "-", "L"),
            Position(starting_position[0], starting_position[1], "-", "R"),
        )

    if south in ["J", "|", "L"] and east in ["J", "-", "7"]:
        return (
            Position(starting_position[0], starting_position[1], "F", "L"),
            Position(starting_position[0], starting_position[1], "F", "U"),
        )

    if north in ["7", "|", "F"] and east in ["J", "-", "7"]:
        return (
            Position(starting_position[0], starting_position[1], "L", "L"),
            Position(starting_position[0], starting_position[1], "L", "D"),
        )

    if north in ["7", "|", "F"] and west in ["L", "-", "F"]:
        return (
            Position(starting_position[0], starting_position[1], "J", "R"),
            Position(starting_position[0], starting_position[1], "J", "D"),
        )

    if south in ["J", "|", "L"] and west in ["L", "-", "F"]:
        return (
            Position(starting_position[0], starting_position[1], "7", "R"),
            Position(starting_position[0], starting_position[1], "7", "U"),
        )


@cli.command(help="Day 10 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
@click.option("--round", is_flag=True)
def day10_part2(ctx, input, round):
    p = re.compile(r"(S)")
    lines = input.readlines()

    starting_position = (-1, -1)
    for i, line in enumerate(lines):
        if m := p.search(line):
            starting_position = (i, m.span()[0])
            break

    if ctx.obj["DEBUG"]:
        click.echo(f"Starting position at: {starting_position}")

    s1, s2 = starting_directions(lines, starting_position)
    start_letter = s1.letter

    if ctx.obj["DEBUG"]:
        click.echo(f"Starting positions: {s1} = {s2}")

    s1_previous = None
    s1_move = None
    s2_previous = None
    s2_move = None
    positions = {
        starting_position,
    }
    while True:
        s1_previous = s1_move
        s1_move = s1.move()
        s2_previous = s2_move
        s2_move = s2.move()
        positions.add(s1_move)
        positions.add(s2_move)

        if s1_move == s2_move:
            if ctx.obj["DEBUG"]:
                click.echo("Joined same position")
            break

        if s1_previous == s2_move and s2_previous == s1_move:
            if ctx.obj["DEBUG"]:
                click.echo("Passed their position")
            break

        next_s1 = lines[s1_move[0]][s1_move[1]]
        s1.update_letter(next_s1)
        next_s2 = lines[s2_move[0]][s2_move[1]]
        s2.update_letter(next_s2)

    insider_outside = InsideOutside(positions, ctx, round)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "S":
                insider_outside.count((i, j), start_letter)
            else:
                insider_outside.count((i, j), c)
        if ctx.obj["DEBUG"]:
            click.echo("")

    click.secho(f"Number of insider and outsider: {insider_outside}")


class InsideOutside:
    def __init__(self, pipe, ctx, round):
        self.insider = 0
        self.outsider = 0
        self.inside = False
        self.last_cross = None
        self.pipe = pipe
        self.ctx = ctx
        self.round = round

    def __str__(self):
        return f"insider: {self.insider}, outsider: {self.outsider}"

    def count(self, position, letter):
        if position in self.pipe:
            if letter == "|":
                self.inside = not self.inside
                if self.ctx.obj["DEBUG"]:
                    click.secho("│", fg="red", nl=False)

            elif letter == "F" and self.last_cross == None:
                self.last_cross = "F"
                if self.ctx.obj["DEBUG"]:
                    click.secho("╭" if self.round else "┌", fg="red", nl=False)
            elif letter == "F" and self.last_cross != None:
                raise Exception(
                    f"Issue with F at position {position}, last cross: {self.last_cross}"
                )

            elif letter == "7" and self.last_cross == "L":
                self.inside = not self.inside
                self.last_cross = None
                if self.ctx.obj["DEBUG"]:
                    click.secho("╮" if self.round else "┐", fg="red", nl=False)
            elif letter == "7":
                self.last_cross = None
                if self.ctx.obj["DEBUG"]:
                    click.secho("╮" if self.round else "┐", fg="red", nl=False)

            elif letter == "L" and self.last_cross == None:
                self.last_cross = "L"
                if self.ctx.obj["DEBUG"]:
                    click.secho("╰" if self.round else "└", fg="red", nl=False)
            elif letter == "L" and self.last_cross != None:
                raise Exception(
                    f"Issue with L at position {position}, last cross: {self.last_cross}"
                )

            elif letter == "J" and self.last_cross == "F":
                self.inside = not self.inside
                self.last_cross = None
                if self.ctx.obj["DEBUG"]:
                    click.secho("╯" if self.round else "┘", fg="red", nl=False)
            elif letter == "J":
                self.last_cross = None
                if self.ctx.obj["DEBUG"]:
                    click.secho("╯" if self.round else "┘", fg="red", nl=False)

            elif letter == "-":
                if self.ctx.obj["DEBUG"]:
                    click.secho("─", fg="red", nl=False)

        else:
            if self.inside:
                self.insider += 1
                if self.ctx.obj["DEBUG"]:
                    click.secho("I", fg="green", nl=False)
            else:
                self.outsider += 1
                if self.ctx.obj["DEBUG"]:
                    click.secho("O", nl=False)
