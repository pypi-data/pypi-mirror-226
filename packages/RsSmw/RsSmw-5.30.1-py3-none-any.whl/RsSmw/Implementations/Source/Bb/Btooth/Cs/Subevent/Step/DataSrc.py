from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataSrcCls:
	"""DataSrc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dataSrc", core, parent)

	def set(self, data_src: enums.DataSourceB, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:DATASrc \n
		Snippet: driver.source.bb.btooth.cs.subevent.step.dataSrc.set(data_src = enums.DataSourceB.ALL0, subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param data_src: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = Conversions.enum_scalar_to_str(data_src, enums.DataSourceB)
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:DATASrc {param}')

	# noinspection PyTypeChecker
	def get(self, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> enums.DataSourceB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:DATASrc \n
		Snippet: value: enums.DataSourceB = driver.source.bb.btooth.cs.subevent.step.dataSrc.get(subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: data_src: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:DATASrc?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceB)
