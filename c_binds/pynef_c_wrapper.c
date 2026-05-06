#ifndef Py_Object
#include <Python.h>
#endif

#ifndef fprintf
#include <stdio.h>
#endif

/*
 * This is kind of like the only function you should care about,
 * but if you are already reading the code, here they are!
 *
 *
 * note: The array length in arguments gets ingnored,
 * but I signal it cause it works like this:
 * updateNozzle(
 *   chamber_radius_mm
 *   chamber_cone_length_mm
 *   throat_radius_mm
 *   exit_radius_mm
 *   exit_cone_length_mm
 * )
 * 
 * if you put in more elements they will get ignored.
 */
int pynefWrapper(float new_nozzle_parameters[4], char file_name[], char file_type[], char target_dir[]){
  struct PythonData python_data = initializePythonData();
  Py_Initialize();

  PyRun_SimpleString("from sys import path");
  PyRun_SimpleString("path.append(\"lib/\")");

  python_data.pName = PyUnicode_FromString("pynef");
  python_data.pModule = PyImport_Import(python_data.pName);
  Py_DECREF(python_data.pName);

  if(python_data.pModule == NULL){
    fprintf(stderr,"[FROM C] No module found.\n");
    PyErr_Print();
    killPython(&python_data);
    return -1;
  }

  if(openFileWrapper(&python_data) != 0){
    printf("Failed on openFileWrapper\n");
    return -1;
  }
  if(updateNozzleWrapper(&python_data, new_nozzle_parameters) != 0){
    printf("Failed on updateNozzleWrapper\n");
    return -1;
  }
  if(exportNozzleWrapper(&python_data, file_name, file_type, target_dir, 1) != 0){
    printf("Failed on exportNozzleWrapper\n");
    return -1;
  }

  killPython(&python_data);
  return 0;
}

struct PythonData initializePythonData(){
  struct PythonData python_data;
  python_data.pArgs = NULL;
  python_data.pFunc = NULL;
  python_data.pModule = NULL;
  python_data.pName = NULL;
  python_data.pValue = NULL;
  return python_data;
}

int killPython(struct PythonData *python_data){
  Py_Finalize();
  Py_DECREF(python_data->pValue);
  Py_DECREF(python_data->pName);
  Py_DECREF(python_data->pModule);
  Py_DECREF(python_data->pFunc);
  Py_DECREF(python_data->pArgs);
  return 0;
}


int openFileWrapper(struct PythonData *python_data){
  printf("[FROM C] Entered openFile!.\n");
  python_data->pFunc = PyObject_GetAttrString(python_data->pModule, "openDefaultFile");
  
  if(python_data->pFunc && PyCallable_Check(python_data->pFunc)){
    printf("[FROM C] Found Python openDefaultFile() Function.\n");
    python_data->pValue = PyObject_CallObject(python_data->pFunc, NULL);

    if(python_data->pValue == NULL){
      fprintf(stderr,"[FROM C] Call failed\n");
      PyErr_Print();
      return -1;
    }
    if(python_data->pValue == 0){
      printf("[FROM C] Success!\n");
      printf("[FROM C] Result of call: %ld\n", PyLong_AsLong(python_data->pValue));
      PyErr_Print();
      return 0;
    }
  } else {
    fprintf(stderr,"[FROM C] Function not found.\n");
    PyErr_Print();
    return -1;
  }

  return 0;
}


// updateNozzle(
//   chamber_radius_mm
//   chamber_cone_length_mm
//   throat_radius_mm
//   exit_radius_mm
//   exit_cone_length_mm
// )
int updateNozzleWrapper(struct PythonData *python_data, float new_nozzle_parameters[4]){
  int i;
  printf("[FROM C] Entered updateNozzle!.\n");

  python_data->pFunc = PyObject_GetAttrString(python_data->pModule, "updateNozzle");

  if(python_data->pFunc && PyCallable_Check(python_data->pFunc)){
    printf("[FROM C] Found Python updateNozzle() Function.\n");

    // fill arguments
    python_data->pArgs = PyTuple_New(5);
    
    for(i=0; i<=4; i++){
      python_data->pValue = PyLong_FromInt32(new_nozzle_parameters[i]);
      if (python_data->pValue == NULL) {
        fprintf(stderr, "[FROM C] Cannot convert argument\n");
        PyErr_Print();
        return -1;
      }
      PyTuple_SetItem(python_data->pArgs, i, python_data->pValue);
      PyErr_Print();
    }
    printf("[FROM C] Converted arguments.\n");

    python_data->pValue = PyObject_CallObject(python_data->pFunc, python_data->pArgs);
    PyErr_Print();
    if (PyLong_AsLong(python_data->pValue) == 0){
      printf("[FROM C] Update success!\n");
      return 0;
    } else {
      fprintf(stderr,"[FROM C] Call failed\n");
      PyErr_Print();
      return -1;
    }
  } else {
    fprintf(stderr,"[FROM C] Function not found.\n");
    PyErr_Print();
    return -1;
  }
  return 0;
}


// kind of got the idea from CEA, 
// if you just want to use the defualt you pass NULL and 1,
// if you want to set a specific directory pass the full path and 0
int exportNozzleWrapper(struct PythonData *python_data, char file_name[], char file_type[], char target_dir[], int use_default_taget_dir){
  printf("[FROM C] Entered exportNozzle!.\n");

  python_data->pFunc = PyObject_GetAttrString(python_data->pModule, "exportNozzle");

  if(python_data->pFunc && PyCallable_Check(python_data->pFunc)){
    printf("[FROM C] Found Python exportNozzle() Function.\n");

    // fill arguments
    python_data->pArgs = PyTuple_New(3);
    python_data->pValue = PyUnicode_FromString(file_name);
    if (python_data->pValue == NULL) {
      fprintf(stderr, "[FROM C] Couldn't convert file_name\n");
      return -1;
    }
    printf("[FROM C] file_name: %s\n", PyBytes_AsString(PyUnicode_AsASCIIString(python_data->pValue)));
    PyTuple_SetItem(python_data->pArgs, 0, python_data->pValue);

    python_data->pValue = PyUnicode_FromString(file_type);
    if (python_data->pValue == NULL) {
      fprintf(stderr, "[FROM C] Couldn't convert file_name\n");
      return -1;
    }
    printf("[FROM C] file_type: %s\n", PyBytes_AsString(PyUnicode_AsASCIIString(python_data->pValue)));
    PyTuple_SetItem(python_data->pArgs, 1, python_data->pValue);

    python_data->pValue = PyUnicode_FromString(target_dir);
    if (python_data->pValue == NULL) {
      fprintf(stderr, "[FROM C] Couldn't convert file_name\n");
      return -1;
    }
    printf("[FROM C] target_dir: %s\n", PyBytes_AsString(PyUnicode_AsASCIIString(python_data->pValue)));
    PyTuple_SetItem(python_data->pArgs, 2, python_data->pValue);
    printf("[FROM C] Converted arguments.\n");
    python_data->pValue = PyObject_CallObject(python_data->pFunc, python_data->pArgs);
    PyErr_Print();

    if(PyLong_AsLong(python_data->pValue) == 0){
      printf("[FROM C] Success!\n");
      printf("[FROM C] Result of call: %ld\n", PyLong_AsLong(python_data->pValue));
      PyErr_Print();

    } else {
      fprintf(stderr,"[FROM C] Call failed\n");
      PyErr_Print();

      return -1;
    }
  } else {
    fprintf(stderr,"[FROM C] Function not found.\n");
    PyErr_Print();
    Py_Finalize();
    return -1;
  }
  return 0;
}
