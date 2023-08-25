from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode3Tip2Cls:
	"""Mode3Tip2 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode3Tip2", core, parent)

	def set(self, mode_3_tip_2: enums.BtoCsTiP1, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE3Tip2 \n
		Snippet: driver.source.bb.btooth.cs.subevent.mode3Tip2.set(mode_3_tip_2 = enums.BtoCsTiP1.TIP1_10, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param mode_3_tip_2: No help available
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.enum_scalar_to_str(mode_3_tip_2, enums.BtoCsTiP1)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE3Tip2 {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE3Tip2 \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.subevent.mode3Tip2.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: mode_3_tip_2: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE3Tip2?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)
