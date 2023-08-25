from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChnnlIndexCls:
	"""ChnnlIndex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("chnnlIndex", core, parent)

	def set(self, channel_index: int, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:CHNNlIndex \n
		Snippet: driver.source.bb.btooth.cs.subevent.step.chnnlIndex.set(channel_index = 1, subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param channel_index: integer Range: 0 to 78
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = Conversions.decimal_value_to_str(channel_index)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:CHNNlIndex {param}')

	def get(self, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:CHNNlIndex \n
		Snippet: value: int = driver.source.bb.btooth.cs.subevent.step.chnnlIndex.get(subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: channel_index: integer Range: 0 to 78"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:CHNNlIndex?')
		return Conversions.str_to_int(response)
