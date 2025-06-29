from models.team import Team
from gui import main_gui

def main():
    team = Team("My Basketball Team")
    team.load_from_file()
    main_gui(team)

if __name__ == '__main__':
    main()
