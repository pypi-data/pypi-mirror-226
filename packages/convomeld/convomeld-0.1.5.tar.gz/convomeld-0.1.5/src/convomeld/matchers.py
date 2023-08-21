from abc import ABC, abstractmethod
from typing import Union
from collections.abc import Sequence
from convomeld.state import Action


class ActionMatcher(ABC):
    @abstractmethod
    def _match(self, action1, action2) -> bool:
        pass

    def match(self, actions1, actions2) -> bool:
        if isinstance(actions1, Action):
            actions1 = [actions1]
        if isinstance(actions2, Action):
            actions2 = [actions2]

        if len(actions1) != len(actions2):
            return False

        for action1, action2 in zip(actions1, actions2):
            if not self._match(action1, action2):
                return False

        return True


class SimpleActionMatcher(ActionMatcher):
    def _match(self, action1, action2) -> bool:
        return (
            action1.group_name == action2.group_name and action1.value == action2.value
        )


class TriggerValueMatcher(ABC):
    @abstractmethod
    def match(self, trigger_value1, trigger_value2):
        pass


class SimpleTriggerValueMatcher(TriggerValueMatcher):
    def match(self, trigger_value1, trigger_value2):
        return str(trigger_value1) == str(trigger_value2)
