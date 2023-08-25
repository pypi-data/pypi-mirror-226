from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqTypeCls:
	"""SeqType commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seqType", core, parent)

	def set(self, seq_type: enums.BtoCsSequenceType, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:SEQType \n
		Snippet: driver.source.bb.btooth.cs.subevent.seqType.set(seq_type = enums.BtoCsSequenceType.RANDOM, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param seq_type: SOUNDING| RANDOM
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.enum_scalar_to_str(seq_type, enums.BtoCsSequenceType)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:SEQType {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsSequenceType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:SEQType \n
		Snippet: value: enums.BtoCsSequenceType = driver.source.bb.btooth.cs.subevent.seqType.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: seq_type: SOUNDING| RANDOM"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:SEQType?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSequenceType)
