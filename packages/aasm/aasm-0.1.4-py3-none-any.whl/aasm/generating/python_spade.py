from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.generating.code import Code
from aasm.generating.python_code import PythonCode
from aasm.generating.python_graph import PythonGraph
from aasm.generating.python_module import PythonModule

from aasm.intermediate.action import SendMessageAction
from aasm.intermediate.argument import (
    AgentParam,
    Connection,
    ConnectionList,
    EnumValue,
    Float,
    FloatList,
    MessageList,
    ReceivedMessageParam,
    SendMessageParam,
)
from aasm.intermediate.behaviour import MessageReceivedBehaviour
from aasm.intermediate.block import Block
from aasm.intermediate.declaration import (
    ConnectionDeclaration,
    FloatDeclaration,
    ModuleVariableDeclaration,
)
from aasm.intermediate.instruction import (
    Add,
    AddElement,
    Clear,
    Comparaison,
    Cos,
    Divide,
    ExpDist,
    ExponentiationOperation,
    IfEqual,
    IfGreaterThan,
    IfGreaterThanOrEqual,
    IfInList,
    IfLessThan,
    IfLessThanOrEqual,
    IfNotEqual,
    IfNotInList,
    Length,
    ListElementAccess,
    ListRead,
    ListWrite,
    Logarithm,
    Logs,
    LogsCritical,
    LogsDebug,
    LogsError,
    LogsInfo,
    LogsWarning,
    MathOperation,
    Modulo,
    Multiply,
    NormalDist,
    Power,
    RemoveElement,
    RemoveNElements,
    Round,
    Send,
    Set,
    Sin,
    Subset,
    Subtract,
    TrigonometryOperation,
    UniformDist,
    WhileEqual,
    WhileGreaterThan,
    WhileGreaterThanOrEqual,
    WhileLessThan,
    WhileLessThanOrEqual,
    WhileNotEqual,
    ModuleInstruction,
)
from aasm.parsing.parse import parse_lines

if TYPE_CHECKING:
    from aasm.intermediate.action import Action
    from aasm.intermediate.agent import Agent
    from aasm.intermediate.argument import Argument
    from aasm.intermediate.behaviour import Behaviour
    from aasm.intermediate.message import Message as IntermediateMessage
    from aasm.modules.module import Module


def get_spade_code(
    aasm_lines: List[str],
    indent_size: int = 4,
    debug: bool = False,
    modules: None | List[Module] = None,
) -> Code:
    """Generates SPADE code in Python from `aasm_lines`.

    Parameters
    ----------
    aasm_lines: List[str]
        Lines of code written in Agents Assembly

    indent_size: int, optional
        Python code indentation size

    debug: bool, optional
        Print the translator debug information to the standard output

    modules: List[Module], optional
        A list of Agents Assembly Modules compatible with SPADE platform

    Returns
    -------
    SPADE code along with the algorithm for the graph generation

    Raises
    ------
    PanicException
        If an error is detected while parsing the `aasm_lines`.
    """
    if modules is None:
        modules = []
    parsed = parse_lines(aasm_lines, debug, modules)
    module_code_lines = []
    for module in modules:
        module_code_lines += PythonModule(indent_size, module).code_lines
    return Code(
        PythonSpadeCode(indent_size, parsed.agents, modules).code_lines,
        PythonGraph(indent_size, parsed.graph).code_lines,
        module_code_lines,
    )


