'''
int exec_statement(PyFrameObject *f, PyObject *prog, PyObject *globals, PyObject *locals)
'''
prog_ea = idc.GetRegValue('rdx') if IS_64BIT else get_addr_by_ptr(str2ea('esp + 8'))
if prog_ea != idaapi.BADADDR:
	obj_type = get_obj_type(prog_ea)
	print >> P_OUT, '# exec_statement -> prog({})'.format(obj_type)
	if obj_type == 'PyString':
		print >> P_OUT, pyStringObject_to_string(prog_ea)
	if obj_type == 'PyUnicodeObject':
		print >> P_OUT, pyUnicodeObject_to_string(prog_ea)
	print >> P_OUT, '-' * 50 + '\n'
	print >> P_OUT, call_trace(8)
	return True
return False
