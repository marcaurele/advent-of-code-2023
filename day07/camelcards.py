import re
import click


@click.group(help="Advent of code day 7")
def cli():
    pass


@cli.command(help="Day 7 - part 1")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day7_part1(ctx, input):
    p = re.compile(r"(?P<hand>.{5}) (?P<bid>\d+)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    hands = []

    for line in lines:
        m = p.match(line)
        hand = m.group("hand")
        bid = int(m.group("bid"))

        if ctx.obj["DEBUG"]:
            click.echo(f"{hand} -> {bid}")

        hands.append(CardGame(hand, bid))

    sorted_hands = sorted(hands)
    if ctx.obj["DEBUG"]:
        for h in sorted_hands:
            click.echo(h)

    sum = 0
    for i, h in enumerate(sorted_hands):
        sum += (i + 1) * h.bid

    click.secho(f"Total winnings: {sum}", fg="green")


CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


class CardGame:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.cards = {}
        for i in range(5):
            try:
                self.cards[self.hand[i]] += 1
            except KeyError:
                self.cards[self.hand[i]] = 1
        self.rank = self.set_rank()

    def set_rank(self):
        if len(self.cards) == 1:
            # Five of a kind
            return 6
        vals = [v for v in self.cards.values()]
        if len(self.cards) == 2:
            # Four of kind (5) or Full house (4)
            return 5 if vals[0] * vals[1] == 4 else 4
        if len(self.cards) == 3:
            # Three of a kind (3) or Two pair (2)
            return max(vals)
        if len(self.cards) == 4:
            # One pair (1)
            return 1
        # High card (0)
        return 0

    def __str__(self):
        return f"{self.hand}-{self.rank}-{self.cards} -> {self.bid}"

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        if self.rank == other.rank:
            for i in range(5):
                if self.hand[i] == other.hand[i]:
                    continue
                res = CARDS.index(self.hand[i]) < CARDS.index(other.hand[i])
                return res
            else:
                return True
        return False


@cli.command(help="Day 7 - part 2")
@click.pass_context
@click.argument("input", type=click.File("r"))
def day7_part2(ctx, input):
    p = re.compile(r"(?P<hand>.{5}) (?P<bid>\d+)")
    sum = 0
    lines = input.readlines()
    line_length = len(lines[0]) - 1
    number_of_lines = len(lines)
    hands = []

    for line in lines:
        m = p.match(line)
        hand = m.group("hand")
        bid = int(m.group("bid"))

        if ctx.obj["DEBUG"]:
            click.echo(f"{hand} -> {bid}")

        hands.append(CardGameJoker(hand, bid))

    sorted_hands = sorted(hands)
    if ctx.obj["DEBUG"]:
        for h in sorted_hands:
            click.echo(h)

    sum = 0
    for i, h in enumerate(sorted_hands):
        sum += (i + 1) * h.bid

    click.secho(f"Total winnings: {sum}", fg="green")


CARDS_J = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class CardGameJoker:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.cards = {}
        for i in range(5):
            try:
                self.cards[self.hand[i]] += 1
            except KeyError:
                self.cards[self.hand[i]] = 1
        self.rank = self.set_rank()

    def set_rank(self):
        if len(self.cards) == 1:
            # Five of a kind
            return 6
        vals = [v for v in self.cards.values()]
        number_of_joker = self.cards.get("J") or 0
        if len(self.cards) == 2:
            # Four of kind (5) or Full house (4)
            if number_of_joker == 0:
                if vals[0] * vals[1] == 4:
                    return 5
                else:
                    return 4
            else:
                return 6

        if len(self.cards) == 3:
            # Three of a kind (3) or Two pair (2)
            if number_of_joker == 0:
                return max(vals)
            elif number_of_joker == 1:
                return max(vals) + 2
            elif number_of_joker >= 2:
                return 5
            else:
                raise Exception(f"{self.cards}, {number_of_joker}")

        if len(self.cards) == 4:
            # One pair (1)
            return 3 if number_of_joker else 1
        # High card (0)
        return 0 + number_of_joker

    def __str__(self):
        return f"{self.hand}-{self.rank}-{self.cards} -> {self.bid}"

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        if self.rank == other.rank:
            for i in range(5):
                if self.hand[i] == other.hand[i]:
                    continue
                res = CARDS_J.index(self.hand[i]) < CARDS_J.index(other.hand[i])
                return res
            else:
                return True
        return False
