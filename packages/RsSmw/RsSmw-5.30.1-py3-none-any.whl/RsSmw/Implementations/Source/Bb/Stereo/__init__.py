from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StereoCls:
	"""Stereo commands group definition. 90 total commands, 7 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stereo", core, parent)

	@property
	def audio(self):
		"""audio commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def ds(self):
		"""ds commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_ds'):
			from .Ds import DsCls
			self._ds = DsCls(self._core, self._cmd_group)
		return self._ds

	@property
	def ghex(self):
		"""ghex commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_ghex'):
			from .Ghex import GhexCls
			self._ghex = GhexCls(self._core, self._cmd_group)
		return self._ghex

	@property
	def grps(self):
		"""grps commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_grps'):
			from .Grps import GrpsCls
			self._grps = GrpsCls(self._core, self._cmd_group)
		return self._grps

	@property
	def pilot(self):
		"""pilot commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_pilot'):
			from .Pilot import PilotCls
			self._pilot = PilotCls(self._core, self._cmd_group)
		return self._pilot

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	def get_deviation(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:STEReo:DEViation \n
		Snippet: value: int = driver.source.bb.stereo.get_deviation() \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:DEViation?')
		return Conversions.str_to_int(response)

	def set_deviation(self, deviation: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:DEViation \n
		Snippet: driver.source.bb.stereo.set_deviation(deviation = 1) \n
		No command help available \n
			:param deviation: No help available
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:DEViation {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:PRESet \n
		Snippet: driver.source.bb.stereo.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:PRESet \n
		Snippet: driver.source.bb.stereo.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:STEReo:PRESet', opc_timeout_ms)

	def get_puws_int(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:STEReo:PUWSint \n
		Snippet: value: bool = driver.source.bb.stereo.get_puws_int() \n
		No command help available \n
			:return: puws: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:PUWSint?')
		return Conversions.str_to_bool(response)

	def set_puws_int(self, puws: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:PUWSint \n
		Snippet: driver.source.bb.stereo.set_puws_int(puws = False) \n
		No command help available \n
			:param puws: No help available
		"""
		param = Conversions.bool_to_str(puws)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PUWSint {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.FmStereoAudSrc:
		"""SCPI: [SOURce<HW>]:BB:STEReo:SOURce \n
		Snippet: value: enums.FmStereoAudSrc = driver.source.bb.stereo.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoAudSrc)

	def set_source(self, source: enums.FmStereoAudSrc) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:SOURce \n
		Snippet: driver.source.bb.stereo.set_source(source = enums.FmStereoAudSrc.FILE) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.FmStereoAudSrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:STEReo:STATe \n
		Snippet: value: bool = driver.source.bb.stereo.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:STATe \n
		Snippet: driver.source.bb.stereo.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:STATe {param}')

	def clone(self) -> 'StereoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StereoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