class PythonSpadeCode(PythonCode):
    def __init__(self, indent_size: int, agents: List[Agent], modules: List[Module]):
        super().__init__(indent_size)
        self.modules = modules
        self.target = "spade"
        self.filter_modules()
        for agent in agents:
            self.add_newlines(2)
            self.generate_agent(agent)
            self.add_required_imports()

    def filter_modules(self):
        self.modules = [
            target_mod
            for target_mod in self.modules
            for target in target_mod.targets
            if target.name == self.target
        ]

    def generate_agent(self, agent: Agent) -> None:
        self.add_line(f"class {agent.name}(spade.agent.Agent):", {"spade"})
        self.indent_right()

        self.add_agent_constructor(agent)
        self.add_newline()

        self.add_float_utils()
        self.add_newline()

        self.add_message_utils()
        self.add_newline()

        self.add_agent_setup(agent)
        self.add_newline()

        self.add_backup_behaviour(agent)
        self.add_newline()

        for setup_behaviour in agent.setup_behaviours.values():
            self.add_agent_behaviour(
                setup_behaviour, "spade.behaviour.OneShotBehaviour"
            )
            self.add_newline()

        for one_time_behaviour in agent.one_time_behaviours.values():
            self.add_agent_behaviour(
                one_time_behaviour, "spade.behaviour.TimeoutBehaviour"
            )
            self.add_newline()

        for cyclic_behaviour in agent.cyclic_behaviours.values():
            self.add_agent_behaviour(
                cyclic_behaviour, "spade.behaviour.PeriodicBehaviour"
            )
            self.add_newline()

        for message_received_behaviour in agent.message_received_behaviours.values():
            self.add_agent_behaviour(
                message_received_behaviour, "spade.behaviour.CyclicBehaviour"
            )
            self.add_newline()

        self.indent_left()

    def add_agent_constructor(self, agent: Agent) -> None:
        self.add_line(
            "def __init__(self, jid, password, backup_method = None, backup_queue = None, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):"
        )
        self.indent_right()

        self.add_line("super().__init__(jid, password, verify_security=False)")
        self.add_line(
            "if logger: logger.debug(f'[{jid}] Received parameters: jid: {jid}, password: {password}, backup_method: {backup_method}, backup_queue: {backup_queue}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}')"
        )
        self.add_line("self.logger = logger")
        self.add_line("self.backup_method = backup_method")
        self.add_line("self.backup_queue = backup_queue")
        self.add_line("self.backup_url = backup_url")
        self.add_line("self.backup_period = backup_period")
        self.add_line("self.backup_delay = backup_delay")
        self.add_line('self.connections = kwargs.get("connections", [])')
        self.add_line('self.msgRCount = self.limit_number(kwargs.get("msgRCount", 0))')
        self.add_line('self.msgSCount = self.limit_number(kwargs.get("msgSCount", 0))')

        for init_float_param in agent.init_floats.values():
            name = init_float_param.name
            value = init_float_param.value
            self.add_line(
                f'self.{name} = self.limit_number(kwargs.get("{name}", {value}))'
            )

        for dist_normal_float_param in agent.dist_normal_floats.values():
            name = dist_normal_float_param.name
            mean = f"self.limit_number({dist_normal_float_param.mean})"
            std_dev = f"self.limit_number({dist_normal_float_param.std_dev})"
            self.add_line(
                f'self.{name} = self.limit_number(kwargs.get("{name}", numpy.random.normal({mean}, {std_dev})))',
                {"numpy"},
            )

        for dist_exp_float_param in agent.dist_exp_floats.values():
            name = dist_exp_float_param.name
            lambda_ = f"self.limit_number({dist_exp_float_param.lambda_})"
            self.add_line(
                f'self.{name} = self.limit_number(kwargs.get("{name}", numpy.random.exponential(self.limit_number(1 / {lambda_}))))',
                {"numpy"},
            )

        for dist_uniform_float_param in agent.dist_unifrom_floats.values():
            name = dist_uniform_float_param.name
            a = f"self.limit_number({dist_uniform_float_param.a})"
            b = f"self.limit_number({dist_uniform_float_param.b})"
            self.add_line(
                f'self.{name} = self.limit_number(kwargs.get("{name}", random.uniform({a}, {b})))',
                {"random"},
            )

        for enum_param in agent.enums.values():
            value_list: List[str] = []
            percentage_list: List[str] = []
            for enum_value in enum_param.enum_values:
                value_list.append(f'"{enum_value.value}"')
                percentage_list.append(enum_value.percentage)
            values = f'[{", ".join(value_list)}]'
            percentages = f'[{", ".join(percentage_list)}]'
            self.add_line(
                f'self.{enum_param.name} = kwargs.get("{enum_param.name}", random.choices({values}, {percentages})[0])',
                {"random"},
            )

        for connection_list_param in agent.connection_lists.values():
            self.add_line(
                f'self.{connection_list_param.name} = kwargs.get("{connection_list_param.name}", [])'
            )

        for message_list_param in agent.message_lists.values():
            self.add_line(
                f'self.{message_list_param.name} = kwargs.get("{message_list_param.name}", [])'
            )

        for float_list_param in agent.float_lists.values():
            self.add_line(
                f'self.{float_list_param.name} = kwargs.get("{float_list_param.name}", [])'
            )

        for mod_var_param in agent.module_variables.values():
            self.add_line(f"self.{mod_var_param.name} = {mod_var_param.init_function}")

        self.add_line(
            "if self.logger: self.logger.debug(f'[{self.jid}] Class dict after initialization: {self.__dict__}')"
        )

        self.indent_left()
        self.add_newline()

        self.add_line("@property")
        self.add_line("def connCount(self):")
        self.indent_right()
        self.add_line("return self.limit_number(len(self.connections))")

        self.indent_left()

    def add_float_utils(self) -> None:
        self.add_line("def limit_number(self, value):")
        self.indent_right()
        self.add_line("return float(max(-2147483648, min(value, 2147483647)))")
        self.indent_left()

    def add_message_utils(self) -> None:
        self.add_line("def get_json_from_spade_message(self, msg):")
        self.indent_right()
        self.add_line("return orjson.loads(msg.body)", {"orjson"})
        self.indent_left()
        self.add_newline()

        self.add_line("def get_spade_message(self, receiver_jid, body):")
        self.indent_right()
        self.add_line("msg = spade.message.Message(to=receiver_jid)", {"spade"})
        self.add_line('body["sender"] = str(self.jid)')
        self.add_line('msg.metadata["type"] = body["type"]')
        self.add_line('msg.metadata["performative"] = body["performative"]')
        self.add_line(
            'msg.body = str(orjson.dumps(body), encoding="utf-8")', {"orjson"}
        )
        self.add_line("return msg")

        self.indent_left()

    def add_agent_setup(self, agent: Agent) -> None:
        self.add_line("def setup(self):")
        self.indent_right()

        self.add_line("if self.backup_method is not None:")
        self.indent_right()
        self.add_no_match_template("BackupBehaviour")
        self.add_line(
            "self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period), BackupBehaviour_template)",
            {"datetime"},
        )
        self.indent_left()

        for setup_behaviour in agent.setup_behaviours.values():
            self.add_no_match_template(f"{setup_behaviour.name}")
            self.add_line(
                f"self.add_behaviour(self.{setup_behaviour.name}(), {setup_behaviour.name}_template)"
            )

        for one_time_behaviour in agent.one_time_behaviours.values():
            self.add_no_match_template(f"{one_time_behaviour.name}")
            self.add_line(
                f"self.add_behaviour(self.{one_time_behaviour.name}(start_at=datetime.datetime.now() + datetime.timedelta(seconds={one_time_behaviour.delay})), {one_time_behaviour.name}_template)",
                {"datetime"},
            )

        for cyclic_behaviour in agent.cyclic_behaviours.values():
            self.add_no_match_template(f"{cyclic_behaviour.name}")
            self.add_line(
                f"self.add_behaviour(self.{cyclic_behaviour.name}(period={cyclic_behaviour.period}), {cyclic_behaviour.name}_template)"
            )

        for message_received_behaviour in agent.message_received_behaviours.values():
            self.add_line(
                f"{message_received_behaviour.name}_template = spade.template.Template()",
                {"spade"},
            )
            self.add_line(
                f'{message_received_behaviour.name}_template.set_metadata("type", "{message_received_behaviour.received_message.type}")'
            )
            self.add_line(
                f'{message_received_behaviour.name}_template.set_metadata("performative", "{message_received_behaviour.received_message.performative}")'
            )
            self.add_line(
                f"self.add_behaviour(self.{message_received_behaviour.name}(), {message_received_behaviour.name}_template)"
            )

        self.add_line(
            "if self.logger: self.logger.debug(f'[{self.jid}] Class dict after setup: {self.__dict__}')"
        )

        self.indent_left()

    def add_no_match_template(self, behaviour_name: str) -> None:
        self.add_line(
            f"{behaviour_name}_template = spade.template.Template()", {"spade"}
        )
        self.add_line(
            f'{behaviour_name}_template.set_metadata("reserved", "no_message_match")'
        )

    def add_backup_behaviour(self, agent: Agent) -> None:
        self.add_line(
            "class BackupBehaviour(spade.behaviour.PeriodicBehaviour):", {"spade"}
        )
        self.indent_right()
        self.add_line("def __init__(self, start_at, period):")
        self.indent_right()
        self.add_line("super().__init__(start_at=start_at, period=period)")
        self.add_line("self.http_client = httpx.AsyncClient(timeout=period)", {"httpx"})
        self.indent_left()
        self.add_newline()

        self.add_line("async def run(self):")
        self.indent_right()
        self.add_line("data = {")
        self.indent_right()
        self.add_line(
            '"__timestamp__": int(datetime.datetime.timestamp(datetime.datetime.utcnow())),',
            {"datetime"},
        )
        self.add_line('"jid": str(self.agent.jid),')
        self.add_line(f'"type": "{agent.name}",')

        self.add_line('"floats": {')
        self.indent_right()
        self.add_line('"msgRCount": self.agent.msgRCount,')
        self.add_line('"msgSCount": self.agent.msgSCount,')
        self.add_line('"connCount": self.agent.connCount,')
        for float_param_name in agent.float_param_names:
            self.add_line(f'"{float_param_name}": self.agent.{float_param_name},')
        self.indent_left()
        self.add_line("},")

        self.add_line('"enums": {')
        self.indent_right()
        for enum_param_name in agent.enums:
            self.add_line(f'"{enum_param_name}": self.agent.{enum_param_name},')
        self.indent_left()
        self.add_line("},")

        self.add_line('"connections": {')
        self.indent_right()
        self.add_line('"connections": self.agent.connections,')
        for connection_list_param_name in agent.connection_lists:
            self.add_line(
                f'"{connection_list_param_name}": self.agent.{connection_list_param_name},'
            )
        self.indent_left()
        self.add_line("},")

        self.add_line('"messages": {')
        self.indent_right()
        for message_list_param_name in agent.message_lists:
            self.add_line(
                f'"{message_list_param_name}": self.agent.{message_list_param_name},'
            )
        self.indent_left()
        self.add_line("},")

        self.add_line('"float_lists": {')
        self.indent_right()
        for float_list_param_name in agent.float_lists:
            self.add_line(
                f'"{float_list_param_name}": self.agent.{float_list_param_name},'
            )
        self.indent_left()
        self.add_line("},")
        self.add_line('"module_variables": {')
        self.indent_right()
        for module_variable_name in agent.module_variables:
            self.add_line(
                f'"{module_variable_name}": self.agent.{module_variable_name},'
            )
        self.indent_left()
        self.add_line("},")
        self.indent_left()
        self.add_line("}")

        self.add_line("if self.agent.backup_method == 'http':")
        self.indent_right()
        self.add_line(
            "if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data with http: {data}')"
        )
        self.add_line("try:")
        self.indent_right()
        self.add_line(
            'await self.http_client.post(self.agent.backup_url, headers={"Content-Type": "application/json"}, data=orjson.dumps(data))',
            {"orjson"},
        )
        self.indent_left()
        self.add_line("except Exception as e:")
        self.indent_right()
        self.add_line(
            "if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')"
        )
        self.indent_left()
        self.indent_left()
        self.add_line("elif self.agent.backup_method == 'queue':")
        self.indent_right()
        self.add_line(
            "if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data with queue: {data}')"
        )
        self.add_line("try:")
        self.indent_right()
        self.add_line("await self.agent.backup_queue.coro_put(data)")
        self.indent_left()
        self.add_line("except Exception as e:")
        self.indent_right()
        self.add_line(
            "if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')"
        )
        self.indent_left()
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line(
            "if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Unknown backup method: {self.agent.backup_method}')"
        )
        self.indent_left()
        self.indent_left()
        self.indent_left()

    def add_agent_behaviour(self, behaviour: Behaviour, behaviour_type: str) -> None:
        self.add_line(f"class {behaviour.name}({behaviour_type}):", {"spade"})
        self.indent_right()

        for action in behaviour.actions.values():
            self.add_action(behaviour, action)

        self.add_line("async def run(self):")
        self.indent_right()
        if isinstance(behaviour, MessageReceivedBehaviour):
            self.add_rcv_message()
        elif not behaviour.actions.values():
            self.add_line("...")
            self.indent_left()
            self.indent_left()
            return

        if isinstance(behaviour, MessageReceivedBehaviour):
            self.indent_right()

        for action in behaviour.actions.values():
            self.add_action_call(behaviour, action)

        if isinstance(behaviour, MessageReceivedBehaviour):
            self.indent_left()

        self.indent_left()
        self.indent_left()

    def add_rcv_message(self) -> None:
        self.add_line("rcv = await self.receive(timeout=100000)")
        self.add_line("if rcv:")
        self.indent_right()
        self.add_line("rcv = self.agent.get_json_from_spade_message(rcv)")
        self.add_line(
            "self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)"
        )
        self.add_line(
            "if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')"
        )
        self.indent_left()

    def add_action_call(self, behaviour: Behaviour, action: Action) -> None:
        action_call = ""
        if isinstance(action, SendMessageAction):
            action_call += "await "
        action_call += f"self.{action.name}"
        if isinstance(behaviour, MessageReceivedBehaviour):
            action_call += "(rcv)"
        else:
            action_call += "()"
        self.add_line(action_call)

    def add_action(self, behaviour: Behaviour, action: Action) -> None:
        self.add_action_def(behaviour, action)
        self.indent_right()

        self.add_line(
            f"if self.agent.logger: self.agent.logger.debug(f'[{{self.agent.jid}}] Run action {action.name}')"
        )

        if isinstance(action, SendMessageAction):
            self.add_send_message(action.send_message)

        self.add_block(action.main_block)
        self.indent_left()

        self.add_newline()

    def add_action_def(self, behaviour: Behaviour, action: Action) -> None:
        action_def = ""
        if isinstance(action, SendMessageAction):
            action_def += "async "
        action_def += f"def {action.name}"
        if isinstance(behaviour, MessageReceivedBehaviour):
            action_def += "(self, rcv):"
        else:
            action_def += "(self):"
        self.add_line(action_def)

    def add_send_message(self, message: IntermediateMessage) -> None:
        send_msg = f'send = {{ "type": "{message.type}", "performative": "{message.performative}", '
        for float_param_name in message.float_params:
            send_msg += f'"{float_param_name}": 0.0, '
        for connection_param_name in message.connection_params:
            send_msg += f'"{connection_param_name}": "", '
        for name, modvar_param in message.module_variable_params.items():
            send_msg += f'"{name}": {modvar_param.init_function}, '
        send_msg += "}"
        self.add_line(send_msg)

    def parse_arg(self, arg: Argument) -> str:
        match arg.type_in_op:
            case AgentParam():
                if arg.expr == "self":
                    return "self.agent.jid"
                else:
                    return f"self.agent.{arg.expr}"

            case EnumValue():
                return f'"{arg.expr}"'

            case ReceivedMessageParam():
                prop = arg.expr.split(".")[1]
                return f'rcv["{prop}"]'

            case SendMessageParam():
                prop = arg.expr.split(".")[1]
                return f'send["{prop}"]'

            case _:
                return arg.expr

    def add_block(self, block: Block) -> None:
        if not block.statements:
            self.add_line("...")
            return

        for statement in block.statements:
            match statement:
                case Block():
                    self.indent_right()
                    self.add_block(statement)
                    self.indent_left()

                case FloatDeclaration():
                    self.add_line("")
                    self.add_line("# float declaration")
                    value = (
                        f"self.agent.limit_number({self.parse_arg(statement.value)})"
                    )
                    self.add_line(f"{statement.name} = {value}")

                case ConnectionDeclaration():
                    self.add_line("")
                    self.add_line("# connection declaration")
                    value = f"{self.parse_arg(statement.value)}"
                    self.add_line(f"{statement.name} = {value}")

                case ModuleVariableDeclaration():
                    self.add_line("")
                    self.add_line("# module variable declaration")
                    self.add_line(f"{statement.name} = {statement.init_function}")

                case Subset():
                    self.add_line("")
                    self.add_line("# subset")
                    dst_list = self.parse_arg(statement.dst_list)
                    src_list = self.parse_arg(statement.src_list)
                    src_list_len = f"int(self.agent.limit_number(len({src_list})))"
                    num = f"int(self.agent.limit_number(round(self.agent.limit_number({self.parse_arg(statement.num)}))))"
                    self.add_line(f"if {num} <= 0:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.debug(f'[{{self.agent.jid}}] Non-positive subset size (rounded): \u007b{num}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(
                        f"{dst_list} = [copy.deepcopy(elem) for elem in random.sample({src_list}, min({num}, {src_list_len}))]",
                        {"copy", "random"},
                    )

                case Clear():
                    self.add_line("")
                    self.add_line("# clear")
                    list_ = self.parse_arg(statement.list_)
                    self.add_line(f"{list_}.clear()")

                case Send() if isinstance(statement.receivers.type_in_op, Connection):
                    self.add_line("")
                    self.add_line("# send")
                    receiver = self.parse_arg(statement.receivers)
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.debug(f'[{{self.agent.jid}}] Send message {{send}} to \u007b{receiver}\u007d')"
                    )
                    self.add_line(
                        f"await self.send(self.agent.get_spade_message({receiver}, send))"
                    )
                    self.add_line(
                        "self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)"
                    )

                case Send() if isinstance(
                    statement.receivers.type_in_op, ConnectionList
                ):
                    self.add_line("")
                    self.add_line("# send")
                    receivers = self.parse_arg(statement.receivers)
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.debug(f'[{{self.agent.jid}}] Send message {{send}} to \u007b{receivers}\u007d')"
                    )
                    self.add_line(f"for receiver in {receivers}:")
                    self.indent_right()
                    self.add_line(
                        "await self.send(self.agent.get_spade_message(receiver, send))"
                    )
                    self.add_line(
                        "self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)"
                    )
                    self.indent_left()

                case Set() if isinstance(statement.value.type_in_op, MessageList):
                    self.add_line("")
                    self.add_line("# set")
                    msg = self.parse_arg(statement.dst)
                    msg_list = self.parse_arg(statement.value)
                    self.add_line(
                        f'if not any([msg["type"] == {msg}["type"] and msg["performative"] == {msg}["performative"] for msg in {msg_list}]):'
                    )
                    self.indent_right()
                    self.add_line(
                        f'if self.agent.logger: self.agent.logger.warning(f\'[{{self.agent.jid}}] No messages with type/performative \u007b{msg}["type"]\u007d/\u007b{msg}["performative"]\u007d found in list {msg_list}\')'
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(
                        f'{msg} = copy.deepcopy(random.choice(list(filter(lambda msg: msg["type"] == {msg}["type"] and msg["performative"] == {msg}["performative"], {msg_list}))))',
                        {"copy", "random"},
                    )

                case Set() if isinstance(statement.value.type_in_op, Float):
                    self.add_line("")
                    self.add_line("# set")
                    dst = self.parse_arg(statement.dst)
                    num = f"self.agent.limit_number({self.parse_arg(statement.value)})"
                    self.add_line(f"{dst} = {num}")

                case Set():
                    self.add_line("")
                    self.add_line("# set")
                    dst = self.parse_arg(statement.dst)
                    value = self.parse_arg(statement.value)
                    self.add_line(f"{dst} = {value}")

                case Round():
                    self.add_line("")
                    self.add_line("# round")
                    dst = self.parse_arg(statement.dst)
                    self.add_line(
                        f"{dst} = self.agent.limit_number(round(self.agent.limit_number({dst})))"
                    )

                case UniformDist():
                    self.add_line("")
                    self.add_line("# uniform distribution")
                    dst = self.parse_arg(statement.dst)
                    a = f"self.agent.limit_number({self.parse_arg(statement.a)})"
                    b = f"self.agent.limit_number({self.parse_arg(statement.b)})"
                    self.add_line(
                        f"{dst} = self.agent.limit_number(random.uniform({a}, {b}))",
                        {"random"},
                    )

                case NormalDist():
                    self.add_line("")
                    self.add_line("# normal distribution")
                    dst = self.parse_arg(statement.dst)
                    mean = f"self.agent.limit_number({self.parse_arg(statement.mean)})"
                    std_dev = (
                        f"self.agent.limit_number({self.parse_arg(statement.std_dev)})"
                    )
                    self.add_line(f"if {std_dev} < 0:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Negative standard deviation: \u007b{std_dev}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(
                        f"{dst} = self.agent.limit_number(numpy.random.normal({mean}, {std_dev}))",
                        {"numpy"},
                    )

                case ExpDist():
                    self.add_line("")
                    self.add_line("# exponential distribution")
                    dst = self.parse_arg(statement.dst)
                    lambda_ = (
                        f"self.agent.limit_number({self.parse_arg(statement.lambda_)})"
                    )
                    self.add_line(f"if {lambda_} <= 0:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Non-positive lambda: \u007b{lambda_}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(
                        f"{dst} = self.agent.limit_number(numpy.random.exponential(self.agent.limit_number(1 / {lambda_})))",
                        {"numpy"},
                    )

                case Comparaison():
                    if isinstance(statement.left.type_in_op, Float):
                        left = (
                            f"self.agent.limit_number({self.parse_arg(statement.left)})"
                        )
                    else:
                        left = self.parse_arg(statement.left)

                    if isinstance(statement.right.type_in_op, Float):
                        right = f"self.agent.limit_number({self.parse_arg(statement.right)})"
                    else:
                        right = self.parse_arg(statement.right)

                    match statement:
                        case IfGreaterThan():
                            self.add_line("")
                            self.add_line("# if greater than")
                            self.add_line(f"if {left} > {right}:")

                        case IfGreaterThanOrEqual():
                            self.add_line("")
                            self.add_line("# if greater than or equal")
                            self.add_line(f"if {left} >= {right}:")

                        case IfLessThan():
                            self.add_line("")
                            self.add_line("# if less than")
                            self.add_line(f"if {left} < {right}:")

                        case IfLessThanOrEqual():
                            self.add_line("")
                            self.add_line("# if greater than or equal")
                            self.add_line(f"if {left} <= {right}:")

                        case IfEqual():
                            self.add_line("")
                            self.add_line("# if equal")
                            self.add_line(f"if {left} == {right}:")

                        case IfNotEqual():
                            self.add_line("")
                            self.add_line("# if not equal")
                            self.add_line(f"if {left} != {right}:")

                        case WhileGreaterThan():
                            self.add_line("")
                            self.add_line("# while greater than")
                            self.add_line(f"while {left} > {right}:")

                        case WhileGreaterThanOrEqual():
                            self.add_line("")
                            self.add_line("# while greater than or equal")
                            self.add_line(f"while {left} >= {right}:")

                        case WhileLessThan():
                            self.add_line("")
                            self.add_line("# while less than")
                            self.add_line(f"while {left} < {right}:")

                        case WhileLessThanOrEqual():
                            self.add_line("")
                            self.add_line("# while less than or equal")
                            self.add_line(f"while {left} <= {right}:")

                        case WhileEqual():
                            self.add_line("")
                            self.add_line("# while equal")
                            self.add_line(f"while {left} == {right}:")

                        case WhileNotEqual():
                            self.add_line("")
                            self.add_line("# while not equal")
                            self.add_line(f"while {left} != {right}:")

                        case _:
                            raise Exception(
                                f"Unknown comparaison statement: {statement.print()}"
                            )

                case MathOperation():
                    dst = self.parse_arg(statement.dst)
                    num = f"self.agent.limit_number({self.parse_arg(statement.num)})"
                    match statement:
                        case Add():
                            self.add_line("")
                            self.add_line("# add")
                            self.add_line(
                                f"{dst} = self.agent.limit_number({dst} + {num})"
                            )

                        case Subtract():
                            self.add_line("")
                            self.add_line("# subtract")
                            self.add_line(
                                f"{dst} = self.agent.limit_number({dst} - {num})"
                            )

                        case Multiply():
                            self.add_line("")
                            self.add_line("# multiply")
                            self.add_line(
                                f"{dst} = self.agent.limit_number({dst} * {num})"
                            )

                        case Divide():
                            self.add_line("")
                            self.add_line("# divide")
                            self.add_line(f"if {num} == 0:")
                            self.indent_right()
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Division by zero: \u007b{num}\u007d')"
                            )
                            self.add_line("return")
                            self.indent_left()
                            self.add_line(
                                f"{dst} = self.agent.limit_number({dst} / {num})"
                            )

                        case _:
                            raise Exception(
                                f"Unknown math operation statement: {statement.print()}"
                            )

                case Modulo():
                    dst = self.parse_arg(statement.dst)
                    dividend = (
                        f"self.agent.limit_number({self.parse_arg(statement.dividend)})"
                    )
                    divisor = (
                        f"self.agent.limit_number({self.parse_arg(statement.divisor)})"
                    )
                    self.add_line("")
                    self.add_line("# modulo")
                    self.add_line(f"if {divisor} == 0:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Modulo division by zero: \u007b{divisor}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(
                        f"{dst} = self.agent.limit_number({dividend} % {divisor})"
                    )

                case ListElementAccess():
                    list_ = self.parse_arg(statement.list_)
                    element = self.parse_arg(statement.element)
                    match statement:
                        case AddElement() if isinstance(
                            statement.element.type_in_op, MessageList
                        ):
                            self.add_line("")
                            self.add_line("# add element")
                            self.add_line(
                                f"if {element} not in {list_}: {list_}.append({element})"
                            )

                        case AddElement():
                            self.add_line("")
                            self.add_line("# add element")
                            self.add_line(f"{list_}.append({element})")

                        case RemoveElement():
                            self.add_line("")
                            self.add_line("# remove element")
                            self.add_line(
                                f"if {element} in {list_}: {list_}.remove({element})"
                            )

                        case IfInList():
                            self.add_line("")
                            self.add_line("# if in list")
                            self.add_line(f"if {element} in {list_}:")

                        case IfNotInList():
                            self.add_line("")
                            self.add_line("# if not in list")
                            self.add_line(f"if {element} not in {list_}:")

                        case _:
                            raise Exception(
                                f"Unknown list element access statement: {statement.print()}"
                            )

                case RemoveNElements():
                    self.add_line("")
                    self.add_line("# remove n elements")
                    list_ = self.parse_arg(statement.list_)
                    list_len = f"int(self.agent.limit_number(len({list_})))"
                    num = f"int(self.agent.limit_number(round(self.agent.limit_number({self.parse_arg(statement.num)}))))"
                    self.add_line(f"if {num} < 0 or {num} > {list_len}:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.debug(f'[{{self.agent.jid}}] Incorrect number of elements to remove (rounded, either negative or bigger than the list size): \u007b{num}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(f"random.shuffle({list_})", {"random"})
                    self.add_line(
                        f"{list_} = {list_}[:int(self.agent.limit_number({list_len} - {num}))]"
                    )

                case Length():
                    self.add_line("")
                    self.add_line("# length")
                    dst = self.parse_arg(statement.dst)
                    list_ = self.parse_arg(statement.list_)
                    self.add_line(f"{dst} = self.agent.limit_number(len({list_}))")

                case ListRead():
                    self.add_line("")
                    self.add_line("# list read")
                    dst = self.parse_arg(statement.dst)
                    list_ = self.parse_arg(statement.list_)
                    idx = f"int(self.agent.limit_number(round(self.agent.limit_number({self.parse_arg(statement.idx)}))))"
                    match statement.list_.type_in_op:
                        case FloatList():
                            value = f"self.agent.limit_number({list_}[{idx}])"
                        case _:
                            value = f"{list_}[{idx}]"
                    list_len = f"int(self.agent.limit_number(len({list_})))"
                    self.add_line(f"if {idx} < 0 or {idx} >= {list_len}:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Incorrect index (rounded, either negative or bigger than the list size): \u007b{idx}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(f"{dst} = {value}")

                case ListWrite():
                    self.add_line("")
                    self.add_line("# list write")
                    list_ = self.parse_arg(statement.list_)
                    idx = f"int(self.agent.limit_number(round(self.agent.limit_number({self.parse_arg(statement.idx)}))))"
                    match statement.value.type_in_op:
                        case Float():
                            value = f"self.agent.limit_number({self.parse_arg(statement.value)})"
                        case _:
                            value = self.parse_arg(statement.value)
                    dst = f"{list_}[{idx}]"
                    list_len = f"int(self.agent.limit_number(len({list_})))"
                    self.add_line(f"if {idx} < 0 or {idx} >= {list_len}:")
                    self.indent_right()
                    self.add_line(
                        f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Incorrect index (rounded, either negative or bigger than the list size): \u007b{idx}\u007d')"
                    )
                    self.add_line("return")
                    self.indent_left()
                    self.add_line(f"{dst} = {value}")

                case TrigonometryOperation():
                    dst = self.parse_arg(statement.dst)
                    degree = (
                        f"self.agent.limit_number({self.parse_arg(statement.degree)})"
                    )

                    match statement:
                        case Sin():
                            self.add_line("")
                            self.add_line("# sin")
                            self.add_line(
                                f"{dst} = self.agent.limit_number(numpy.sin(numpy.deg2rad({degree})))",
                                {"numpy"},
                            )

                        case Cos():
                            self.add_line("")
                            self.add_line("# cos")
                            self.add_line(
                                f"{dst} = self.agent.limit_number(numpy.cos(numpy.deg2rad({degree})))",
                                {"numpy"},
                            )

                        case _:
                            raise Exception(
                                f"Unknown trigonometry operation statement: {statement.print()}"
                            )

                case ExponentiationOperation():
                    dst = self.parse_arg(statement.dst)
                    base = f"self.agent.limit_number({self.parse_arg(statement.base)})"
                    num = f"self.agent.limit_number({self.parse_arg(statement.num)})"

                    match statement:
                        case Power():
                            self.add_line("")
                            self.add_line("# power")
                            self.add_line(
                                f"{dst} = self.agent.limit_number(numpy.power({base}, {num}))",
                                {"numpy"},
                            )

                        case Logarithm():
                            self.add_line("")
                            self.add_line("# logarithm")
                            self.add_line(
                                f"if {base} <= 0 or {num} <= 0 or {base} == 1:"
                            )
                            self.indent_right()
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.warning(f'[{{self.agent.jid}}] Incorrect logarithm arguments: log(\u007b{base}\u007d, \u007b{num}\u007d')"
                            )
                            self.add_line("return")
                            self.indent_left()
                            numerator = f"self.agent.limit_number(numpy.log({num}))"
                            denominator = f"self.agent.limit_number(numpy.log({base}))"
                            self.add_line(
                                f"{dst} = self.agent.limit_number({numerator} / {denominator})",
                                {"numpy"},
                            )

                        case _:
                            raise Exception(
                                f"Unknown exponentiation operation statement: {statement.print()}"
                            )

                case Logs():
                    logger_msg = '{ "jid": self.agent.jid, "agent": type(self.agent).__name__, "behaviour": type(self).__name__, "action": inspect.stack()[0].function'
                    for arg in statement.args:
                        name = arg.expr + "__" + arg.explain_type_in_op()
                        value = self.parse_arg(arg)
                        logger_msg += f', "{name}": {value}'
                    logger_msg += " }"

                    match statement:
                        case LogsDebug():
                            self.add_line("")
                            self.add_line("# logs (debug)")
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.debug({logger_msg})",
                                {"inspect"},
                            )

                        case LogsInfo():
                            self.add_line("")
                            self.add_line("# logs (info)")
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.info({logger_msg})",
                                {"inspect"},
                            )

                        case LogsWarning():
                            self.add_line("")
                            self.add_line("# logs (warning)")
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.warning({logger_msg})",
                                {"inspect"},
                            )

                        case LogsError():
                            self.add_line("")
                            self.add_line("# logs (error)")
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.error({logger_msg})",
                                {"inspect"},
                            )

                        case LogsCritical():
                            self.add_line("")
                            self.add_line("# logs (critical)")
                            self.add_line(
                                f"if self.agent.logger: self.agent.logger.critical({logger_msg})",
                                {"inspect"},
                            )

                        case _:
                            raise Exception(
                                f"Unknown logs statement: {statement.print()}"
                            )
                case ModuleInstruction():
                    self.add_line("")
                    self.add_line(f"# module instruction {statement.op_code}")
                    arguments_string = ", ".join(
                        [self.parse_arg(arg) for arg in statement.args]
                    )
                    if statement.is_block:
                        self.add_line(
                            # NOTE: there are no while statements in the modules, all blocks are ifs
                            f"if {statement.module}.{statement.op_code}({arguments_string}):"
                        )
                    else:
                        if statement.assignment is None:
                            self.add_line(
                                f"{statement.module}.{statement.op_code}({arguments_string})"
                            )
                        else:
                            self.add_line(
                                f"{self.parse_arg(statement.assignment)} = {statement.module}.{statement.op_code}({arguments_string})"
                            )

                case _:
                    print(statement)
                    raise Exception(f"Unknown statement: {statement.print()}")
