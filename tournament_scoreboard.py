"""Maintain and display a simple sports tournament scoreboard."""

import logging
import secrets
import tempfile
from typing import TypedDict

POINTS = {"win": 3, "draw": 1, "loss": 0}
LOGGER = logging.getLogger(__name__)


class TeamStats(TypedDict):
    """Statistics and roster for one tournament team."""

    played: int
    won: int
    drawn: int
    lost: int
    gf: int
    ga: int
    players: list[str]


teams: dict[str, TeamStats] = {}
matches: list[tuple[str, str, int, int]] = []


def add_team(team_name: str, players: list[str] | None = None) -> None:
    """Register a team, using an independent copy of its player list."""
    if not isinstance(team_name, str) or not team_name.strip():
        raise ValueError("team_name must be a non-empty string")
    if team_name in teams:
        raise ValueError(f"Team {team_name!r} is already registered")
    if players is not None and any(
        not isinstance(player, str) or not player.strip() for player in players
    ):
        raise ValueError("players must contain non-empty strings")

    teams[team_name] = {
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "gf": 0,
        "ga": 0,
        "players": list(players) if players is not None else [],
    }


def _validate_goals(home_goals: int, away_goals: int) -> None:
    """Reject goal counts that are not non-negative integers."""
    for label, value in (
        ("home_goals", home_goals),
        ("away_goals", away_goals),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{label} must be a non-negative integer")


def match_result(home_goals: int, away_goals: int) -> str:
    """Return the match outcome from the home team's perspective."""
    _validate_goals(home_goals, away_goals)

    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(
    home: str, away: str, home_goals: int, away_goals: int
) -> None:
    """Validate and record a match, updating both teams' statistics."""
    if home not in teams:
        raise KeyError(f"Unknown home team: {home}")
    if away not in teams:
        raise KeyError(f"Unknown away team: {away}")
    if home == away:
        raise ValueError("A team cannot play against itself")

    _validate_goals(home_goals, away_goals)
    result = match_result(home_goals, away_goals)

    sides = (
        (home, home_goals, away_goals),
        (away, away_goals, home_goals),
    )

    for team_name, scored, conceded in sides:
        stats = teams[team_name]
        stats["played"] += 1
        stats["gf"] += scored
        stats["ga"] += conceded

    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (
            (home, away) if result == "home" else (away, home)
        )
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1

    matches.append((home, away, home_goals, away_goals))


def points(team_name: str) -> int:
    """Return league points for a registered team."""
    stats = teams[team_name]
    return (
        stats["won"] * POINTS["win"]
        + stats["drawn"] * POINTS["draw"]
    )


def goal_difference(team_name: str) -> int:
    """Return a team's goals scored minus goals conceded."""
    stats = teams[team_name]
    return stats["gf"] - stats["ga"]


def league_table() -> list[str]:
    """Return team names ordered by points and then goal difference."""
    return sorted(
        teams,
        key=lambda team_name: (
            points(team_name),
            goal_difference(team_name),
        ),
        reverse=True,
    )


def is_top_two(team_name: str) -> bool:
    """Return whether a registered team is currently in the top two."""
    if team_name not in teams:
        raise KeyError(f"Unknown team: {team_name}")
    return team_name in league_table()[:2]


def toss_coin() -> str:
    """Return a randomly selected side of a coin."""
    return secrets.choice(("Heads", "Tails"))


def table_file_path() -> str:
    """Create a temporary JSON file and return its path."""
    with tempfile.NamedTemporaryFile(
        prefix="tournament_table_",
        suffix=".json",
        delete=False,
    ) as temporary_file:
        return temporary_file.name


def main() -> None:
    """Run a short demonstration of the scoreboard."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    for name in (
        "Royal Strikers",
        "City Rovers",
        "Lake United",
        "Hill Warriors",
    ):
        add_team(name)

    print(f"Toss: {toss_coin()}")

    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)

    print("Pos Team Played Won Drawn Lost Pts")

    for position, team_name in enumerate(league_table(), start=1):
        stats = teams[team_name]
        print(
            f"{position} {team_name} {stats['played']} {stats['won']} "
            f"{stats['drawn']} {stats['lost']} {points(team_name)}"
        )

    print(f"Is City Rovers in the top two? {is_top_two('City Rovers')}")
    print(f"Matches played: {len(matches)}")


if __name__ == "__main__":
    main()
