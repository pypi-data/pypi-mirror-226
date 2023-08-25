from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode1Tip1Cls:
	"""Mode1Tip1 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode1Tip1", core, parent)

	def set(self, mode_1_tip_1: enums.BtoCsTiP1, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE1Tip1 \n
		Snippet: driver.source.bb.btooth.cs.subevent.mode1Tip1.set(mode_1_tip_1 = enums.BtoCsTiP1.TIP1_10, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param mode_1_tip_1: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.enum_scalar_to_str(mode_1_tip_1, enums.BtoCsTiP1)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE1Tip1 {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE1Tip1 \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.subevent.mode1Tip1.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: mode_1_tip_1: TIP1_10| TIP1_20| TIP1_30| TIP1_40| TIP1_50| TIP1_60| TIP1_80| TIP1_145"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE1Tip1?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)
