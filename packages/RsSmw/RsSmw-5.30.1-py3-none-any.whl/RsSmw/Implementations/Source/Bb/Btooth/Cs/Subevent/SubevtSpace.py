from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubevtSpaceCls:
	"""SubevtSpace commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subevtSpace", core, parent)

	def get(self, subEventNull=repcap.SubEventNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:SUBEvtSpace \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.subevtSpace.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: subevent_space: integer Range: 150 to 65535"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:SUBEvtSpace?')
		return Conversions.str_to_int(response)
