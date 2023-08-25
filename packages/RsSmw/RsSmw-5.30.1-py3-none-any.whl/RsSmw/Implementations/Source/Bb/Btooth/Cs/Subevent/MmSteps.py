from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmStepsCls:
	"""MmSteps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mmSteps", core, parent)

	def get(self, subEventNull=repcap.SubEventNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MMSTeps \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.mmSteps.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: main_mode_steps: integer Range: 2 to 160"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MMSTeps?')
		return Conversions.str_to_int(response)
