from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChnnlCls:
	"""Chnnl commands group definition. 4 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: ChannelNull, default value after init: ChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("chnnl", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channelNull_get', 'repcap_channelNull_set', repcap.ChannelNull.Nr0)

	def repcap_channelNull_set(self, channelNull: repcap.ChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelNull.Default
		Default value after init: ChannelNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(channelNull)

	def repcap_channelNull_get(self) -> repcap.ChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def chnnlAllowed(self):
		"""chnnlAllowed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chnnlAllowed'):
			from .ChnnlAllowed import ChnnlAllowedCls
			self._chnnlAllowed = ChnnlAllowedCls(self._core, self._cmd_group)
		return self._chnnlAllowed

	@property
	def chnnlIndex(self):
		"""chnnlIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chnnlIndex'):
			from .ChnnlIndex import ChnnlIndexCls
			self._chnnlIndex = ChnnlIndexCls(self._core, self._cmd_group)
		return self._chnnlIndex

	@property
	def chnnlType(self):
		"""chnnlType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chnnlType'):
			from .ChnnlType import ChnnlTypeCls
			self._chnnlType = ChnnlTypeCls(self._core, self._cmd_group)
		return self._chnnlType

	@property
	def csCntrFreq(self):
		"""csCntrFreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csCntrFreq'):
			from .CsCntrFreq import CsCntrFreqCls
			self._csCntrFreq = CsCntrFreqCls(self._core, self._cmd_group)
		return self._csCntrFreq

	def clone(self) -> 'ChnnlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ChnnlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
