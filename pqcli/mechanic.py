import datetime
import enum
import random
import typing as T
from dataclasses import dataclass, field

from pqcli.config import *


def level_up_time(level: int) -> int:
    # seconds
    return 20 * level * 60


def generate_name() -> str:
    parts = [
        "br|cr|dr|fr|gr|j|kr|l|m|n|pr||||r|sh|tr|v|wh|x|y|z".split("|"),
        "a|a|e|e|i|i|o|o|u|u|ae|ie|oo|ou".split("|"),
        "b|ck|d|g|k|m|n|p|t|v|x|z".split("|"),
    ]
    result = ""
    for i in range(6):
        result += random.choice(parts[i % 3])
    return result.title()


@dataclass
class Stats:
    def __init__(self) -> None:
        self.values = {stat: 0 for stat in Stat}

    def __iter__(self) -> T.Iterable[T.Tuple[Stat, int]]:
        return iter(self.values.items())

    def __setitem__(self, stat: Stat, value: int) -> None:
        self.values[stat] = value

    def __getitem__(self, stat: Stat) -> int:
        return self.values[stat]


@dataclass
class Item:
    name: str
    quantity: int


@dataclass
class Spell:
    name: str
    level: int


class Inventory:
    def __init__(self, items: T.Optional[T.List[Item]] = []) -> None:
        self.items = [] if items is None else items

    def add(self, item_name: str, quantity: int) -> None:
        for item in self.items:
            if item.name == item_name:
                item.quantity += quantity
                break
        else:
            self.items.append(Item(name=item_name, quantity=quantity))


class SpellBook:
    def __init__(self, spells: T.Optional[T.List[Item]] = None) -> None:
        self.spells = [] if spells is None else spells

    def add(self, spell_name: str, level: int) -> None:
        for item in self.spells:
            if item.name == spell_name:
                item.level += level
                break
        else:
            self.spells.append(Spell(name=spell_name, level=level))


class Bar:
    def __init__(self, max_: int, position: int = 0) -> None:
        self.position = position
        self.max_ = max_


class TaskType(enum.Enum):
    task = "task"
    plot = "plot"


@dataclass
class Task:
    task_type: TaskType
    length: int
    description: str


class Player:
    def __init__(
        self,
        name: str,
        birthday: datetime.datetime,
        race: Race,
        class_: Class,
        stats: Stats,
    ) -> None:
        self.name: str = name
        self.birthday: datetime.datetime = birthday
        self.race: Race = race
        self.class_: Class = class_
        self.stats: Stats = stats
        self.level = 1
        self.act = 0

        self.queue: T.List[Task] = [
            Task(
                TaskType.task,
                10,
                "Experiencing an enigmatic and foreboding night vision",
            ),
            Task(
                TaskType.task,
                6,
                "Much is revealed about that wise old bastard you'd underestimated",
            ),
            Task(
                TaskType.task,
                6,
                "A shocking series of events leaves you alone and bewildered, but resolute",
            ),
            Task(
                TaskType.task,
                4,
                "Drawing upon an unrealized reserve of determination, you set out on a long and dangerous journey",
            ),
            Task(TaskType.plot, 2, "Loading"),
        ]

        self.exp_bar = Bar(max_=level_up_time(1))
        self.encum_bar = Bar(max_=stats[Stat.strength] + 10)
        self.quest_bar = Bar(max_=1)
        self.task_bar = Bar(max_=2000)
        self.plot_bar = Bar(max_=sum(task.length for task in self.queue))

        self.inventory = Inventory([Item(name="Gold", quantity=0)])
        self.spell_book = SpellBook()
        self.equipment: T.Dict[Equipment, str] = {
            Equipment.weapon: "Sharp Rock",
            Equipment.hauberk: "-3 Burlap",
        }


def special_item() -> str:
    return interesting_item() + " of " + random.choice(ITEM_OFS)


def interesting_item() -> str:
    return random.choice(ITEM_ATTRIB) + " " + random.choice(SPECIALS)


def boring_item() -> str:
    return random.choice(BORING_ITEMS)


def win_item(player: Player) -> None:
    player.inventory.add(special_item(), 1)


class Roster:
    def __init__(self) -> None:
        self.players: T.List[Player] = []

    def add_player(self, player: Player) -> None:
        self.players.append(player)


class StatsBuilder:
    def __init__(self) -> None:
        self.history: T.List[Stats] = []

    def roll(self) -> Stats:
        stats = Stats()
        for stat in PRIME_STATS:
            stats[stat] = (
                3
                + random.randint(0, 5)
                + random.randint(0, 5)
                + random.randint(0, 5)
            )
        stats[Stat.hp_max] = random.randint(0, 7) + stats[Stat.condition] // 6
        stats[Stat.mp_max] = (
            random.randint(0, 7) + stats[Stat.intelligence] // 6
        )
        self.history.append(stats)
        return stats

    def unroll(self) -> Stats:
        self.history.pop()
        return self.history[-1]


def create_player(
    name: str, race: Race, class_: Class, stats: Stats
) -> Player:
    now = datetime.datetime.now()
    random.seed(now)
    return Player(
        birthday=now, name=name, race=race, class_=class_, stats=stats
    )