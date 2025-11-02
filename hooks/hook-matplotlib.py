from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('matplotlib')
hiddenimports = [
    'matplotlib.backends.backend_agg',
    'matplotlib.backends.backend_tkagg'
]