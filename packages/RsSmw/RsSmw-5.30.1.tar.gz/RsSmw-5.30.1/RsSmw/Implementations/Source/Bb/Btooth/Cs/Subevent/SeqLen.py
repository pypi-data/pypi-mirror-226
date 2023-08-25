from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqLenCls:
	"""SeqLen commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seqLen", core, parent)

	def set(self, seq_len: enums.BtoCsSequenceLen, subEventNull=repcap.SubEventNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:SEQLen \n
		Snippet: driver.source.bb.btooth.cs.subevent.seqLen.set(seq_len = enums.BtoCsSequenceLen.SL_128, subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param seq_len: SL_32| SL_64| SL_96| SL_128
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
		"""
		param = Conversions.enum_scalar_to_str(seq_len, enums.BtoCsSequenceLen)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:SEQLen {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default) -> enums.BtoCsSequenceLen:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:SEQLen \n
		Snippet: value: enums.BtoCsSequenceLen = driver.source.bb.btooth.cs.subevent.seqLen.get(subEventNull = repcap.SubEventNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:return: seq_len: SL_32| SL_64| SL_96| SL_128"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:SEQLen?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSequenceLen)
