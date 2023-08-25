from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode2TswCls:
	"""Mode2Tsw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode2Tsw", core, parent)

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsTsw:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE2Tsw \n
		Snippet: value: enums.BtoCsTsw = driver.source.bb.btooth.cs.subevent.mode2Tsw.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: tsw: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE2Tsw?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTsw)
