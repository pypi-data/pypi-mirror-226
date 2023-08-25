import os
import shutil

ori_dir = os.getcwd()
target_dir = os.path.join(ori_dir,'okftools')

os.chdir('code_sources/GUI')
filename = os.path.join(os.getcwd(),'okftools.py')
shutil.copy(filename, os.path.join(target_dir,'GUI'))

os.system("python -m venv test_env")
os.chdir("test_env")
shutil.copy(filename, os.path.join(target_dir,os.getcwd()))

os.system("source bin/activate")
os.system("pip install pygame")
os.system("pip install pyinstaller")
os.system("pyinstaller --onefile okftools.py")

os.chdir(ori_dir)
