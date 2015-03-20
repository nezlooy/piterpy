
#define _PyObject_HEAD_EXTRA
#define _PyObject_EXTRA_INIT
#define PyDict_MINSIZE 8
#define PySet_MINSIZE 8

typedef size_t Py_ssize_t;

#define PyObject_HEAD		\
	_PyObject_HEAD_EXTRA	\
	Py_ssize_t ob_refcnt;		\
	void *ob_type;

#define PyObject_VAR_HEAD 	\
	PyObject_HEAD 			\
	Py_ssize_t ob_size;

typedef struct _PyTypeObject {
	PyObject_VAR_HEAD
	const char *tp_name;
} PyTypeObject;

typedef struct _PyObject {
	PyObject_HEAD
} PyObject, *PPyObject;

typedef struct _PyVarObject {
	PyObject_VAR_HEAD
} PyVarObject;

typedef struct _PyStringObject {
	PyObject_VAR_HEAD
	long ob_shash;
	int ob_sstate;
	char ob_sval[1];
} PyStringObject, *PPyStringObject;

typedef struct _PyTupleObject {
	PyObject_VAR_HEAD
	PPyObject ob_item[1];
} PyTupleObject, *PPyTupleObject;

typedef struct _PyIntObject {
	PyObject_HEAD
	long ob_ival;
} PyIntObject;

typedef PyIntObject PyBoolObject;

typedef struct _PyCodeObject {
	PyObject_HEAD

	int co_argcount;
	int co_nlocals;
	int co_stacksize;
	int co_flags;

	PPyStringObject co_code;

	PPyTupleObject co_consts;
	PPyTupleObject co_names;
	PPyTupleObject co_varnames;
	PPyTupleObject co_freevars;
	PPyTupleObject co_cellvars;

	PPyStringObject co_filename;
	PPyStringObject co_name;

	int co_firstlineno;
	PPyStringObject co_lnotab;
	void *co_zombieframe;
	PPyObject co_weakreflist;
} PyCodeObject;

typedef struct _PyBufferObject {
	PyObject_HEAD
	PyObject *b_base;
	void *b_ptr;
	Py_ssize_t b_size;
	Py_ssize_t b_offset;
	int b_readonly;
	long b_hash;
} PyBufferObject;

typedef struct _PyDictEntry {
	Py_ssize_t me_hash;
	PPyObject me_key;
	PPyObject me_value;
} PyDictEntry;

typedef struct _PyDictObject {
	PyObject_HEAD
	Py_ssize_t ma_fill;  /* # Active + # Dummy */
	Py_ssize_t ma_used;  /* # Active (LEN -> ret) */

	Py_ssize_t ma_mask;

	PyDictEntry *ma_table;
	PyDictEntry *(__cdecl *ma_lookup)(_PyDictObject *mp, PPyObject key, long hash);
	PyDictEntry ma_smalltable[PyDict_MINSIZE];
} PyDictObject;

typedef struct _PyVarObject {
	PyObject_VAR_HEAD
} PyVarObject;

typedef struct _Py_buffer {
	void *buf;
	PPyObject obj;		/* owned reference */
	Py_ssize_t len;
	Py_ssize_t itemsize;

	int readonly;
	int ndim;
	char *format;

	Py_ssize_t *shape;
	Py_ssize_t *strides;
	Py_ssize_t *suboffsets;
	Py_ssize_t smalltable[2];  /* static store for shape and strides of
								  mono-dimensional buffers. */
	void *internal;
} Py_buffer;

typedef struct _PyMemoryViewObject {
	PyObject_HEAD
	PPyObject base;
	Py_buffer view;
} PyMemoryViewObject;

typedef struct _PyFloatObject {
	PyObject_HEAD
	double ob_fval;
} PyFloatObject;

typedef struct _PyFileObject {
	PyObject_HEAD
	FILE *f_fp;
	PPyObject f_name;
	PPyObject f_mode;
	int (*f_close)(FILE *);
	int f_softspace;			/* Flag used by 'print' command */
	int f_binary;			   /* Flag which indicates whether the file is
							   open in binary (1) or text (0) mode */
	char* f_buf;				/* Allocated readahead buffer */
	char* f_bufend;			 /* Points after last occupied position */
	char* f_bufptr;			 /* Current buffer position */
	char *f_setbuf;			 /* Buffer for setbuf(3) and setvbuf(3) */
	int f_univ_newline;		 /* Handle any newline convention */
	int f_newlinetypes;		 /* Types of newlines seen */
	int f_skipnextlf;		   /* Skip next \n */
	PPyObject f_encoding;
	PPyObject f_errors;
	PPyObject weakreflist; /* List of weak references */
	int unlocked_count;		 /* Num. currently running sections of code
							   using f_fp with the GIL released. */
	int readable;
	int writable;
} PyFileObject;

