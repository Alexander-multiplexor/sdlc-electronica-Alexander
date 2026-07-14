# Semana 1 - Python Profesional y Principios SOLID

Este módulo marca la transición de prácticas de firmware procedurales en C hacia el desarrollo de software moderno y modular en Python, aplicando los principios de diseño SOLID y pruebas automatizadas.

## Instalación y Ejecución de Pruebas

Asegúrese de tener el entorno virtual activo:
```bash
source .venv/bin/activate
```

Para ejecutar la suite completa de pruebas unitarias (29 tests actuales) y verificar la cobertura de código:
```bash
PYTHONPATH=. pytest semana1/ -v --cov=semana1
```

Para verificar la calidad estética del código y consistencia de tipos:
```bash
ruff check semana1/
mypy semana1/ --ignore-missing-imports
```
## Reflexión Arquitectónica: SOLID en el Dominio de Sensores
Pasar del desarrollo embebido al software de alto nivel requiere romper con el acoplamiento duro al hardware. Los principios SOLID implementados en el uart_driver resuelven los vicios clásicos del código en C:

Single Responsibility Principle (SRP): en firmware es común ver un superloop o una ISR que lee el puerto, parsea la trama, escribe en una SD y prende un LED. Aquí, UartConfig solo valida parámetros, UartDevice controla la conexión y DataRecorder maneja la persistencia pura en JSON-lines. Cambiar el formato de guardado jamás romperá el transceptor.

Open/Closed Principle (OCP): el diseño está cerrado a la modificación pero abierto a la extensión. Gracias a la clase abstracta MessageParser, añadir un nuevo protocolo industrial (como CAN o un string propietario) no requiere tocar una sola línea del driver existente; basta con crear una nueva clase que herede de la base.

Liskov Substitution Principle (LSP): ModbusParser y NMEAParser son completamente intercambiables. La aplicación cliente puede tratarlos de manera uniforme bajo la abstracción base sin temor a excepciones inesperadas o comportamientos heterogéneos.

Interface Segregation Principle (ISP): mediante el uso de Protocol, dividimos interfaces robustas y monolíticas en contratos atómicos de grano fino (Readable, Writable). Un transductor que solo reporta lecturas de telemetría no es obligado a implementar lógica de escritura o calibración.

Dependency Inversion Principle (DIP): el controlador UartDevice no depende de parsers concretos; depende de la abstracción MessageParser. Esto rompe el acoplamiento con el hardware y permite inyectar componentes emulados (Mocks) durante las pruebas unitarias, logrando un entorno de ejecución 100% aislado y testeable en microsegundos.