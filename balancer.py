import itertools
import random


class Balancer:
    def __init__(self, skill_dict, method):
        self.skill_array = [(key, value) for key, value in skill_dict.items()]
        self.method = method

    def balance_teams(self):
        # Checks if the skill array is empty
        if len(self.skill_array) == 0:
            return "No one reacted to this message, so teams can't be assigned"
        # Checks if the skill array is not odd
        if len(self.skill_array) % 2 != 0:
            return (
                "An odd number of people reacted, so equal teams can't be constructed"
            )

        # Specifies the balance of teams through rough matches in skill
        # For example, if players are assigned an integer skill value from 1-10,
        # teams would be balanced if the sums of the players' skill on each team
        # are rougly equal. Objectively more fair than the "team captain" method
        if self.method == "true_balance":
            skill_sum = sum(x[1] for x in self.skill_array)
            # Desired total 'skill' of each team
            skill_balance = int(skill_sum / 2)
            # Creates an array of team combinations and their proximity to the desired
            # balanced skill sum. A smaller difference means that the said combination
            # is close to being balanced.
            comb_closest = [
                (combination, abs(sum(x[1] for x in combination) - skill_balance))
                for combination in itertools.combinations(
                    [(x[0], x[1]) for x in self.skill_array],
                    int(len(self.skill_array) / 2),
                )
            ]
            # Filter out the team combinations that aren't balanced as much as they can be
            closest_diff = min(comb_closest, key=lambda x: x[1])[1]
            filtered = list(filter(lambda a: a[1] == closest_diff, comb_closest))
            team1 = list((filtered[random.randrange(len(filtered))])[0])
            # Team 1 has already been determined, then Team 2 will just be the remaining players
            for x in team1:
                self.skill_array.remove(x)
            team2 = self.skill_array
            # Sums the skill to display later
            team1_sum = sum(x[1] for x in team1)
            team2_sum = sum(x[1] for x in team2)
            # Creates a nice formatted string to output to the Discord bot
            team1 = [f"{x[0]} ({x[1]})" for x in team1]
            team2 = [f"{x[0]} ({x[1]})" for x in team2]
            return team1, team1_sum, team2, team2_sum

        # Method to handle balancing teams by the "team captain" method.
        # Pretty much the same as a elementary school kickball selection process.
        # The best players will line everybody up based on skill and in alternating turns,
        # will pick the next best available player.
        elif self.method == "skill_draft":
            sorted_skills = sorted(self.skill_array, key=lambda x: x[1], reverse=True)
            team1 = [sorted_skills[i] for i in range(len(sorted_skills)) if i % 2 != 0]
            team2 = [sorted_skills[i] for i in range(len(sorted_skills)) if i % 2 == 0]
            team1_sum = sum(x[1] for x in team1)
            team2_sum = sum(x[1] for x in team2)
            team1 = [f"{x[0]} ({x[1]})" for x in team1]
            team2 = [f"{x[0]} ({x[1]})" for x in team2]
            return team1, team1_sum, team2, team2_sum

        # Will add a better error handler later
        else:
            return "An unknown error occurred."

    # Creates a nice formatted string to each of the teams' members; for Discord formatting
    def to_string(self, team_array):
        string = ""
        for member in team_array:
            string += member + "\n"
        return string


if __name__ == "__main__":
    skills = {
        "Alex": 5,
        "Brendan": 2,
        "Charlie": 1,
        "Daniel": 9,
        "Elmer": 6,
        "Frank": 3,
        "Grant": 4,
    }

    balancer = Balancer(skills, "true_balance")
    try:
        team1, team1_sum, team2, team2_sum = balancer.balance_teams()
        print(
            "**Team 1:**\n"
            + balancer.to_string(team1)
            + "\nSum: "
            + str(team1_sum)
            + "\n"
        )
        print("**Team 2:**\n" + balancer.to_string(team2) + "\nSum: " + str(team2_sum))

    except:
        error = balancer.balance_teams()
        print(error)
