struct PythonData initializePythonData();
int openFileWrapper(struct PythonData *python_data);
int updateNozzleWrapper(struct PythonData *python_data, float new_nozzle_parameters[4]);
int exportNozzleWrapper(struct PythonData *python_data, char file_name[], char file_type[], char target_dir[], int use_default_taget_dir);
int killPython(struct PythonData *python_data);
int pynefWrapper(float new_nozzle_parameters[4], char file_name[], char file_type[], char target_dir[]);
