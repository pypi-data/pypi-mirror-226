from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 55 total commands, 3 Subgroups, 19 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	@property
	def chnnSelec(self):
		"""chnnSelec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chnnSelec'):
			from .ChnnSelec import ChnnSelecCls
			self._chnnSelec = ChnnSelecCls(self._core, self._cmd_group)
		return self._chnnSelec

	@property
	def chnnTable(self):
		"""chnnTable commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_chnnTable'):
			from .ChnnTable import ChnnTableCls
			self._chnnTable = ChnnTableCls(self._core, self._cmd_group)
		return self._chnnTable

	@property
	def subevent(self):
		"""subevent commands group. 23 Sub-classes, 0 commands."""
		if not hasattr(self, '_subevent'):
			from .Subevent import SubeventCls
			self._subevent = SubeventCls(self._core, self._cmd_group)
		return self._subevent

	# noinspection PyTypeChecker
	def get_ch_3_cjump(self) -> enums.BtoCsCh3Cjump:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CH3CJump \n
		Snippet: value: enums.BtoCsCh3Cjump = driver.source.bb.btooth.cs.get_ch_3_cjump() \n
		No command help available \n
			:return: ch_3_cjump: JUMP_2| JUMP_3| JUMP_4| JUMP_5| JUMP_6| JUMP_7| JUMP_8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CH3CJump?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cjump)

	def set_ch_3_cjump(self, ch_3_cjump: enums.BtoCsCh3Cjump) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CH3CJump \n
		Snippet: driver.source.bb.btooth.cs.set_ch_3_cjump(ch_3_cjump = enums.BtoCsCh3Cjump.JUMP_2) \n
		No command help available \n
			:param ch_3_cjump: JUMP_2| JUMP_3| JUMP_4| JUMP_5| JUMP_6| JUMP_7| JUMP_8
		"""
		param = Conversions.enum_scalar_to_str(ch_3_cjump, enums.BtoCsCh3Cjump)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CH3CJump {param}')

	# noinspection PyTypeChecker
	def get_ch_3_cshape(self) -> enums.BtoCsCh3Cshape:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CH3CShape \n
		Snippet: value: enums.BtoCsCh3Cshape = driver.source.bb.btooth.cs.get_ch_3_cshape() \n
		No command help available \n
			:return: ch_3_cshape: HAT| X
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CH3CShape?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cshape)

	def set_ch_3_cshape(self, ch_3_cshape: enums.BtoCsCh3Cshape) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CH3CShape \n
		Snippet: driver.source.bb.btooth.cs.set_ch_3_cshape(ch_3_cshape = enums.BtoCsCh3Cshape.HAT) \n
		No command help available \n
			:param ch_3_cshape: HAT| X
		"""
		param = Conversions.enum_scalar_to_str(ch_3_cshape, enums.BtoCsCh3Cshape)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CH3CShape {param}')

	def get_cnnect_intval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CNNEctIntval \n
		Snippet: value: float = driver.source.bb.btooth.cs.get_cnnect_intval() \n
		No command help available \n
			:return: connect_interval: float Range: 7.5 to 4000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CNNEctIntval?')
		return Conversions.str_to_float(response)

	def set_cnnect_intval(self, connect_interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CNNEctIntval \n
		Snippet: driver.source.bb.btooth.cs.set_cnnect_intval(connect_interval = 1.0) \n
		No command help available \n
			:param connect_interval: float Range: 7.5 to 4000
		"""
		param = Conversions.decimal_value_to_str(connect_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CNNEctIntval {param}')

	def get_cs_in_c(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSINc \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_in_c() \n
		No command help available \n
			:return: cs_in_c: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSINc?')
		return Conversions.str_to_str_list(response)

	def set_cs_in_c(self, cs_in_c: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSINc \n
		Snippet: driver.source.bb.btooth.cs.set_cs_in_c(cs_in_c = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_in_c: 32 bits
		"""
		param = Conversions.list_to_csv_str(cs_in_c)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSINc {param}')

	def get_cs_in_p(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSINp \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_in_p() \n
		No command help available \n
			:return: cs_in_p: 32 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSINp?')
		return Conversions.str_to_str_list(response)

	def set_cs_in_p(self, cs_in_p: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSINp \n
		Snippet: driver.source.bb.btooth.cs.set_cs_in_p(cs_in_p = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_in_p: 32 bits
		"""
		param = Conversions.list_to_csv_str(cs_in_p)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSINp {param}')

	def get_cs_iv_c(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSIVc \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_iv_c() \n
		No command help available \n
			:return: cs_iv_c: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSIVc?')
		return Conversions.str_to_str_list(response)

	def set_cs_iv_c(self, cs_iv_c: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSIVc \n
		Snippet: driver.source.bb.btooth.cs.set_cs_iv_c(cs_iv_c = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_iv_c: 64 bits
		"""
		param = Conversions.list_to_csv_str(cs_iv_c)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSIVc {param}')

	def get_cs_iv_p(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSIVp \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_iv_p() \n
		No command help available \n
			:return: cs_iv_p: 64 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSIVp?')
		return Conversions.str_to_str_list(response)

	def set_cs_iv_p(self, cs_iv_p: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSIVp \n
		Snippet: driver.source.bb.btooth.cs.set_cs_iv_p(cs_iv_p = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_iv_p: 64 bits
		"""
		param = Conversions.list_to_csv_str(cs_iv_p)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSIVp {param}')

	def get_cs_pv_c(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSPVc \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_pv_c() \n
		No command help available \n
			:return: cs_pv_c: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSPVc?')
		return Conversions.str_to_str_list(response)

	def set_cs_pv_c(self, cs_pv_c: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSPVc \n
		Snippet: driver.source.bb.btooth.cs.set_cs_pv_c(cs_pv_c = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_pv_c: 64 bits
		"""
		param = Conversions.list_to_csv_str(cs_pv_c)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSPVc {param}')

	def get_cs_pv_p(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSPVp \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_cs_pv_p() \n
		No command help available \n
			:return: cs_pv_p: 64 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSPVp?')
		return Conversions.str_to_str_list(response)

	def set_cs_pv_p(self, cs_pv_p: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSPVp \n
		Snippet: driver.source.bb.btooth.cs.set_cs_pv_p(cs_pv_p = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param cs_pv_p: 64 bits
		"""
		param = Conversions.list_to_csv_str(cs_pv_p)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSPVp {param}')

	def get_event_intval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EVENtIntval \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_event_intval() \n
		No command help available \n
			:return: event_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EVENtIntval?')
		return Conversions.str_to_int(response)

	def set_event_intval(self, event_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EVENtIntval \n
		Snippet: driver.source.bb.btooth.cs.set_event_intval(event_interval = 1) \n
		No command help available \n
			:param event_interval: integer Range: 500 to 4e6
		"""
		param = Conversions.decimal_value_to_str(event_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EVENtIntval {param}')

	def get_event_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EVENtoffset \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_event_offset() \n
		No command help available \n
			:return: event_offset: integer Range: 500 to 4e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EVENtoffset?')
		return Conversions.str_to_int(response)

	def set_event_offset(self, event_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EVENtoffset \n
		Snippet: driver.source.bb.btooth.cs.set_event_offset(event_offset = 1) \n
		No command help available \n
			:param event_offset: integer Range: 500 to 4e6
		"""
		param = Conversions.decimal_value_to_str(event_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EVENtoffset {param}')

	def get_filter_chm(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:FILTerchm \n
		Snippet: value: List[str] = driver.source.bb.btooth.cs.get_filter_chm() \n
		No command help available \n
			:return: cs_filtered_ch_m: 80 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:FILTerchm?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_role(self) -> enums.BtoCsRoles:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: value: enums.BtoCsRoles = driver.source.bb.btooth.cs.get_role() \n
		No command help available \n
			:return: role: INITIATOR| REFLECTOR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsRoles)

	def set_role(self, role: enums.BtoCsRoles) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: driver.source.bb.btooth.cs.set_role(role = enums.BtoCsRoles.INITIATOR) \n
		No command help available \n
			:param role: INITIATOR| REFLECTOR
		"""
		param = Conversions.enum_scalar_to_str(role, enums.BtoCsRoles)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:ROLE {param}')

	# noinspection PyTypeChecker
	def get_sh_sel(self) -> enums.BtoCsChSel:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SHSEl \n
		Snippet: value: enums.BtoCsChSel = driver.source.bb.btooth.cs.get_sh_sel() \n
		No command help available \n
			:return: ch_sel: SEL_3B| SEL_3C
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SHSEl?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsChSel)

	def set_sh_sel(self, ch_sel: enums.BtoCsChSel) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SHSEl \n
		Snippet: driver.source.bb.btooth.cs.set_sh_sel(ch_sel = enums.BtoCsChSel.SEL_3B) \n
		No command help available \n
			:param ch_sel: SEL_3B| SEL_3C
		"""
		param = Conversions.enum_scalar_to_str(ch_sel, enums.BtoCsChSel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SHSEl {param}')

	# noinspection PyTypeChecker
	def get_step_sched(self) -> enums.AutoManualModeB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:STEPSched \n
		Snippet: value: enums.AutoManualModeB = driver.source.bb.btooth.cs.get_step_sched() \n
		No command help available \n
			:return: step_sched: AUTO| MANUAL
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:STEPSched?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualModeB)

	def set_step_sched(self, step_sched: enums.AutoManualModeB) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:STEPSched \n
		Snippet: driver.source.bb.btooth.cs.set_step_sched(step_sched = enums.AutoManualModeB.AUTO) \n
		No command help available \n
			:param step_sched: AUTO| MANUAL
		"""
		param = Conversions.enum_scalar_to_str(step_sched, enums.AutoManualModeB)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:STEPSched {param}')

	def get_subevents(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEVents \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_subevents() \n
		No command help available \n
			:return: num_of_subevent: integer Range: 1 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SUBEVents?')
		return Conversions.str_to_int(response)

	def set_subevents(self, num_of_subevent: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEVents \n
		Snippet: driver.source.bb.btooth.cs.set_subevents(num_of_subevent = 1) \n
		No command help available \n
			:param num_of_subevent: integer Range: 1 to 32
		"""
		param = Conversions.decimal_value_to_str(num_of_subevent)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEVents {param}')

	def get_subevent_len(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEventLen \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_subevent_len() \n
		No command help available \n
			:return: subevent_len: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SUBEventLen?')
		return Conversions.str_to_int(response)

	def set_subevent_len(self, subevent_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEventLen \n
		Snippet: driver.source.bb.btooth.cs.set_subevent_len(subevent_len = 1) \n
		No command help available \n
			:param subevent_len: integer Range: 0 to 2.7e11
		"""
		param = Conversions.decimal_value_to_str(subevent_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEventLen {param}')

	def get_subevt_intv(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEvetIntv \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_subevt_intv() \n
		No command help available \n
			:return: subevent_interva: integer Range: 0 to 2.7e11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SUBEvetIntv?')
		return Conversions.str_to_int(response)

	def set_subevt_intv(self, subevent_interva: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SUBEvetIntv \n
		Snippet: driver.source.bb.btooth.cs.set_subevt_intv(subevent_interva = 1) \n
		No command help available \n
			:param subevent_interva: integer Range: 0 to 2.7e11
		"""
		param = Conversions.decimal_value_to_str(subevent_interva)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SUBEvetIntv {param}')

	# noinspection PyTypeChecker
	def get_user_ply_patt(self) -> enums.BtoCsPyLdPatt:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:USERPlypatt \n
		Snippet: value: enums.BtoCsPyLdPatt = driver.source.bb.btooth.cs.get_user_ply_patt() \n
		No command help available \n
			:return: user_ply_patt: PRBS09| RE11110000| RE10101010| PRBS15| RE11111111| RE00000000| RE00001111| RE01010101| USERPAYLOD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:USERPlypatt?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsPyLdPatt)

	def set_user_ply_patt(self, user_ply_patt: enums.BtoCsPyLdPatt) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:USERPlypatt \n
		Snippet: driver.source.bb.btooth.cs.set_user_ply_patt(user_ply_patt = enums.BtoCsPyLdPatt.PRBS09) \n
		No command help available \n
			:param user_ply_patt: PRBS09| RE11110000| RE10101010| PRBS15| RE11111111| RE00000000| RE00001111| RE01010101| USERPAYLOD
		"""
		param = Conversions.enum_scalar_to_str(user_ply_patt, enums.BtoCsPyLdPatt)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:USERPlypatt {param}')

	def clone(self) -> 'CsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
