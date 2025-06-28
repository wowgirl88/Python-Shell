import pyinjector
import os
import re
import psutil

def scan_linux():
    offset = 0
    processes = []
    regex_python_so = re.compile(r'libpython(\d+\.\d+|\d+)\.so')
    for proc in psutil.process_iter(['pid', 'name', 'memory_maps']):
        try:
            maps = proc.info['memory_maps']
            version = None
            if maps:
                for mem_map in maps:
                    if mem_map.path:
                        so_name = os.path.basename(mem_map.path)
                        match = regex_python_so.match(so_name)
                        if match:
                            version_part = match.group(1) if match.group(1) else ""
                            version = f"libpython{version_part}.so"
                            break 
            if version:
                pid = str(proc.info['pid'])
                name = proc.info['name']
                c_offset = max(len(pid), len(name), len(version))
                if c_offset > offset:
                    offset = c_offset
                processes.append((pid, name, version))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            pass

    max_pid_len = max(len(p[0]) for p in processes) if processes else 3
    max_name_len = max(len(p[1]) for p in processes) if processes else 4
    max_version_len = max(len(p[2]) for p in processes) if processes else 7
    pid_offset = max(len("PID"), max_pid_len)
    name_offset = max(len("NAME"), max_name_len)
    version_offset = max(len("VERSION"), max_version_len) 
    splitter = f"+{'-' * (pid_offset + 2)}+{'-' * (name_offset + 2)}+{'-' * (version_offset + 2)}+"
    compiler = lambda a, b, c: f"| {str(a).ljust(pid_offset)} | {str(b).ljust(name_offset)} | {str(c).ljust(version_offset)} |"
    print(splitter)
    print(compiler("PID", "NAME", "VERSION"))
    print(splitter)
    for pid, name, version in processes:
        if int(pid) != os.getpid():
            print(compiler(pid, name, version))
    print(splitter)

def get_so_path() -> str:
    files = [f for f in os.listdir(".") if f.endswith(".so")]
    for i, filename in enumerate(files, start=1):
        print(f"{i}. {filename}")
    print("0. Exit")
    target_file: str = input("Enter target file: ")
    if target_file == "0":
        return
    file_index = int(target_file) - 1
    if 0 <= file_index < len(files):
        selected_file = files[file_index]
        file_path = os.path.join(selected_file)
    return file_path

def main() -> None:
    scan_linux()
    pid = int(input("enter pid: "))
    print("[HolyShell] Core injected")
    try:
        pyinjector.inject(pid, os.path.abspath("shell.so"))
    except:
        pass

if __name__ == "__main__":
    main()
