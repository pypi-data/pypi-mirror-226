from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from aasm.utils.iteration import zip_consecutive_pairs

if TYPE_CHECKING:
    from aasm.intermediate.behaviour import (
        Behaviour,
        CyclicBehaviour,
        MessageReceivedBehaviour,
        OneTimeBehaviour,
        SetupBehaviour,
    )


class InitFloatParam:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value

    def print(self) -> None:
        print(f"InitFloatParam {self.name} = {self.value}")


class DistNormalFloatParam:
    def __init__(self, name: str, mean: str, std_dev: str):
        self.name: str = name
        self.mean: str = mean
        self.std_dev: str = std_dev

    def print(self) -> None:
        print(
            f"DistNormalFloatParam {self.name} = normal(mean={self.mean}, std_dev={self.std_dev})"
        )


class DistExpFloatParam:
    def __init__(self, name: str, lambda_: str):
        self.name: str = name
        self.lambda_: str = lambda_

    def print(self) -> None:
        print(f"DistExpFloatParam {self.name} = exp(lambda={self.lambda_})")


class DistUniformFloatParam:
    def __init__(self, name: str, a: str, b: str):
        self.name: str = name
        self.a: str = a
        self.b: str = b

    def print(self) -> None:
        print(f"DistUniformFloatParam {self.name} = uniform(a={self.a}, b={self.b})")


class EnumParam:
    def __init__(self, name: str, enums: List[str]):
        self.name: str = name
        self.enum_values: List[EnumValue] = [
            EnumValue(name, value, percentage)
            for value, percentage in zip_consecutive_pairs(enums)
        ]

    def print(self) -> None:
        print(f"EnumParam {self.name} = {self.enum_values}")


class EnumValue:
    def __init__(self, from_enum: str, value: str, percentage: str):
        self.from_enum: str = from_enum
        self.value: str = value
        self.percentage: str = percentage

    def __str__(self) -> str:
        return f"({self.value}, {self.percentage}; from_enum={self.from_enum})"


class MessageListParam:
    def __init__(self, name: str):
        self.name: str = name

    def print(self) -> None:
        print(f"MessageListParam {self.name} = []")


class ConnectionListParam:
    def __init__(self, name: str):
        self.name: str = name

    def print(self) -> None:
        print(f"ConnectionListParam {self.name} = []")


class FloatListParam:
    def __init__(self, name: str):
        self.name: str = name

    def print(self) -> None:
        print(f"FloatListParam {self.name} = []")


class ModuleVariableParam:
    def __init__(self, name: str, type: str, init_function: str):
        self.name: str = name
        self.type: str = type
        self.init_function: str = init_function

    def print(self) -> None:
        print(f"ModuleVariableParam {self.name}: {self.type}")


