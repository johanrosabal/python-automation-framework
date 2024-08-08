@echo off
:: Configurar pip para confiar en los hosts
pip config --global set global.trusted-host pypi.org
pip config --global set global.trusted-host files.pythonhosted.org

:: Instalar dependencias
pip install -r requirements.txt