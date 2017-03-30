
set /p project="Enter name of project:"



django-admin startproject %project%
timeout 1
cd %project%
set /p app_name="Enter name of app:"
mkdir apps
cd apps
null> __init__.py
python ..\manage.py startapp %app_name%
timeout 1
cd %app_name%
mkdir static
mkdir templates
cd static
mkdir %app_name%
mkdir css
mkdir images
mkddir js
cd..
cd templates
mkdir %app_name%
cd %app_name%
null> index.html
cd..
cd..
null> urls.py

echo "success"
echo "created " %project% "and " %app_name%
echo "Press any key to exit"
pause
