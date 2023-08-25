from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqContentCls:
	"""SeqContent commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seqContent", core, parent)

	def get(self, subEventNull=repcap.SubEventNull.Default, stepNull=repcap.StepNull.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SUBEvent<CH0>]:[STEP<ST0>]:SEQContent \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.subevent.step.seqContent.get(subEventNull = repcap.SubEventNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param subEventNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: seq_content: 128 bits"""
		subEventNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subEventNull, repcap.SubEventNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvent{subEventNull_cmd_val}:STEP{stepNull_cmd_val}:SEQContent?')
		return Conversions.str_to_str_list(response)
