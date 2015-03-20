'''
PyObject *__cdecl PyImport_Import(_object *module_name)
'''
if IS_64BIT:
	name_ea = map(idc.GetRegValue, ['rcx'])
else:
	r_esp = idc.GetRegValue('esp')
	name_ea = map(lambda off: get_addr_by_ptr(r_esp + off), [4])
if name_ea != idaapi.BADADDR:
	name = pyStringObject_to_string(name_ea)
	print >> P_OUT, '-' * 50 + '\n'
	print >> P_OUT, '#PyImport_Import ({}) -> "{}"'.format(FILETYPES[_type], name)
	print >> P_OUT, call_trace(8)
	return True
return False
