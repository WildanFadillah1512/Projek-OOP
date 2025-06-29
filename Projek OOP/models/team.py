import json
import os
from models.player import Player
from models.coach import Coach

class Team:
    def __init__(self, name):
        self.name = name
        self.coach = None
        self.players = []

    def set_coach(self, coach):
        self.coach = coach

    def add_player(self, player):
        self.players.append(player)

    def get_roster(self):
        return [player.show_info() for player in self.players]

    def save_to_file(self, filepath='data/team.json'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            'name': self.name,
            'coach': self.coach.to_dict() if self.coach else None,
            'players': [p.to_dict() for p in self.players]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filepath='data/team.json'):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.name = data.get('name', self.name)

                coach_data = data.get('coach')
                if coach_data:
                    self.set_coach(Coach.from_dict(coach_data))

                self.players = []
                for p in data.get('players', []):
                    self.add_player(Player.from_dict(p))
