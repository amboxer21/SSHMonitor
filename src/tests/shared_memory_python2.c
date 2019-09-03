#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <sys/ipc.h>
#include <sys/shm.h>

// Function 1: A simple 'hello world' function
static PyObject* shared_memory_python2(PyObject* self, PyObject* args) {
    // ftok to generate unique key
    key_t key = ftok("shmfile",65);

    int shmid = shmget(key,1024,0666|IPC_CREAT);

    // shmat to attach to shared memory
    char *str = (char*) shmat(shmid,(void*)0,0);
    const void *message = "Secret message";

    memcpy(str, message, (sizeof(message) + sizeof(size_t)));

    printf("Data written in memory: %s\n",str);

    //detach from shared memory
    shmdt(str);
    return Py_None;
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "shared_memory_python2", shared_memory_python2, METH_NOARGS, "Prints Hello World" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Test Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_myModule(void) {
    return PyModule_Create(&myModule);
}
