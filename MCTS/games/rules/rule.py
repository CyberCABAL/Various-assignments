from games.actions import Action


# A rule that allow or prohibits something. Should be as small as possible.
class Rule:
    def __init__(self, rule: callable, name: str):
        self.name = name
        self.rule = rule    # It is a function that gives the answer as to whether something is legal.

    def is_valid(self, action: Action, map_instance=None, p: bool = False):
        if not self.rule(action, map_instance):
            if p:
                print("Rejected by rule:", self.name)   # Debug to say what caused it to be rejected.
            return False
        return True

    def __str__(self):
        return "Rule: " + self.name
