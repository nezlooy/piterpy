'''
PyObject *builtin_eval(PyObject *self, PyTupleObject *args)
'''
args_ea = idc.GetRegValue('rdx') if IS_64BIT else get_addr_by_ptr(str2ea('esp + 8'))
if args_ea != idaapi.BADADDR:
	args = pyTupleObject_to_plist(args_ea)
	print >> P_OUT, '#builtin_eval -> args count {}'.format(len(args))
	if args:
		if get_obj_type(args[0]) == 'PyString':
			print >> P_OUT, pyStringObject_to_string(args[0])
		if get_obj_type(args[0]) == 'PyUnicodeObject':
			print >> P_OUT, pyUnicodeObject_to_string(args[0])
	print >> P_OUT, '-' * 50 + '\n'
	print >> P_OUT, call_trace(8)
	return True
return False
