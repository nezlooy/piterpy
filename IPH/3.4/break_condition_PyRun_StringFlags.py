'''
PyObject *__cdecl j_PyRun_StringFlags(const char *str, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)
'''
if IS_64BIT:
	str_ea, start_ea = map(idc.GetRegValue, ['rcx', 'rdx'])
else:
	r_esp = idc.GetRegValue('esp')
	str_ea, start_ea = map(lambda off: get_addr_by_ptr(r_esp + off), [4, 8])
if str_ea != idaapi.BADADDR:
	_str = idc.GetString(str_ea, -1, ASCSTR_UNICODE)
	if _str is None:
		_str = idc.GetString(str_ea)
	print >> P_OUT, '#PyRun_StringFlags -> start_ea: {}'.format(start_ea)
	print >> P_OUT, _str
	print >> P_OUT, '-' * 50 + '\n'
	print call_trace(8)
	return True
return False
