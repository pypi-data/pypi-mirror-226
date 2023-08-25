from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode2TpmCls:
	"""Mode2Tpm commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode2Tpm", core, parent)

	def set(self, tmp: enums.BtoCsTpm, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE2Tpm \n
		Snippet: driver.source.bb.btooth.cs.subevent.mode2Tpm.set(tmp = enums.BtoCsTpm.TPM_10, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param tmp: No help available
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.enum_scalar_to_str(tmp, enums.BtoCsTpm)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE2Tpm {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsTpm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:MODE2Tpm \n
		Snippet: value: enums.BtoCsTpm = driver.source.bb.btooth.cs.subevent.mode2Tpm.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: tmp: TSW_0| TSW_1| TSW_2| TSW_4| TSW_10"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:MODE2Tpm?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTpm)
