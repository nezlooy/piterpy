'''
PyObject *PyEval_EvalCodeEx(PyCodeObject *co, PyObject *globals, PyObject *locals, PyObject **args, int argcount, PyObject **kws, int kwcount, PyObject **defs, int defcount, PyObject *closure)
'''
if IS_64BIT:
	co_ea, _globals, _locals = map(idc.GetRegValue, ['rcx', 'rdx', 'r8'])
else:
	r_esp = idc.GetRegValue('esp')
	co_ea, _globals, _locals = map(lambda off: get_addr_by_ptr(r_esp + off), [4, 8, 12])
if co_ea != idaapi.BADADDR:
	co_filename_ea = py_object_get_pmember(co_ea, 'PyCodeObject', 'co_filename')
	co_name_ea = py_object_get_pmember(co_ea, 'PyCodeObject', 'co_name')
	co_firstlineno = idc.Dword(py_object_get_member(co_ea, 'PyCodeObject', 'co_firstlineno'))
	co_filename, co_name = map(pyStringObject_to_string, [co_filename_ea, co_name_ea])
	if not co_filename.startswith(PYTHON_APP_DIR):
		print >> P_OUT, '-' * 50 + '\n'
		print >> P_OUT, '\n#EvalCodeEx -> 0x{:08X} ({}): "{}:{}" ({})'.format(co_ea, idc.SegName(co_ea), co_filename, co_firstlineno, co_name)
		'dump_code(co_ea, out=P_OUT)'
		print >> P_OUT, call_trace(8)
		return True
return False
