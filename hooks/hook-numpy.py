from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

datas = collect_data_files('numpy')
binaries = collect_dynamic_libs('numpy')
hiddenimports = [
    'numpy.core._multiarray_umath',
    'numpy.core._dtype_ctypes', 
    'numpy.core._multiarray_tests'
]