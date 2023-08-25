from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode2NapCls:
	"""Mode2Nap commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode2Nap", core, parent)

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsNap:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE2Nap \n
		Snippet: value: enums.BtoCsNap = driver.source.bb.btooth.cs.subevent.mode2Nap.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: nap: NAP_1| NAP_2| NAP_3| NAP_4"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE2Nap?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsNap)
