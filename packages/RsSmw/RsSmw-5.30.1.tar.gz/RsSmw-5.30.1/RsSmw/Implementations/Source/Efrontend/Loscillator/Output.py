from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:OUTPut:FREQuency \n
		Snippet: value: float = driver.source.efrontend.loscillator.output.get_frequency() \n
		No command help available \n
			:return: output_frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:LOSCillator:OUTPut:FREQuency?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:OUTPut:STATe \n
		Snippet: value: bool = driver.source.efrontend.loscillator.output.get_state() \n
		No command help available \n
			:return: out_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:LOSCillator:OUTPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, out_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:LOSCillator:OUTPut:STATe \n
		Snippet: driver.source.efrontend.loscillator.output.set_state(out_state = False) \n
		No command help available \n
			:param out_state: No help available
		"""
		param = Conversions.bool_to_str(out_state)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:LOSCillator:OUTPut:STATe {param}')
