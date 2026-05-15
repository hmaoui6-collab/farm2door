@echo off
cd /d "%~dp0"
python manage.py migrate
python manage.py setup_abdellah_admin
python manage.py fix_product_images
echo.
echo Farm2Door est prepare.
echo Admin principal: abdellah / Anomaly123
echo.
pause
