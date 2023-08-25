from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmMaxStepsCls:
	"""MmMaxSteps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mmMaxSteps", core, parent)

	def set(self, main_mode_max_step: int, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MMMAxsteps \n
		Snippet: driver.source.bb.btooth.cs.subevent.mmMaxSteps.set(main_mode_max_step = 1, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param main_mode_max_step: integer Range: 2 to 255
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.decimal_value_to_str(main_mode_max_step)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MMMAxsteps {param}')

	def get(self, subEventNull=repcap.SubEventNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MMMAxsteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.mmMaxSteps.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: main_mode_max_step: integer Range: 2 to 255"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MMMAxsteps?')
		return Conversions.str_to_int(response)
