cd src
python main.py --genonly
set packer=packer_tmp.py
copy ..\%packer% .
pyinstaller %packer% -F --distpath . --clean -n game.exe
REM pyinstaller %packer% -w -F --distpath src --clean -n game.exe
del %packer%
rmdir build /S /Q
rmdir __pycache__ /S /Q
del game.exe.spec