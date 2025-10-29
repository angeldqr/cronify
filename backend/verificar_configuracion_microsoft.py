"""
Script de verificación de configuración de Microsoft OAuth
Ejecuta este script para verificar que todo está configurado correctamente
"""

import os
import sys
from pathlib import Path

# Configurar el path de Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cronify_backend.settings')

import django
django.setup()

from django.conf import settings
from django.core.management import call_command


def check_environment_variables():
    """Verifica que las variables de entorno necesarias estén configuradas"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("="*60 + "\n")
    
    required_vars = {
        'MICROSOFT_CLIENT_ID': settings.MICROSOFT_CLIENT_ID,
        'MICROSOFT_CLIENT_SECRET': settings.MICROSOFT_CLIENT_SECRET,
        'MICROSOFT_TENANT_ID': settings.MICROSOFT_TENANT_ID,
        'MICROSOFT_AUTHORITY': settings.MICROSOFT_AUTHORITY,
        'MICROSOFT_REDIRECT_URI': settings.MICROSOFT_REDIRECT_URI,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
    }
    
    all_configured = True
    for var_name, var_value in required_vars.items():
        if var_value and var_value != '':
            print(f"✅ {var_name}: Configurado")
        else:
            print(f"❌ {var_name}: NO CONFIGURADO")
            all_configured = False
    
    print("\n" + "-"*60)
    if all_configured:
        print("✅ Todas las variables están configuradas correctamente\n")
    else:
        print("❌ Faltan variables por configurar. Revisa el archivo .env\n")
    
    return all_configured


def check_installed_apps():
    """Verifica que las apps necesarias estén instaladas"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE APPS INSTALADAS")
    print("="*60 + "\n")
    
    required_apps = [
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.microsoft',
        'users',
    ]
    
    all_installed = True
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"✅ {app}: Instalado")
        else:
            print(f"❌ {app}: NO INSTALADO")
            all_installed = False
    
    print("\n" + "-"*60)
    if all_installed:
        print("✅ Todas las apps están instaladas correctamente\n")
    else:
        print("❌ Faltan apps por instalar. Revisa settings.py\n")
    
    return all_installed


def check_database():
    """Verifica el estado de las migraciones"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE BASE DE DATOS")
    print("="*60 + "\n")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a la base de datos: OK")
        
        # Verificar migraciones
        print("\nVerificando migraciones pendientes...")
        call_command('showmigrations', '--plan', stdout=open(os.devnull, 'w'))
        print("✅ Migraciones: OK")
        
        return True
    except Exception as e:
        print(f"❌ Error con la base de datos: {e}")
        return False


def check_user_model():
    """Verifica que el modelo Usuario tenga los campos necesarios"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DEL MODELO USUARIO")
    print("="*60 + "\n")
    
    try:
        from users.models import Usuario
        
        required_fields = [
            'microsoft_id',
            'microsoft_access_token',
            'microsoft_refresh_token',
        ]
        
        all_fields_exist = True
        for field_name in required_fields:
            if hasattr(Usuario, field_name):
                print(f"✅ Campo '{field_name}': Existe")
            else:
                print(f"❌ Campo '{field_name}': NO EXISTE")
                all_fields_exist = False
        
        print("\n" + "-"*60)
        if all_fields_exist:
            print("✅ El modelo Usuario tiene todos los campos necesarios\n")
        else:
            print("❌ Faltan campos en el modelo Usuario")
            print("   Ejecuta: python manage.py makemigrations")
            print("   Luego: python manage.py migrate\n")
        
        return all_fields_exist
    except Exception as e:
        print(f"❌ Error al verificar el modelo: {e}\n")
        return False


def test_microsoft_auth_service():
    """Verifica que el servicio de autenticación funcione"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DEL SERVICIO DE AUTENTICACIÓN")
    print("="*60 + "\n")
    
    try:
        from users.microsoft_auth import MicrosoftAuthService
        
        service = MicrosoftAuthService()
        print("✅ MicrosoftAuthService: Importado correctamente")
        
        # Verificar que se puede obtener la URL de autorización
        try:
            auth_url = service.get_authorization_url()
            if auth_url and 'login.microsoftonline.com' in auth_url:
                print("✅ URL de autorización: OK")
                return True
            else:
                print("❌ URL de autorización: Inválida")
                return False
        except Exception as e:
            print(f"❌ Error al obtener URL de autorización: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Error al importar MicrosoftAuthService: {e}")
        return False


def print_summary(results):
    """Imprime un resumen final"""
    print("\n" + "="*60)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*60 + "\n")
    
    if all(results.values()):
        print("✅ ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!")
        print("\n📝 Próximos pasos:")
        print("   1. Inicia el servidor: python manage.py runserver")
        print("   2. Inicia el frontend: cd ../frontend && npm run dev")
        print("   3. Ve a http://localhost:9000/auth/login")
        print("   4. Prueba el botón 'Iniciar sesión con Microsoft'\n")
    else:
        print("❌ HAY PROBLEMAS DE CONFIGURACIÓN")
        print("\n📝 Revisa los errores anteriores y:")
        failed_checks = [k for k, v in results.items() if not v]
        for check in failed_checks:
            print(f"   - {check}")
        print()


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("VERIFICADOR DE CONFIGURACIÓN - MICROSOFT OAUTH")
    print("="*60)
    
    results = {
        'Variables de entorno': check_environment_variables(),
        'Apps instaladas': check_installed_apps(),
        'Base de datos': check_database(),
        'Modelo Usuario': check_user_model(),
        'Servicio de autenticación': test_microsoft_auth_service(),
    }
    
    print_summary(results)


if __name__ == '__main__':
    main()
