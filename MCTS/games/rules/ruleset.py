from games.actions import Action


# The entire set of rules for a game. Can be slow to do it this way, so use such a rule system carefully.
class RuleSet:
    def __init__(self, rules: list = None):
        self.rules = rules

    def is_valid(self, action: Action, map_instance=None, p: bool = False):
        for rule in self.rules:
            if not callable(rule.rule):
                raise Exception(str(rule) + " is not callable.")
            if not rule.is_valid(action, map_instance, p):
                return False    # It is enough that one rule forbids this for it to not be allowed.
        return True  # All rules said "ok".