typedef struct _Py_complex {
	double real;
	double imag;
} Py_complex;

typedef struct _PyComplexObject {
	PyObject_HEAD
	Py_complex cval;
} PyComplexObject;

typedef struct _PyClassObject {
	PyObject_HEAD
	PPyObject cl_bases;	/* A tuple of class objects */
	PPyObject cl_dict;	/* A dictionary */
	PPyObject cl_name;	/* A string */
	/* The following three are functions or NULL */
	PPyObject cl_getattr;
	PPyObject cl_setattr;
	PPyObject cl_delattr;
	PPyObject cl_weakreflist; /* List of weak references */
} PyClassObject, *PPyClassObject;

typedef struct _PyInstanceObject {
	PyObject_HEAD
	PPyClassObject in_class;	/* The class object */
	PPyObject in_dict;	/* A dictionary */
	PPyObject in_weakreflist; /* List of weak references */
} PyInstanceObject;

typedef struct _PyMethodObject {
	PyObject_HEAD
	PPyObject im_func;   /* The callable object implementing the method */
	PPyObject im_self;   /* The instance it is bound to, or NULL */
	PPyObject im_class;  /* The class that asked for the method */
	PPyObject im_weakreflist; /* List of weak references */
} PyMethodObject;

typedef struct _PyByteArrayObject {
	PyObject_VAR_HEAD
	/* XXX(nnorwitz): should ob_exports be Py_sPy_ssize_t? */
	int ob_exports; /* how many buffer exports */
	Py_ssize_t ob_alloc; /* How many bytes allocated */
	char *ob_bytes;
} PyByteArrayObject;

typedef struct _PyListObject {
	PyObject_VAR_HEAD
	/* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
	PyObject **ob_item;
	Py_ssize_t allocated;
} PyListObject;


typedef unsigned short digit; // longintrepr.h (PYLONG_BITS_IN_DIGIT)
typedef short sdigit;

typedef struct _PyLongObject {
	PyObject_VAR_HEAD
	digit ob_digit[1];
} PyLongObject;


typedef PyObject *(*PyCFunction)(PyObject *, PyObject *);

typedef struct _PyMethodDef {
	const char	*ml_name;	/* The name of the built-in function/method */
	PyCFunction  ml_meth;	/* The C function that implements it */
	int		 ml_flags;	/* Combination of METH_xxx flags, which mostly
				   describe the args expected by the C func */
	const char	*ml_doc;	/* The __doc__ attribute, or NULL */
} PyMethodDef;

typedef struct {
	PyObject_HEAD
	PyMethodDef *m_ml; /* Description of the C function to call */
	PyObject	*m_self; /* Passed as 'self' arg to the C func, can be NULL */
	PyObject	*m_module; /* The __module__ attribute, can be anything */
} PyCFunctionObject;

typedef struct _setentry {
	long hash;	  /* cached hash code for the entry key */
	PyObject *key;
} setentry;

typedef struct _PySetObject {
	PyObject_HEAD

	Py_ssize_t fill;  /* # Active + # Dummy */
	Py_ssize_t used;  /* # Active */

	/* The table contains mask + 1 slots, and that's a power of 2.
	 * We store the mask instead of the size because the mask is more
	 * frequently needed.
	 */
	Py_ssize_t mask;

	/* table points to smalltable for small tables, else to
	 * additional malloc'ed memory.  table is never NULL!  This rule
	 * saves repeated runtime null-tests.
	 */
	setentry *table;
	setentry *(*lookup)(_PySetObject *so, PyObject *key, long hash);
	setentry smalltable[PySet_MINSIZE];

	long hash;				  /* only used by frozenset objects */
	PyObject *weakreflist;	  /* List of weak references */
} PySetObject;

typedef struct {
	PyObject_HEAD
	PyObject *start, *stop, *step;	/* not NULL */
} PySliceObject;

typedef struct _PyWeakReference {
	PyObject_HEAD

	PyObject *wr_object;
	PyObject *wr_callback;

	long hash;
	_PyWeakReference *wr_prev;
	_PyWeakReference *wr_next;
} PyWeakReference;

typedef struct _PyUnicodeObject {
	PyObject_HEAD
	Py_ssize_t length;		  /* Length of raw Unicode data in buffer */
	wchar_t *str;			/* Raw Unicode buffer (PY_UNICODE_TYPE (MS_WIN32)) */
	long hash;				  /* Hash value; -1 if not set */
	PyObject *defenc;		   /* (Default) Encoded version as Python
								   string, or NULL; this is used for
								   implementing the buffer protocol */
} PyUnicodeObject;

typedef struct _PyCObject {
	PyObject_HEAD
	void *cobject;
	void *desc;
	void (*destructor)(void *);
} PyCObject;

typedef PyTypeObject PyCapsuleObject;