#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct {
    PyObject_HEAD
} StreamObject;

static PyTypeObject StreamType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "dominx.stream.Stream",
    .tp_doc = NULL,
    .tp_basicsize = sizeof(StreamObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
};

static PyModuleDef stream_py = {
    PyModuleDef_HEAD_INIT,
    .m_name = "dominx.stream",
    .m_doc = NULL,
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_stream(void) {
    PyObject *m;

    if (PyType_Ready(&StreamType) < 0)
        return NULL;

    m = PyModule_Create(&stream_py);
    if (m == NULL)
        return NULL;

    Py_INCREF(&StreamType);
    if (PyModule_AddObject(m, "Stream", (PyObject *) &StreamType) < 0) {
        Py_DECREF(&StreamType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
