from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MfCls:
	"""Mf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mf", core, parent)

	def set(self, mf: float, groupNull=repcap.GroupNull.Default, dataNull=repcap.DataNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST0>:MFL:DATA<CH0>:MF \n
		Snippet: driver.source.bb.stereo.grps.gt.mfl.data.mf.set(mf = 1.0, groupNull = repcap.GroupNull.Default, dataNull = repcap.DataNull.Default) \n
		No command help available \n
			:param mf: No help available
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Gt')
			:param dataNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Data')
		"""
		param = Conversions.decimal_value_to_str(mf)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		dataNull_cmd_val = self._cmd_group.get_repcap_cmd_value(dataNull, repcap.DataNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{groupNull_cmd_val}:MFL:DATA{dataNull_cmd_val}:MF {param}')

	def get(self, groupNull=repcap.GroupNull.Default, dataNull=repcap.DataNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST0>:MFL:DATA<CH0>:MF \n
		Snippet: value: float = driver.source.bb.stereo.grps.gt.mfl.data.mf.get(groupNull = repcap.GroupNull.Default, dataNull = repcap.DataNull.Default) \n
		No command help available \n
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Gt')
			:param dataNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Data')
			:return: mf: No help available"""
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		dataNull_cmd_val = self._cmd_group.get_repcap_cmd_value(dataNull, repcap.DataNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{groupNull_cmd_val}:MFL:DATA{dataNull_cmd_val}:MF?')
		return Conversions.str_to_float(response)
