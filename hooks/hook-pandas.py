from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('pandas')
hiddenimports = [
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.skiplist'
]