from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCntrFreqCls:
	"""CsCntrFreq commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csCntrFreq", core, parent)

	def get(self, channelNull=repcap.ChannelNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNtable:[CHNNL<CH0>]:CSCNtrFreq \n
		Snippet: value: float = driver.source.bb.btooth.cs.chnnTable.chnnl.csCntrFreq.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Chnnl')
			:return: cs_cntr_freq: float Range: 2402 to 2480"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CHNNtable:CHNNL{channelNull_cmd_val}:CSCNtrFreq?')
		return Conversions.str_to_float(response)
