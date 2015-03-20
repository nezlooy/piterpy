import sys, os, marshal
import idc, idaapi, idautils
import unpyc3


IS_64BIT = idaapi.get_inf_structure().is_64bit()
ADDR_SIZE = idc.SizeOf(idc.ParseType('void *', PT_TYP)[1])
R_SP = ('r' if IS_64BIT else 'e') + 'sp'
CALL_PATTERN = [[-2, [0xFF]], [-3, [0xFF]], [-5, [0xE8]], [-6, [0xFF]]]
get_addr_by_ptr = idc.Qword if IS_64BIT else idc.Dword
IMMR_LEVEL = 4
Py_MARSHAL_VERSION = 2
PYTHON_APP_DIR = 'C:\\Python34' # python dist-dir for filtering
P_OUT = sys.stdout # or file


def find_function(f_name, s100=False):
	for func in idautils.Functions():
		name = idc.GetFunctionName(func)
		if s100 and f_name == name:
			return name, func
		if not s100 and f_name in name:
			return name, func
	raise Exception('Function "{}" was not found'.format(f_name))

def prev_insn_is_call(ea):
	for p in CALL_PATTERN:
		# assume caller's ea
		caller = ea + p[0]
		# get the bytes
		bytes = [x for x in idautils.GetDataList(caller, len(p[1]), 1)]
		# do we have a match? is it a call instruction?
		if bytes == p[1] and idaapi.is_call_insn(caller):
			return caller
	return 0x00

def call_trace(max_ldeep=IMMR_LEVEL):
	sp = idc.GetRegValue(R_SP)
	seg = idaapi.getseg(sp)
	callers = []
	level = 0
	for sp_item in range(sp, seg.endEA + ADDR_SIZE, ADDR_SIZE):
		ptr = get_addr_by_ptr(sp_item)
		seg = idaapi.getseg(ptr)
		# only accept executable segments
		if (not seg) or ((seg.perm & idaapi.SEGPERM_EXEC) == 0):
			continue
		caller = prev_insn_is_call(ptr)
		# isn't CALL, skip it!
		if not caller:
			continue
		callers.append((idc.SegName(caller), idaapi.get_func_name(caller), hex(sp_item), GetCurrentThreadId()))
		level += 1
		if level == max_ldeep:
			break
	for c in callers:
		print c
	return ''

def py_object_get_member(ea, sname, mname):
	if isinstance(ea, idaapi.PyIdc_cvt_int64__):
		ea = ea.value
	sid = idaapi.get_struc_id(sname)
	stru = idaapi.get_struc(sid)
	member = idaapi.get_member_by_name(stru, mname)
	return ea + member.soff

def py_object_get_pmember(ea, sname, mname):
	return get_addr_by_ptr(py_object_get_member(ea, sname, mname))

def pyStringObject_to_string(ea, ob_type='PyUnicodeAsBytesObject'):
	if isinstance(ea, idaapi.PyIdc_cvt_int64__):
		ea = ea.value
	# cast to OB_TYPE struct to memory
	size = py_object_get_pmember(ea, ob_type, 'ob_size')
	sval = py_object_get_member(ea, ob_type, 'ob_sval')
	# dump it
	return idaapi.get_many_bytes(sval, size)

pyMarshal_WriteObjectToString = find_function('PyMarshal_WriteObjectToString')
def dump_code(ea, uncompyle=True, out=None):
	# function name withoit prefix "PythonXX_" if PDB used
	# proto: ret (void *) for disabling ctypes-casting
	marshaled = idaapi.Appcall.proto(pyMarshal_WriteObjectToString, 'void *__cdecl {}(PyObject *x, int version);'.format(pyMarshal_WriteObjectToString))
	dump = pyStringObject_to_string(marshaled(ea, Py_MARSHAL_VERSION))
	if uncompyle:
		print >> out, unpyc3.decompile(marshal.loads(dump))
	idaapi.Appcall.cleanup_appcall()

def get_obj_type(ea):
	if isinstance(ea, idaapi.PyIdc_cvt_int64__):
		ea = ea.value
	typename = idaapi.get_name(idaapi.BADADDR, py_object_get_pmember(ea, 'PyObject', 'ob_type'))
	typename = filter(lambda x: x, typename.split('_'))
	if typename[0].startswith('python'):
		typename.pop()
	return typename[0]

def pyTupleObject_to_plist(ea):
	if isinstance(ea, idaapi.PyIdc_cvt_int64__):
		ea = ea.value
	length = py_object_get_pmember(ea, 'PyTupleObject', 'ob_size')
	first_item_ea = py_object_get_member(ea, 'PyTupleObject', 'ob_item')
	return [get_addr_by_ptr(first_item_ea + off) for off in range(0, length * ADDR_SIZE, ADDR_SIZE)]


'''
Condition-code for func "builtin_exec" in file "break_condition_builtin_exec.py"
Condition-code for func "builtin_eval" in file "break_condition_builtin_eval.py"
Condition-code for func "PyImport_ImportModule" in file "break_condition_PyImport_ImportModule.py"
Condition-code for func "PyRun_StringFlags" in file "break_condition_PyRun_StringFlags.py"
Condition-code for func "PyRun_AnyFileExFlags" in file "break_condition_PyRun_AnyFileExFlags.py"
Condition-code for func "PyImport_ExecCodeModuleEx" in file "break_condition_PyImport_ExecCodeModuleEx.py"
Condition-code for func "PyEval_EvalCodeEx" in file "break_condition_PyEval_EvalCodeEx.py"

See "https://www.hex-rays.com/products/ida/6.6/" (Multiline breakpoint conditions) for mode info.
'''

def main():
	func_names = [
		('builtin_exec', True),
		('builtin_eval', True),
		('PyImport_Import', True),
		('PyRun_StringFlags', False),
		('PyRun_AnyFileExFlags', False),
		('PyImport_ExecCodeModuleEx', False),
		('PyEval_EvalCodeEx', False)
	]

	for func_name, func_f_cond in func_names:
		func_name, func_ea = find_function(func_name, func_f_cond)
		idc.AddBptEx(func_ea, 0, idaapi.BPT_SOFT)
		idaapi.enable_bpt(func_ea, True)
		print >> P_OUT, '[*] Setting conditional breakpoint on {}(0x{:08X})'.format(func_name, func_ea)

if __name__ == '__main__':
	main()
