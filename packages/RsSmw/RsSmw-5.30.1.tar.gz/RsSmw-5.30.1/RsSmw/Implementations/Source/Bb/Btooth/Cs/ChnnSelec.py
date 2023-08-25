from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChnnSelecCls:
	"""ChnnSelec commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("chnnSelec", core, parent)

	def get_chm_repet(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNselec:CHMRepet \n
		Snippet: value: int = driver.source.bb.btooth.cs.chnnSelec.get_chm_repet() \n
		No command help available \n
			:return: cs_repetition: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CHNNselec:CHMRepet?')
		return Conversions.str_to_int(response)

	def set_chm_repet(self, cs_repetition: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CHNNselec:CHMRepet \n
		Snippet: driver.source.bb.btooth.cs.chnnSelec.set_chm_repet(cs_repetition = 1) \n
		No command help available \n
			:param cs_repetition: integer Range: 1 to 3
		"""
		param = Conversions.decimal_value_to_str(cs_repetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CHNNselec:CHMRepet {param}')
