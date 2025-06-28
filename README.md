### HolyShell - Python Injection Shell

#### Overview
This project enables runtime Python code injection into running processes via a dual-component system:
1. **C Library** (`holyshell.so`) - Injects an interactive Python shell into target processes
2. **Python Script** (`inject.py`) - Scans processes and manages injection operations

Key features:
- Interactive Python shell in foreign processes
- File script execution via `rrun` command
- Automatic detection of Python-loaded processes
- Cross-version Python support (libpythonX.X.so)

#### Compilation
Build the shared library with:
```bash
gcc -shared -o shell.so shell.c \
    -I/usr/include/python3.12/ \
    -L/usr/lib/ \
    -lpython3.12 -ldl -lm \
    -fPIC
```

Requirements:
- Python 3.x development headers
- GCC compiler
- Linux environment

#### Usage
1. Scan for Python processes:
```bash
python3 inject.py
```

2. Select target process from the table:
```
+------+-----------+------------------+
| PID  | NAME      | VERSION          |
+------+-----------+------------------+
| 1234 | python3   | libpython3.8.so  |
| 5678 | my_script | libpython3.6.so  |
+------+-----------+------------------+
enter pid: 5678
[HolyShell] Core injected
```

3. Interact with the injected shell:
```
holyshell > import sys
holyshell > print(sys.version)
3.6.9 (default, Oct  8 2020, 12:12:24)

holyshell > rrun /path/to/script.py
Script output...

holyshell > exit
holyshell > exited
```

#### Shell Commands
- `rrun <filename>` - Execute Python script from file
- Any valid Python code - Immediate execution
- `exit` - Terminate shell session (doesn't kill host process)

#### Implementation Details
1. **Safe Initialization**:
- Checks Python interpreter state (`Py_IsInitialized()`)
- Manages GIL (Global Interpreter Lock)
- Handles Python exceptions gracefully

2. **File Handling**:
- Binary read mode with size validation
- Dynamic memory allocation
- Null-termination guarantee

3. **Process Scanner**:
- Detects libpython in memory maps
- Auto-discovers Python versions
- Dynamic column formatting for display

#### Dependencies
- Python 3.12
- Required packages: `psutil`, `pyinjector`
```bash
pip install psutil pyinjector
```

#### Use Cases
- Debugging live Python applications
- Emergency intervention in critical processes
- Dynamic behavior modification
- Runtime memory inspection
- Legacy environment support
