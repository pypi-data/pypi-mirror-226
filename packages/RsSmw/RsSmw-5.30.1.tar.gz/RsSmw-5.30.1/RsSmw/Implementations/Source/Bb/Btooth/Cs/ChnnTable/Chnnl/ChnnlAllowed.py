from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChnnlAllowedCls:
	"""ChnnlAllowed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("chnnlAllowed", core, parent)

	def set(self, channel_allowed: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNtable:[CHNNL<CH0>]:CHNNlAllowed \n
		Snippet: driver.source.bb.btooth.cs.chnnTable.chnnl.chnnlAllowed.set(channel_allowed = False, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channel_allowed: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Chnnl')
		"""
		param = Conversions.bool_to_str(channel_allowed)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CHNNtable:CHNNL{channelNull_cmd_val}:CHNNlAllowed {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNtable:[CHNNL<CH0>]:CHNNlAllowed \n
		Snippet: value: bool = driver.source.bb.btooth.cs.chnnTable.chnnl.chnnlAllowed.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Chnnl')
			:return: channel_allowed: ADVertising| DATA| CS"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CHNNtable:CHNNL{channelNull_cmd_val}:CHNNlAllowed?')
		return Conversions.str_to_bool(response)
