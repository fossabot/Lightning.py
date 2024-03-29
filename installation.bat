@ECHO OFF
title Python Requirements Installation Script
ECHO Installing Discord.py...
py -3 -m pip install -U discord.py[voice]
PAUSE
ECHO Installing SQLAlchemy...
pip install SQLAlchemy==1.3.2
PAUSE
ECHO Installing GitPython...
pip install GitPython
PAUSE 
ECHO Installing Jishaku...
py -3 -m pip install -U jishaku
PAUSE
ECHO Installing BeautifulSoup...
pip install beautifulsoup4
PAUSE
ECHO Installing Python-DateUtil...
pip install python-dateutil
PAUSE
ECHO Installing dhooks...
pip install dhooks
PAUSE
ECHO Installing parsedatetime...
pip install parsedatetime
PAUSE
ECHO Finished Installation. Now exiting... 
TIMEOUT 30 /nobreak
EXIT