class Agent:
    RESERVED_CONNECTION_PARAMS = ["self"]
    RESERVED_CONNECTION_LIST_PARAMS = ["connections"]
    RESERVED_FLOAT_PARAMS = ["connCount", "msgRCount", "msgSCount"]

    def __init__(self, name: str):
        self.name: str = name
        self.init_floats: Dict[str, InitFloatParam] = {}
        self.dist_normal_floats: Dict[str, DistNormalFloatParam] = {}
        self.dist_exp_floats: Dict[str, DistExpFloatParam] = {}
        self.dist_unifrom_floats: Dict[str, DistUniformFloatParam] = {}
        self.enums: Dict[str, EnumParam] = {}
        self.connection_lists: Dict[str, ConnectionListParam] = {}
        self.message_lists: Dict[str, MessageListParam] = {}
        self.float_lists: Dict[str, FloatListParam] = {}
        self.module_variables: Dict[str, ModuleVariableParam] = {}
        self.setup_behaviours: Dict[str, SetupBehaviour] = {}
        self.one_time_behaviours: Dict[str, OneTimeBehaviour] = {}
        self.cyclic_behaviours: Dict[str, CyclicBehaviour] = {}
        self.message_received_behaviours: Dict[str, MessageReceivedBehaviour] = {}
        self._last_modified_behaviour: Behaviour | None = None

    def get_module_variable_type(self, name):
        return self.module_variables[name].type

    @property
    def last_behaviour(self) -> Behaviour:
        if self._last_modified_behaviour is None:
            raise Exception("No behaviour added to agent")
        return self._last_modified_behaviour

    @property
    def param_names(self) -> List[str]:
        return [
            *Agent.RESERVED_CONNECTION_PARAMS,
            *Agent.RESERVED_CONNECTION_LIST_PARAMS,
            *Agent.RESERVED_FLOAT_PARAMS,
            *list(self.init_floats),
            *list(self.dist_normal_floats),
            *list(self.dist_exp_floats),
            *list(self.dist_unifrom_floats),
            *list(self.enums),
            *list(self.connection_lists),
            *list(self.message_lists),
            *list(self.float_lists),
            *list(self.module_variables),
        ]

    @property
    def behaviour_names(self) -> List[str]:
        return [
            *list(self.setup_behaviours),
            *list(self.one_time_behaviours),
            *list(self.cyclic_behaviours),
            *list(self.message_received_behaviours),
        ]

    @property
    def float_param_names(self) -> List[str]:
        return [
            *list(self.init_floats),
            *list(self.dist_normal_floats),
            *list(self.dist_exp_floats),
            *list(self.dist_unifrom_floats),
        ]

    def add_init_float(self, float_param: InitFloatParam) -> None:
        self.init_floats[float_param.name] = float_param

    def add_dist_normal_float(self, float_param: DistNormalFloatParam) -> None:
        self.dist_normal_floats[float_param.name] = float_param

    def add_dist_exp_float(self, float_param: DistExpFloatParam) -> None:
        self.dist_exp_floats[float_param.name] = float_param

    def add_dist_uniform_float(self, float_param: DistUniformFloatParam) -> None:
        self.dist_unifrom_floats[float_param.name] = float_param

    def add_enum(self, enum_param: EnumParam) -> None:
        self.enums[enum_param.name] = enum_param

    def add_connection_list(self, name: str) -> None:
        list_param = ConnectionListParam(name)
        self.connection_lists[list_param.name] = list_param

    def add_message_list(self, name: str) -> None:
        list_param = MessageListParam(name)
        self.message_lists[list_param.name] = list_param

    def add_float_list(self, name: str) -> None:
        list_param = FloatListParam(name)
        self.float_lists[list_param.name] = list_param

    def add_module_variable(self, variable_param: ModuleVariableParam) -> None:
        self.module_variables[variable_param.name] = variable_param

    def add_setup_behaviour(self, behaviour: SetupBehaviour) -> None:
        self.setup_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviour = behaviour

    def add_one_time_behaviour(self, behaviour: OneTimeBehaviour) -> None:
        self.one_time_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviour = behaviour

    def add_cyclic_behaviour(self, behaviour: CyclicBehaviour) -> None:
        self.cyclic_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviour = behaviour

    def add_message_received_behaviour(
        self, behaviour: MessageReceivedBehaviour
    ) -> None:
        self.message_received_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviour = behaviour

    def param_exists(self, name: str) -> bool:
        return name in self.param_names

    def behaviour_exists(self, name: str) -> bool:
        return name in self.behaviour_names

    def name_exists(self, name: str) -> bool:
        return self.param_exists(name) or self.behaviour_exists(name)

    def behaviour_for_template_exists(
        self, msg_type: str, msg_performative: str
    ) -> bool:
        for msg_rcv_behav in self.message_received_behaviours.values():
            if (
                msg_rcv_behav.received_message.type == msg_type
                and msg_rcv_behav.received_message.performative == msg_performative
            ):
                return True
        return False

    def print(self) -> None:
        print(f"Agent {self.name}")
        for init_float_param in self.init_floats.values():
            init_float_param.print()
        for dist_normal_float_param in self.dist_normal_floats.values():
            dist_normal_float_param.print()
        for dist_exp_float_param in self.dist_exp_floats.values():
            dist_exp_float_param.print()
        for dist_uniform_float_param in self.dist_unifrom_floats.values():
            dist_uniform_float_param.print()
        for enum_param in self.enums.values():
            enum_param.print()
        for connection_list_param in self.connection_lists.values():
            connection_list_param.print()
        for message_list_param in self.message_lists.values():
            message_list_param.print()
        for float_list_param in self.float_lists.values():
            float_list_param.print()
        for module_variable in self.module_variables.values():
            module_variable.print()
        for setup_behaviour in self.setup_behaviours.values():
            setup_behaviour.print()
        for one_time_behaviour in self.one_time_behaviours.values():
            one_time_behaviour.print()
        for cyclic_behaviour in self.cyclic_behaviours.values():
            cyclic_behaviour.print()
        for message_received_behaviour in self.message_received_behaviours.values():
            message_received_behaviour.print()
