from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataListCls:
	"""DataList commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dataList", core, parent)

	def set(self, data_list: str, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:DTAList \n
		Snippet: driver.source.bb.btooth.cs.subevent.step.dataList.set(data_list = '1', subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param data_list: string
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = Conversions.value_to_quoted_str(data_list)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:DTAList {param}')

	def get(self, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:DTAList \n
		Snippet: value: str = driver.source.bb.btooth.cs.subevent.step.dataList.get(subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: data_list: string"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:DTAList?')
		return trim_str_response(response)
