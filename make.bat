set project=FolderMonitor

pyinstaller %1 --distpath ..\dist -y %project%.py

@echo.
@echo.
@echo.
@echo -----------------------------------------------------------------------------------------------------
@echo -----------------------------------------------------------------------------------------------------
@echo                 generazione exe completata per il progetto %project%...
@echo -----------------------------------------------------------------------------------------------------
@echo -----------------------------------------------------------------------------------------------------
@echo comando:    pyinstaller %1 --distpath ..\dist -y %project%.py
@echo.
@echo.
@echo.


info generazione exe completata per il progetto %project%...
exit
