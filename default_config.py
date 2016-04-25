# -*- coding: utf-8 -*-
DEFAULT_TYPES = ["real"]
DEFAULT_TEAM_IDS = ["1"]
DEFAULT_LOCATION = "."
DEFAULT_ACTIVE_GROUPS = ["A", "B"]

TEAMS = {
    # id: name
    "1": "Team 1A",
    "2": "Team 2A",
    "3": "Team 3A",
    "4": "Team 4A",
    "5": "Team 1B",
    "6": "Team 2B",
    "7": "Team 3B",
    "8": "Team 4B"
}

GROUPS = {
    # name: [team_ids]
    "A": ["1", "2", "3", "4"],
    "B": ["5", "6", "7", "8"]
}

PLAYED_FIXTURES = {
    # group: [fixtures1, fixtures2, ...]
    # fixtures1 -> ((fixture), (fixture), (fixture))
    # fixture -> (team1_id, team2_id, (result,))
    # result -> tuple with number from (1, 0, 2) == (win team 1, draw, win team 2)
    "A": [
        (("1", "2", (1,)), ("3", "4", (2,))),
        (("1", "3", (2,)), ("2", "4", (0,)))
    ],
    "B": [
        (("5", "6", (1,)), ("7", "8", (1,))),
        (("5", "7", (0,)), ("6", "8", (2,)))
    ]
}
FIXTURES = {
    # group: fixture_possibility
    # fixture_possibility -> name: PLAYED_FIXTURES + [fixtures1, fixtures2, fixtures3]
    # fixtures1 -> ((fixture), (fixture), (fixture))
    # fixture -> (team1_id, team2_id, (possible_result_combination))
    # possible_result_combination -> tuple with any combination of numbers
    # from (1, 0, 2) == (win team 1, draw, win team 2)
    "A": {
        "real": PLAYED_FIXTURES["A"] + [
            (("1", "4", (1, 0, 2)), ("2", "3", (1, 0, 2)))
        ]
    },
    "B": {
        "real": PLAYED_FIXTURES["B"] + [
            (("5", "8", (1, 0, 2)), ("6", "7", (1, 0, 2))),
        ]
    }
}

DESC = {
    # group: descriptions
    # descriptions -> name: description
    # name must be in fixture_possibility.name
    "A": {
        "real": "sve jos visi u zraku"
    },
    "B": {
        "real": "sve jos visi u zraku",
    }
}

INIT_STATES = {
    "A": [[{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}]],
    "B": [[{"8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0}]]
}
