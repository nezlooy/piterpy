'''
PyObject *load_module(char *name, FILE *fp, char *pathname, int type, PyObject *loader)
'''
if IS_64BIT:
	name_ea, pathname_ea, _type = map(idc.GetRegValue, ['rcx', 'r8', 'r9'])
else:
	r_esp = idc.GetRegValue('esp')
	name_ea, pathname_ea, _type = map(lambda off: get_addr_by_ptr(r_esp + off), [4, 12, 16])
if idaapi.BADADDR not in [name_ea, pathname_ea]:
	name, pathname = map(idc.GetString, [name_ea, pathname_ea])
	if pathname is not None and pathname.startswith(PYTHON_APP_DIR):
		return False
	print >> P_OUT, '-' * 50 + '\n'
	print >> P_OUT, '#load_module ({}) -> "{}" at "{}"'.format(FILETYPES[_type], name, pathname)
	print >> P_OUT, call_trace(8)
	return True
return False
