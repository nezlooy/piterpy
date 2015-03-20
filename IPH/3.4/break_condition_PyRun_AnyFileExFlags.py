'''
int PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)
'''
filename_ea = idc.GetRegValue('rdx') if IS_64BIT else get_addr_by_ptr(str2ea('esp + 8'))
if filename_ea != idaapi.BADADDR:
	filename = idc.GetString(filename_ea)
	if not filename.startswith(PYTHON_APP_DIR):
		print >> P_OUT, '-' * 50 + '\n'
		print >> P_OUT, '#PyRun_AnyFileExFlags -> "{}"'.format(filename)
		print >> P_OUT, call_trace(8)
		return True
return False
