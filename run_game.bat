@echo off
echo Starting Protocol Overdrive in Docker...
echo Ensure VcXsrv is running with 'Disable Access Control' checked!

docker-compose up --build
pause
