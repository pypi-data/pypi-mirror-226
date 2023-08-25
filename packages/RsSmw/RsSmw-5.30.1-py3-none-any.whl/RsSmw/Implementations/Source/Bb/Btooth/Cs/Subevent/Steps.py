from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepsCls:
	"""Steps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("steps", core, parent)

	def set(self, num_of_steps: int, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:STEPs \n
		Snippet: driver.source.bb.btooth.cs.subevent.steps.set(num_of_steps = 1, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param num_of_steps: integer Range: 2 to 160
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.decimal_value_to_str(num_of_steps)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEPs {param}')

	def get(self, subEventNull=repcap.SubEventNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:STEPs \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.steps.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: num_of_steps: integer Range: 2 to 160"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEPs?')
		return Conversions.str_to_int(response)
