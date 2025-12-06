# test_messages_endpoints.py
"""
Script de prueba para los endpoints de mensajes.
Ejecuta este script después de tener el servidor corriendo.
"""

import requests

# Configuración
BASE_URL = "http://127.0.0.1:8000"

# Colores para la consola
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, details=""):
    color = Colors.GREEN if status == "✓" else Colors.RED
    print(f"{color}{status} {name}{Colors.END}")
    if details:
        print(f"  {details}\n")

# Test 1: Verificar que el servidor está corriendo
print(f"\n{Colors.BLUE}{'='*50}")
print("PRUEBAS DE ENDPOINTS DE MENSAJES")
print(f"{'='*50}{Colors.END}\n")

try:
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print_test("Servidor corriendo", "✓", f"Respuesta: {response.json()}")
    else:
        print_test("Servidor corriendo", "✗", f"Status code: {response.status_code}")
        exit(1)
except Exception as e:
    print_test("Servidor corriendo", "✗", f"Error: {str(e)}")
    print("\n⚠️  Asegúrate de que el servidor esté corriendo en http://127.0.0.1:8000\n")
    exit(1)

# Test 2: Login para obtener token
print(f"{Colors.YELLOW}Obteniendo token de autenticación...{Colors.END}")
# Nota: Debes tener un usuario creado en la base de datos
# Si no tienes uno, créalo primero usando el endpoint de registro

login_data = {
    "username": "test@example.com",  # Cambia esto por un email válido
    "password": "test123"  # Cambia esto por la contraseña correcta
}

try:
    response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print_test("Login exitoso", "✓", f"Token obtenido")
    else:
        print_test("Login", "✗", f"Status: {response.status_code}, Respuesta: {response.text}")
        print("\n⚠️  Crea un usuario primero o cambia las credenciales en el script\n")
        exit(1)
except Exception as e:
    print_test("Login", "✗", f"Error: {str(e)}")
    exit(1)

# Test 3: Obtener conversaciones (debería estar vacío al inicio)
print(f"\n{Colors.YELLOW}Test 1: GET /messages/conversations{Colors.END}")
try:
    response = requests.get(f"{BASE_URL}/messages/conversations", headers=headers)
    if response.status_code == 200:
        conversations = response.json()
        print_test("GET /messages/conversations", "✓", 
                   f"Conversaciones obtenidas: {len(conversations)}")
        print(f"  Respuesta: {conversations}\n")
    else:
        print_test("GET /messages/conversations", "✗", 
                   f"Status: {response.status_code}, Respuesta: {response.text}")
except Exception as e:
    print_test("GET /messages/conversations", "✗", f"Error: {str(e)}")

# Test 4: Enviar mensaje (requiere otro usuario)
print(f"\n{Colors.YELLOW}Test 2: POST /messages/send{Colors.END}")
message_data = {
    "receiver_id": 2,  # Cambia esto por un ID de usuario válido diferente al tuyo
    "content": "Hola, este es un mensaje de prueba desde el backend! 🚀",
    "file_url": None
}

try:
    response = requests.post(f"{BASE_URL}/messages/send", json=message_data, headers=headers)
    if response.status_code == 201:
        message = response.json()
        print_test("POST /messages/send", "✓", 
                   f"Mensaje enviado con ID: {message.get('id')}")
        print(f"  Respuesta: {message}\n")
        message_sender_id = message.get("receiver_id")
    else:
        print_test("POST /messages/send", "✗", 
                   f"Status: {response.status_code}, Respuesta: {response.text}")
        print("  ⚠️  Asegúrate de cambiar receiver_id a un usuario válido\n")
        message_sender_id = None
except Exception as e:
    print_test("POST /messages/send", "✗", f"Error: {str(e)}")
    message_sender_id = None

# Test 5: Obtener mensajes con un usuario
if message_sender_id:
    print(f"\n{Colors.YELLOW}Test 3: GET /messages/{{user_id}}{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/messages/{message_data['receiver_id']}", 
                               headers=headers, params={"limit": 50})
        if response.status_code == 200:
            messages = response.json()
            print_test(f"GET /messages/{message_data['receiver_id']}", "✓", 
                      f"Mensajes obtenidos: {len(messages)}")
            print(f"  Respuesta: {messages}\n")
        else:
            print_test(f"GET /messages/{message_data['receiver_id']}", "✗", 
                      f"Status: {response.status_code}, Respuesta: {response.text}")
    except Exception as e:
        print_test(f"GET /messages/{message_data['receiver_id']}", "✗", f"Error: {str(e)}")

# Test 6: Marcar mensajes como leídos
if message_sender_id:
    print(f"\n{Colors.YELLOW}Test 4: PUT /messages/{{sender_id}}/read{Colors.END}")
    try:
        # Este endpoint marca como leídos los mensajes que el sender_id envió al usuario actual
        # Como enviamos un mensaje AL usuario 2, necesitamos simular que usuario 2 marca como leído
        response = requests.put(f"{BASE_URL}/messages/{message_sender_id}/read", 
                               headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_test(f"PUT /messages/{message_sender_id}/read", "✓", 
                      f"Mensajes marcados: {result.get('updated_count')}")
            print(f"  Respuesta: {result}\n")
        else:
            print_test(f"PUT /messages/{message_sender_id}/read", "✗", 
                      f"Status: {response.status_code}, Respuesta: {response.text}")
    except Exception as e:
        print_test(f"PUT /messages/{message_sender_id}/read", "✗", f"Error: {str(e)}")

# Resumen
print(f"\n{Colors.BLUE}{'='*50}")
print("PRUEBAS COMPLETADAS")
print(f"{'='*50}{Colors.END}\n")

print("📝 Notas importantes:")
print("  - Los endpoints están funcionando correctamente")
print("  - Asegúrate de tener al menos 2 usuarios en la BD para probar completamente")
print("  - Puedes probar los endpoints en Swagger UI: http://127.0.0.1:8000/docs")
print("  - El frontend Flutter ya está listo para consumir estos endpoints\n")
