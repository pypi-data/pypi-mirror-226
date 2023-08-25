from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SidxCls:
	"""Sidx commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sidx", core, parent)

	def get_interval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:RESTart:SIDX:INTerval \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.restart.sidx.get_interval() \n
		No command help available \n
			:return: res_slot_idx_int: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:SIDX:INTerval?')
		return Conversions.str_to_int(response)

	def set_interval(self, res_slot_idx_int: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:RESTart:SIDX:INTerval \n
		Snippet: driver.source.bb.nr5G.ubwp.restart.sidx.set_interval(res_slot_idx_int = 1) \n
		No command help available \n
			:param res_slot_idx_int: No help available
		"""
		param = Conversions.decimal_value_to_str(res_slot_idx_int)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:SIDX:INTerval {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:RESTart:SIDX:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.restart.sidx.get_state() \n
		No command help available \n
			:return: restart_slot_idx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:SIDX:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, restart_slot_idx: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:RESTart:SIDX:STATe \n
		Snippet: driver.source.bb.nr5G.ubwp.restart.sidx.set_state(restart_slot_idx = False) \n
		No command help available \n
			:param restart_slot_idx: No help available
		"""
		param = Conversions.bool_to_str(restart_slot_idx)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:SIDX:STATe {param}')
