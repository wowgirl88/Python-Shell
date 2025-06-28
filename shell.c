#include <stdio.h>
#include <Python.h>
#include <string.h>
#include <stdlib.h>

char* getFilename(const char* inputString) {
    const char* prefix = "rrun ";
    int prefixLen = strlen(prefix);
    if (strncmp(inputString, prefix, prefixLen) != 0) {
        return NULL;
    }
    return (char*)(inputString + prefixLen);
}

char* readFileContent(const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (file == NULL) {
        return NULL;
    }
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);
    char* buffer = (char*)malloc(fileSize + 1);
    if (buffer == NULL) {
        fclose(file);
        return NULL;
    }
    size_t bytesRead = fread(buffer, 1, fileSize, file);
    if (bytesRead != fileSize) {
        free(buffer);
        fclose(file);
        return NULL;
    }
    buffer[fileSize] = '\0';
    fclose(file);
    return buffer;
}

void __attribute__((constructor)) init(void) {
    if (!Py_IsInitialized()) {
      Py_Initialize();
    }
    if (!Py_IsInitialized()) {
        fprintf(stderr, "Can't find Python interpreter or failed to initialize.\n");
        return;
    }

    char code[4096];
    printf("\n");

    while (1) {
        printf("holyshell > ");
        if (fgets(code, sizeof(code), stdin) == NULL) {
            break;
        }
        code[strcspn(code, "\n")] = 0;

        if (strcmp(code, "exit") == 0) {
            break;
        }

        char* filename = getFilename(code);
        if (filename != NULL) {
            char* fileContent = readFileContent(filename);
            if (fileContent != NULL) {
                PyGILState_STATE gstate = PyGILState_Ensure();
                PyRun_SimpleString(fileContent);
                if (PyErr_Occurred()) {
                    PyErr_Print();
                    PyErr_Clear();
                }
                PyGILState_Release(gstate);
                free(fileContent);
            } else {
                fprintf(stderr, "Error: Could not read file '%s'\n", filename);
            }
        } else {
            PyGILState_STATE gstate = PyGILState_Ensure();
            PyRun_SimpleString(code);
            if (PyErr_Occurred()) {
                PyErr_Print();
                PyErr_Clear();
            }
            PyGILState_Release(gstate);
        }
    }
    printf("holyshell > exited\n");
}
