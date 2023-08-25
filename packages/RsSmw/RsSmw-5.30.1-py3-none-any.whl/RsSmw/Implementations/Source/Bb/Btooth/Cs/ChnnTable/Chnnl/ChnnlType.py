from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChnnlTypeCls:
	"""ChnnlType commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("chnnlType", core, parent)

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoChnnelType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNtable:[CHNNL<CH0>]:CHNNlType \n
		Snippet: value: enums.BtoChnnelType = driver.source.bb.btooth.cs.chnnTable.chnnl.chnnlType.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Chnnl')
			:return: channel_sounding: ADVertising| DATA| CS"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CHNNtable:CHNNL{channelNull_cmd_val}:CHNNlType?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChnnelType)
