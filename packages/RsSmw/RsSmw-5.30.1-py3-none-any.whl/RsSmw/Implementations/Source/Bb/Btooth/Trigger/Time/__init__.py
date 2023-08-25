from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def get_time(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:TIME:TIME \n
		Snippet: value: str = driver.source.bb.btooth.trigger.time.get_time() \n
		No command help available \n
			:return: time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:TRIGger:TIME:TIME?')
		return trim_str_response(response)

	def set_time(self, time: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:TIME:TIME \n
		Snippet: driver.source.bb.btooth.trigger.time.set_time(time = '1') \n
		No command help available \n
			:param time: No help available
		"""
		param = Conversions.value_to_quoted_str(time)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:TIME:TIME {param}')

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
