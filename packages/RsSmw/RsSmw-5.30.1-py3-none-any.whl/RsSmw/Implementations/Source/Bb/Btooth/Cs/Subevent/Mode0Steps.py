from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode0StepsCls:
	"""Mode0Steps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode0Steps", core, parent)

	def set(self, mode_0_steps: int, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE0steps \n
		Snippet: driver.source.bb.btooth.cs.subevent.mode0Steps.set(mode_0_steps = 1, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param mode_0_steps: integer Range: 1 to 3
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.decimal_value_to_str(mode_0_steps)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE0steps {param}')

	def get(self, subEventNull=repcap.SubEventNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE0steps \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.mode0Steps.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: mode_0_steps: integer Range: 1 to 3"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE0steps?')
		return Conversions.str_to_int(response)
