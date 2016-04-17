# -*- coding: utf-8 -*-
import os
import argparse
import local as config


class ArgParser(object):
    @staticmethod
    def get_parser(args):
        args = args
        parser = argparse.ArgumentParser(description='Process some inputs.')

        for key, value in args.iteritems():
            parser.add_argument(*key, **value)
        return parser


class LeagueCalculator(object):
    TEAMS = config.TEAMS
    GROUPS = config.GROUPS
    PLAYED_FIXTURES = config.PLAYED_FIXTURES
    FIXTURES = config.FIXTURES
    DESC = config.DESC

    def __init__(self):
        self.reset()

    def reset(self):
        self.set_init_combs()
        self.set_init_states()

    def set_init_combs(self):
        self.COMBS = {}
        for group in self.GROUPS:
            self.COMBS[group] = []

    def set_init_states(self):
        self.STATES = {}
        for group in self.GROUPS:
            self.STATES[group] = [[{team_id: 0 for team_id in self.GROUPS[group]}]]

    def not_only_init_state(self):
        return len(self.STATES[group]) > 1

    def set_fixture_types(self, fixture_types):
        self.fixture_types = fixture_types

    def generate_combinations(self):
        for group, fixture_type in self.fixture_types.iteritems():
            if group in self.GROUPS:
                if fixture_type in self.FIXTURES[group]:
                    print fixture_type
                    for fixtures in self.FIXTURES[group][fixture_type]:
                        self.COMBS[group].append([])
                        for r1 in fixtures[0][2]:
                            for r2 in fixtures[1][2]:
                                for r3 in fixtures[2][2]:
                                    self.COMBS[group][-1].append([
                                        (fixtures[0][0], fixtures[0][1], r1),
                                        (fixtures[1][0], fixtures[1][1], r2),
                                        (fixtures[2][0], fixtures[2][1], r3)
                                    ])

    def calculate(self):
        self.generate_combinations()
        for group in self.GROUPS:
            for combs in self.COMBS[group]:
                current_states = self.STATES[group][-1][:]
                new_states = []
                for comb in combs:
                    for state in current_states:
                        new_state = {}
                        used_teams = []
                        for home, away, result in comb:
                            used_teams.append(home)
                            used_teams.append(away)
                            new_state[home] = state[home] + (3 if result == 1 else 1 if result == 0 else 0)
                            new_state[away] = state[away] + (3 if result == 2 else 1 if result == 0 else 0)
                        teams_not_used = [team for team in self.GROUPS[group] if team not in used_teams]
                        for team in teams_not_used:
                            new_state[team] = state[team]
                        new_states.append(new_state.copy())
                self.STATES[group].append(new_states[:])

        if not self.not_only_init_state():
            return False

        return True

    def pretty_print(self):
        if self.not_only_init_state():
            for group in self.fixture_types:
                print "GRUPA %s\n" % group
                for state in self.STATES[group][-1]:
                    for team_id, points in sorted([(team_id, points) for team_id, points in state.iteritems()], key=lambda x: x[1], reverse=True):
                        print "%s %s" % (self.TEAMS[team_id], points)
                    print ""

    def save_to_file(self, location):
        if self.not_only_init_state():
            for group in self.fixture_types:
                with open(os.path.join(location, "%s_%s.txt" % (group, self.fixture_types[group])), 'wb') as _file:
                    _file.write("GRUPA %s\n\n" % group)
                    for state in self.STATES[group][-1]:
                        for team_id, points in sorted([(team_id, points) for team_id, points in state.iteritems()], key=lambda x: x[1], reverse=True):
                            _file.write("%s %s\n" % (self.TEAMS[team_id], points))
                        _file.write("\n")

    def get_group_for_team_id(self, team_id):
        return "A" if team_id in self.GROUPS["A"] else "B" if team_id in self.GROUPS["B"] else None

    def print_team_perc(self, team_id):
        group = self.get_group_for_team_id(team_id)
        if group and self.not_only_init_state():
            numbers = {}
            for state in self.STATES[group][-1]:
                # sortiramo po bodovima i onda po team idu za najgori slucaj da dijelimo 5. mjesto
                for idx, (t_id, points) in enumerate(sorted([(tid, points) for tid, points in state.iteritems()], key=lambda x: (x[1], int(x[0])), reverse=True)):
                    if t_id == team_id:
                        position = idx + 1
                        if position not in numbers:
                            numbers[position] = 0
                        numbers[position] += 1

            total = sum(numbers.values())
            if self.fixture_types[group] in self.DESC[group]:
                print "\n%s - %s: %s\n" % (group, self.TEAMS[team_id], self.DESC[group][self.fixture_types[group]])
            for key, value in numbers.iteritems():
                print "%s %.2f%%" % (key, float(value)/total * 100)


if __name__ == "__main__":
    args = {
        ('-ft', ): {
            'default': config.DEFAULT_TYPES,
            'dest': 'types',
            'nargs': '*',
            'type': str,
            'help': 'types'
        },
        ('-ta', ): {
            'default': config.DEFAULT_TEAM_IDS,
            'dest': 'team_ids',
            'nargs': '*',
            'type': str,
            'help': 'ids of teams to show results for'
        },
        ('-stf', '--save_to_file'): {
            'default': False,
            'action': 'store_true',
            'dest': 'save_to_file',
            'help': 'save possible outcomes to file'
        },
        ('-l', '--location'): {
            'default': config.DEFAULT_LOCATION,
            'dest': 'location',
            'type': str,
            'help': 'location to store outcome files'
        }
    }

    parser = ArgParser.get_parser(args)
    args = parser.parse_args()

    lc = LeagueCalculator()
    group_teams = {}
    for team_id in args.team_ids:
        group = lc.get_group_for_team_id(team_id)
        if group not in group_teams:
            group_teams[group] = []
        group_teams[group].append(team_id)

    for group, team_ids in group_teams.iteritems():
        for _type in args.types:
            lc.reset()
            lc.set_fixture_types({ group: _type })
            if lc.calculate():
                if args.save_to_file:
                    lc.save_to_file(args.location)
                for team_id in team_ids:
                    lc.print_team_perc(team_id)
