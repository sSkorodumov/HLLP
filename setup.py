from cx_Freeze import setup, Executable

base = None    

executables = [Executable("C:\python\PythonApplication2\PythonApplication2\PythonApplication2.py", base=base)]

packages = ["smtplib", "email", "email.mime.application", "email.mime.multipart", "zipfile", "os", "struct", "sys", "threading"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "virus",
    options = options,
    version = "1.0",
    description = '',
    executables = executables
)