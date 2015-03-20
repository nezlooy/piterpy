# Python 3.4 (IDA-actions)

1. Download debug information files
2. Setup debugger option (`Debugger -> Debugger options`) "Suspend on library load/unload"
3. Start process
4. After loading "python27.dll" select debug information file for it `File -> Load file -> PDB file`
5. In dialog window select file "python27.pdb" and set base address of module "python27.dll"
6. Load Header file with general structs `File -> Load file -> Parse C header file -> Select header-file` ("python2.7_x86.h" - for 32-bits, "python2.7_x86_64.h" for 64-bit versin of python)
7. Load script with general functions `File -> Script file -> Select "general_functions.py"`
8. In Breakpoints window, set breakpoint-condition (contents of the file `break_condition_<FUNCNAME>.py`) for each item
