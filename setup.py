from distutils.core import setup
import shutil, py2exe

opts = {'py2exe': {'compressed': True, "dll_excludes": ["MSVCP90.dll"], "includes": ["PyQt5.sip"]}}

setup(console=[{"script" : "tetris.py"}], options=opts)
shutil.rmtree('build', ignore_errors=True)