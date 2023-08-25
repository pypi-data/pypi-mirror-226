from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BlockCls:
	"""Block commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: FmBlock, default value after init: FmBlock.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("block", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_fmBlock_get', 'repcap_fmBlock_set', repcap.FmBlock.Nr1)

	def repcap_fmBlock_set(self, fmBlock: repcap.FmBlock) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FmBlock.Default
		Default value after init: FmBlock.Nr1"""
		self._cmd_group.set_repcap_enum_value(fmBlock)

	def repcap_fmBlock_get(self) -> repcap.FmBlock:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, block: int, dataNull=repcap.DataNull.Default, fmBlock=repcap.FmBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GHEX:DATA<CH0>:BLOCk<ST> \n
		Snippet: driver.source.bb.stereo.ghex.data.block.set(block = 1, dataNull = repcap.DataNull.Default, fmBlock = repcap.FmBlock.Default) \n
		No command help available \n
			:param block: No help available
			:param dataNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Data')
			:param fmBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
		"""
		param = Conversions.decimal_value_to_str(block)
		dataNull_cmd_val = self._cmd_group.get_repcap_cmd_value(dataNull, repcap.DataNull)
		fmBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(fmBlock, repcap.FmBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GHEX:DATA{dataNull_cmd_val}:BLOCk{fmBlock_cmd_val} {param}')

	def get(self, dataNull=repcap.DataNull.Default, fmBlock=repcap.FmBlock.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GHEX:DATA<CH0>:BLOCk<ST> \n
		Snippet: value: int = driver.source.bb.stereo.ghex.data.block.get(dataNull = repcap.DataNull.Default, fmBlock = repcap.FmBlock.Default) \n
		No command help available \n
			:param dataNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Data')
			:param fmBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: block: No help available"""
		dataNull_cmd_val = self._cmd_group.get_repcap_cmd_value(dataNull, repcap.DataNull)
		fmBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(fmBlock, repcap.FmBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GHEX:DATA{dataNull_cmd_val}:BLOCk{fmBlock_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'BlockCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BlockCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
