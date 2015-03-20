'''
PyObject *__cdecl j_PyImport_ExecCodeModuleEx(const char *name, PyObject *co, const char *pathname)
'''
if IS_64BIT:
	name_ea, co_ea, pathname_ea = map(idc.GetRegValue, ['rcx', 'rdx', 'r8'])
else:
	r_esp = idc.GetRegValue('esp')
	name_ea, co_ea, pathname_ea = map(lambda off: get_addr_by_ptr(r_esp + off), [4, 8, 12])
if co_ea != idaapi.BADADDR:
	co_filename_ea = py_object_get_pmember(co_ea, 'PyCodeObject', 'co_filename')
	co_name_ea = py_object_get_pmember(co_ea, 'PyCodeObject', 'co_name')
	co_filename, co_name = map(pyStringObject_to_string, [co_filename_ea, co_name_ea])
	name, pathname = map(idc.GetString, [name_ea, pathname_ea])
	if not co_filename.startswith(PYTHON_APP_DIR):
		print >> P_OUT, '-' * 50 + '\n'
		print >> P_OUT, '#ExecCodeModuleEx -> 0x{:08X} ({}): {} ({}) -> "{}" ({})'.format(co_ea, idc.SegName(co_ea), name, pathname, co_filename, co_name)
		'dump_code(co_ea, out=P_OUT)'
		print >> P_OUT, call_trace(8)
		return True
return False
