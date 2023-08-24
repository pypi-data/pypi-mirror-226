#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyModuleDef display_py = {
    PyModuleDef_HEAD_INIT,
    .m_name = "dominx.display",
    .m_doc = NULL,
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_display(void) {
  PyObject *m = PyModule_Create(&display_py);
  return m;
}
