from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EepromCls:
	"""Eeprom commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eeprom", core, parent)

	@property
	def customize(self):
		"""customize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_customize'):
			from .Customize import CustomizeCls
			self._customize = CustomizeCls(self._core, self._cmd_group)
		return self._customize

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	def delete(self) -> None:
		"""SCPI: DIAGnostic<HW>:EEPRom:DELete \n
		Snippet: driver.diagnostic.eeprom.delete() \n
		No command help available \n
		"""
		self._core.io.write(f'DIAGnostic<HwInstance>:EEPRom:DELete')

	def delete_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: DIAGnostic<HW>:EEPRom:DELete \n
		Snippet: driver.diagnostic.eeprom.delete_with_opc() \n
		No command help available \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'DIAGnostic<HwInstance>:EEPRom:DELete', opc_timeout_ms)

	def clone(self) -> 'EepromCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EepromCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
