

python -m venv .venv
.venv\Scripts\activate .venv
pip install -e ./tabular_project

Start the application:
python3 .\tabular_project\tabular\menu_main.py

pip index versions readline


With pip:

pip install -e ./tabular_project

Or pip3:

pip3 install -e ./tabular_project

Resulting path:

pip3 show tabular | grep Location

/Users/jaronschut/Library/Python/3.9/bin 

drwxr-xr-x  10 jaronschut  staff  320 Jun 13 17:02 .
drwx------   4 jaronschut  staff  128 Jun 13 17:00 ..
-rwxr-xr-x   1 jaronschut  staff  199 Jun 13 17:02 f2py
-rwxr-xr-x   1 jaronschut  staff  203 Jun 13 17:02 markdown-it
-rwxr-xr-x   1 jaronschut  staff  199 Jun 13 17:02 numpy-config
-rwxr-xr-x   1 jaronschut  staff  256 Jun 13 17:00 pip
-rwxr-xr-x   1 jaronschut  staff  256 Jun 13 17:00 pip3
-rwxr-xr-x   1 jaronschut  staff  256 Jun 13 17:00 pip3.9
-rwxr-xr-x   1 jaronschut  staff  198 Jun 13 17:02 pygmentize
-rwxr-xr-x   1 jaronschut  staff  202 Jun 13 17:02 tickdata

export PATH="$HOME/Library/Python/3.9/bin:$PATH"
export PATH="$HOME/opt/miniconda3/lib/python3.13/:$PATH"

Add to windows path:
C:\Users\Helms\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages

Check available versions

pip index versions requests
