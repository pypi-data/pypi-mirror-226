from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubeventCls:
	"""Subevent commands group definition. 31 total commands, 23 Subgroups, 0 group commands
	Repeated Capability: SubEventNull, default value after init: SubEventNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subevent", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_subEventNull_get', 'repcap_subEventNull_set', repcap.SubEventNull.Nr0)

	def repcap_subEventNull_set(self, subEventNull: repcap.SubEventNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubEventNull.Default
		Default value after init: SubEventNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(subEventNull)

	def repcap_subEventNull_get(self) -> repcap.SubEventNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def mainMode(self):
		"""mainMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mainMode'):
			from .MainMode import MainModeCls
			self._mainMode = MainModeCls(self._core, self._cmd_group)
		return self._mainMode

	@property
	def mmMaxSteps(self):
		"""mmMaxSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmMaxSteps'):
			from .MmMaxSteps import MmMaxStepsCls
			self._mmMaxSteps = MmMaxStepsCls(self._core, self._cmd_group)
		return self._mmMaxSteps

	@property
	def mmMinSteps(self):
		"""mmMinSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmMinSteps'):
			from .MmMinSteps import MmMinStepsCls
			self._mmMinSteps = MmMinStepsCls(self._core, self._cmd_group)
		return self._mmMinSteps

	@property
	def mmRepet(self):
		"""mmRepet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmRepet'):
			from .MmRepet import MmRepetCls
			self._mmRepet = MmRepetCls(self._core, self._cmd_group)
		return self._mmRepet

	@property
	def mmSteps(self):
		"""mmSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmSteps'):
			from .MmSteps import MmStepsCls
			self._mmSteps = MmStepsCls(self._core, self._cmd_group)
		return self._mmSteps

	@property
	def mode0Tip1(self):
		"""mode0Tip1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode0Tip1'):
			from .Mode0Tip1 import Mode0Tip1Cls
			self._mode0Tip1 = Mode0Tip1Cls(self._core, self._cmd_group)
		return self._mode0Tip1

	@property
	def mode0Steps(self):
		"""mode0Steps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode0Steps'):
			from .Mode0Steps import Mode0StepsCls
			self._mode0Steps = Mode0StepsCls(self._core, self._cmd_group)
		return self._mode0Steps

	@property
	def mode1Tip1(self):
		"""mode1Tip1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode1Tip1'):
			from .Mode1Tip1 import Mode1Tip1Cls
			self._mode1Tip1 = Mode1Tip1Cls(self._core, self._cmd_group)
		return self._mode1Tip1

	@property
	def mode2Nap(self):
		"""mode2Nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode2Nap'):
			from .Mode2Nap import Mode2NapCls
			self._mode2Nap = Mode2NapCls(self._core, self._cmd_group)
		return self._mode2Nap

	@property
	def mode2Tip2(self):
		"""mode2Tip2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode2Tip2'):
			from .Mode2Tip2 import Mode2Tip2Cls
			self._mode2Tip2 = Mode2Tip2Cls(self._core, self._cmd_group)
		return self._mode2Tip2

	@property
	def mode2Tpm(self):
		"""mode2Tpm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode2Tpm'):
			from .Mode2Tpm import Mode2TpmCls
			self._mode2Tpm = Mode2TpmCls(self._core, self._cmd_group)
		return self._mode2Tpm

	@property
	def mode2Tsw(self):
		"""mode2Tsw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode2Tsw'):
			from .Mode2Tsw import Mode2TswCls
			self._mode2Tsw = Mode2TswCls(self._core, self._cmd_group)
		return self._mode2Tsw

	@property
	def mode3Tip2(self):
		"""mode3Tip2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode3Tip2'):
			from .Mode3Tip2 import Mode3Tip2Cls
			self._mode3Tip2 = Mode3Tip2Cls(self._core, self._cmd_group)
		return self._mode3Tip2

	@property
	def mode3Tpm(self):
		"""mode3Tpm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode3Tpm'):
			from .Mode3Tpm import Mode3TpmCls
			self._mode3Tpm = Mode3TpmCls(self._core, self._cmd_group)
		return self._mode3Tpm

	@property
	def mode3Tsw(self):
		"""mode3Tsw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode3Tsw'):
			from .Mode3Tsw import Mode3TswCls
			self._mode3Tsw = Mode3TswCls(self._core, self._cmd_group)
		return self._mode3Tsw

	@property
	def seqLen(self):
		"""seqLen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqLen'):
			from .SeqLen import SeqLenCls
			self._seqLen = SeqLenCls(self._core, self._cmd_group)
		return self._seqLen

	@property
	def seqType(self):
		"""seqType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqType'):
			from .SeqType import SeqTypeCls
			self._seqType = SeqTypeCls(self._core, self._cmd_group)
		return self._seqType

	@property
	def steps(self):
		"""steps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_steps'):
			from .Steps import StepsCls
			self._steps = StepsCls(self._core, self._cmd_group)
		return self._steps

	@property
	def subevtSpace(self):
		"""subevtSpace commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subevtSpace'):
			from .SubevtSpace import SubevtSpaceCls
			self._subevtSpace = SubevtSpaceCls(self._core, self._cmd_group)
		return self._subevtSpace

	@property
	def subMstep(self):
		"""subMstep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subMstep'):
			from .SubMstep import SubMstepCls
			self._subMstep = SubMstepCls(self._core, self._cmd_group)
		return self._subMstep

	@property
	def subMode(self):
		"""subMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subMode'):
			from .SubMode import SubModeCls
			self._subMode = SubModeCls(self._core, self._cmd_group)
		return self._subMode

	@property
	def tfcs(self):
		"""tfcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfcs'):
			from .Tfcs import TfcsCls
			self._tfcs = TfcsCls(self._core, self._cmd_group)
		return self._tfcs

	@property
	def step(self):
		"""step commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	def clone(self) -> 'SubeventCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubeventCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
