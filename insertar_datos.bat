@echo off
echo ============================================
echo Insertando datos de prueba en proyecto_1t
echo ============================================
echo.

"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -padmin < insertar_datos_prueba.sql

if %errorlevel% equ 0 (
    echo.
    echo [OK] Datos insertados exitosamente!
    echo.
    echo ========================================
    echo CREDENCIALES DE PRUEBA:
    echo ========================================
    echo.
    echo ADMIN:
    echo   Email: admin@xtart.com
    echo   Password: admin123
    echo.
    echo EMPLEADO:
    echo   Email: empleado@xtart.com
    echo   Password: emp123
    echo.
    echo CLIENTE:
    echo   Email: cliente@test.com
    echo   Password: cliente123
    echo ========================================
) else (
    echo.
    echo [ERROR] No se pudieron insertar los datos
)

pause
