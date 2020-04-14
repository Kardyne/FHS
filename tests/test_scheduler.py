""" This module contains tests for the scheduler. """
import itertools
from typing import List, Tuple

import pytest

from scheduler import create_schedule, Game, Team


def create_flattened_schedule(team_count: int, return_game: bool) -> List[Game]:
    """ Creates a flattened schedule with the given team count.

    Parameters
    ----------
    team_count : int
        Number of teams generated for the schedule. Must be greater than zero.
    return_game : bool
        Whether to generate return games.

    Returns
    -------
    List[Game]
        A flattened schedule.
    """
    team_list: List[int] = list(range(team_count))
    schedule: List[List[Game]] = create_schedule(team_list, return_game)
    # Flatten the schedule to have a single list containing all games
    return list(itertools.chain.from_iterable(schedule))



@pytest.mark.parametrize("team_count", list(range(1, 10)))
@pytest.mark.parametrize("return_game", [False, True])
def test_uniqueness(team_count: int, return_game: bool) -> None:
    """ Checks that schedules only have unique games.

    Parameters
    ----------
    team_count : int
        Number of teams generated for the schedule. Must be greater than zero.
    return_game : bool
        Whether to generate return games.
    """
    flattened_schedule: List[Game] = create_flattened_schedule(team_count, return_game)
    # Compare the size of the set (containing unique elements) to the size of
    # the flattened schedule (containing all games)
    assert len(flattened_schedule) == len(set(flattened_schedule))


@pytest.mark.parametrize("team_count", list(range(1, 10)))
@pytest.mark.parametrize("return_game", [False, True])
def test_length(team_count: int, return_game: bool) -> None:
    """ Checks that the schedule contains the appropriate game count.

    Parameters
    ----------
    team_count : int
        Number of teams generated for the schedule. Must be greater than zero.
    return_game : bool
        Whether to generate return games.
    """
    flattened_schedule: List[Game] = create_flattened_schedule(team_count, return_game)
    # The scheduling process adds a bogus team for odd counts
    # For the total number of games, this acts as if there was another team
    normalized_team_count: int = team_count
    if normalized_team_count % 2 == 1:
        normalized_team_count += 1
    if return_game:
        assert len(flattened_schedule) == normalized_team_count * (
            normalized_team_count - 1
        )
    else:
        assert (
            len(flattened_schedule)
            == (normalized_team_count * (normalized_team_count - 1)) // 2
        )
