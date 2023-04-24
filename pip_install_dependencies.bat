@echo off
call "->QGISPATH<-\\o4w_env.bat"
call "py3_env"
call python -m pip install -r \"->HOMEPATH<-requirements.txt\"
call exit
@echo on