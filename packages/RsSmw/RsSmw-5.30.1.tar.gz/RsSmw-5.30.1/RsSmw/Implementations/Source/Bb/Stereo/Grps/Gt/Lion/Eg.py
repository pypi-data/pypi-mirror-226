from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EgCls:
	"""Eg commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eg", core, parent)

	def set(self, eg: bool, groupNull=repcap.GroupNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST0>:LION:EG \n
		Snippet: driver.source.bb.stereo.grps.gt.lion.eg.set(eg = False, groupNull = repcap.GroupNull.Default) \n
		No command help available \n
			:param eg: No help available
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Gt')
		"""
		param = Conversions.bool_to_str(eg)
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{groupNull_cmd_val}:LION:EG {param}')

	def get(self, groupNull=repcap.GroupNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST0>:LION:EG \n
		Snippet: value: bool = driver.source.bb.stereo.grps.gt.lion.eg.get(groupNull = repcap.GroupNull.Default) \n
		No command help available \n
			:param groupNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Gt')
			:return: eg: No help available"""
		groupNull_cmd_val = self._cmd_group.get_repcap_cmd_value(groupNull, repcap.GroupNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{groupNull_cmd_val}:LION:EG?')
		return Conversions.str_to_bool(response)
