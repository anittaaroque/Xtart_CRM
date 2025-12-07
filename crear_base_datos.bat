@echo off
echo ============================================
echo Creando base de datos proyecto_1t
echo ============================================
echo.
echo Usando credenciales:
echo Usuario: root
echo Password: admin
echo.

mysql -u root -padmin < setup_database.sql

if %errorlevel% equ 0 (
    echo.
    echo [OK] Base de datos creada exitosamente!
    echo.
    echo Ahora puede ejecutar: python main.py
) else (
    echo.
    echo [ERROR] No se pudo crear la base de datos
    echo.
    echo Verifique que:
    echo 1. MySQL este instalado y ejecutandose
    echo 2. Las credenciales sean correctas (usuario: root, password: admin)
    echo 3. El servicio MySQL este activo
)

pause
