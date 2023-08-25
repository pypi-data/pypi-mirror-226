from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepCls:
	"""Step commands group definition. 9 total commands, 9 Subgroups, 0 group commands
	Repeated Capability: StepNull, default value after init: StepNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("step", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_stepNull_get', 'repcap_stepNull_set', repcap.StepNull.Nr0)

	def repcap_stepNull_set(self, stepNull: repcap.StepNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to StepNull.Default
		Default value after init: StepNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(stepNull)

	def repcap_stepNull_get(self) -> repcap.StepNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def accAddr(self):
		"""accAddr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_accAddr'):
			from .AccAddr import AccAddrCls
			self._accAddr = AccAddrCls(self._core, self._cmd_group)
		return self._accAddr

	@property
	def chnnlIndex(self):
		"""chnnlIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chnnlIndex'):
			from .ChnnlIndex import ChnnlIndexCls
			self._chnnlIndex = ChnnlIndexCls(self._core, self._cmd_group)
		return self._chnnlIndex

	@property
	def comSig(self):
		"""comSig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_comSig'):
			from .ComSig import ComSigCls
			self._comSig = ComSigCls(self._core, self._cmd_group)
		return self._comSig

	@property
	def dataPatt(self):
		"""dataPatt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dataPatt'):
			from .DataPatt import DataPattCls
			self._dataPatt = DataPattCls(self._core, self._cmd_group)
		return self._dataPatt

	@property
	def dataSrc(self):
		"""dataSrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dataSrc'):
			from .DataSrc import DataSrcCls
			self._dataSrc = DataSrcCls(self._core, self._cmd_group)
		return self._dataSrc

	@property
	def dataList(self):
		"""dataList commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dataList'):
			from .DataList import DataListCls
			self._dataList = DataListCls(self._core, self._cmd_group)
		return self._dataList

	@property
	def modeType(self):
		"""modeType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modeType'):
			from .ModeType import ModeTypeCls
			self._modeType = ModeTypeCls(self._core, self._cmd_group)
		return self._modeType

	@property
	def seqContent(self):
		"""seqContent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqContent'):
			from .SeqContent import SeqContentCls
			self._seqContent = SeqContentCls(self._core, self._cmd_group)
		return self._seqContent

	@property
	def userPaylod(self):
		"""userPaylod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_userPaylod'):
			from .UserPaylod import UserPaylodCls
			self._userPaylod = UserPaylodCls(self._core, self._cmd_group)
		return self._userPaylod

	def clone(self) -> 'StepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
