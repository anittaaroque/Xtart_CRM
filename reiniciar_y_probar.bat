@echo off
echo ============================================
echo Esperando a que reinicies Tomcat...
echo ============================================
echo.
echo INSTRUCCIONES:
echo 1. Detener Tomcat (Ctrl+C en la consola donde esta corriendo)
echo 2. Iniciar Tomcat nuevamente
echo 3. Esperar 10-15 segundos a que arranque
echo 4. Presionar cualquier tecla aqui para probar la conexion
echo.
pause

echo.
echo Probando conexion con la API...
echo.

python test_api.py

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo TODO LISTO! Puedes ejecutar la aplicacion
    echo ============================================
    echo.
    echo Ejecuta: python main.py
) else (
    echo.
    echo [ERROR] Aun hay problemas con la conexion
    echo Verifica que Tomcat este ejecutandose correctamente
)

pause
