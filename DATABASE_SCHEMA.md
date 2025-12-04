# Esquema de Base de Datos - Networking Backend

## Descripción General

Este documento contiene la estructura completa de las tablas de la base de datos del sistema de networking. El sistema utiliza SQLModel (SQLAlchemy con Pydantic) y puede estar configurado con SQLite o PostgreSQL.

---

## Tablas de la Base de Datos

### 1. **User** (Tabla Principal)

Almacena la información de los usuarios del sistema (personas, empresas y administradores).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del usuario |
| `email` | String | UNIQUE, NOT NULL, Indexed | Correo electrónico del usuario |
| `full_name` | String | NULL | Nombre completo del usuario |
| `hashed_password` | String | NOT NULL | Contraseña hasheada (no se guarda en texto plano) |
| `is_active` | Boolean | DEFAULT: True | Indica si el usuario está activo |
| `is_verified` | Boolean | DEFAULT: False | Indica si el usuario ha verificado su email |
| `role` | Enum | DEFAULT: "person" | Rol del usuario: `person`, `company`, `admin` |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de creación del registro |

**Relaciones:**
- One-to-Many con `UserSkill`
- One-to-Many con `UserHobby`
- One-to-Many con `Preference`
- One-to-Many con `ActivityLog`
- One-to-Many con `JobApplication`

---

### 2. **Skill** (Habilidades)

Almacena las habilidades disponibles en el sistema.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único de la habilidad |
| `name` | String | NOT NULL, Indexed, UNIQUE | Nombre de la habilidad |
| `type` | Enum | DEFAULT: "hard" | Tipo de habilidad: `hard` (técnica) o `soft` (blanda) |

**Relaciones:**
- One-to-Many con `UserSkill` (inversa)

---

### 3. **UserSkill** (Tabla Intermedia: Usuario-Habilidad)

Tabla de relación many-to-many entre usuarios y habilidades.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `user_id` | Integer | FOREIGN KEY (user.id), PRIMARY KEY | ID del usuario |
| `skill_id` | Integer | FOREIGN KEY (skill.id), PRIMARY KEY | ID de la habilidad |
| `level` | Integer | DEFAULT: 1, NULL | Nivel de dominio (recomendado 1-5) |
| `endorsements` | Integer | DEFAULT: 0 | Número de recomendaciones recibidas |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de asignación de la habilidad |

**Relaciones:**
- Many-to-One con `User`
- Many-to-One con `Skill`

---

### 4. **Hobby** (Pasatiempos)

Almacena los pasatiempos disponibles en el sistema.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del pasatiempo |
| `name` | String | NOT NULL, Indexed | Nombre del pasatiempo |

**Relaciones:**
- One-to-Many con `UserHobby` (inversa)

---

### 5. **UserHobby** (Tabla Intermedia: Usuario-Pasatiempo)

Tabla de relación many-to-many entre usuarios y pasatiempos.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del registro |
| `user_id` | Integer | FOREIGN KEY (user.id), NOT NULL | ID del usuario |
| `hobby_id` | Integer | FOREIGN KEY (hobby.id), NOT NULL | ID del pasatiempo |

**Relaciones:**
- Many-to-One con `User`
- Many-to-One con `Hobby`

---

### 6. **Preference** (Preferencias del Usuario)

Almacena las preferencias personalizadas de cada usuario (trabajo remoto, salario, etc.).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único de la preferencia |
| `user_id` | Integer | FOREIGN KEY (user.id), NOT NULL | ID del usuario propietario de la preferencia |
| `key` | String | NOT NULL | Clave de la preferencia (e.g., "remote", "looking_for", "salary_min") |
| `value` | String | NOT NULL | Valor de la preferencia (se puede guardar como JSON) |

**Relaciones:**
- Many-to-One con `User`

---

### 7. **ActivityLog** (Registro de Actividades)

Registra todas las actividades del usuario en el sistema para auditoría y análisis.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del registro |
| `user_id` | Integer | FOREIGN KEY (user.id), NOT NULL | ID del usuario que realizó la actividad |
| `type` | Enum | NOT NULL | Tipo de actividad: `login`, `apply_job`, `view_job`, `message_sent`, `profile_update` |
| `details` | String | NULL | Detalles adicionales de la actividad |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha y hora de la actividad |

**Relaciones:**
- Many-to-One con `User`

---

### 8. **JobApplication** (Solicitudes de Empleo)

Registra las solicitudes de empleos realizadas por los usuarios.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único de la solicitud |
| `user_id` | Integer | FOREIGN KEY (user.id), NOT NULL, Indexed | ID del usuario solicitante |
| `job_id` | Integer | NOT NULL, Indexed | ID del empleó (referencia a servicio externo de empleos) |
| `status` | Enum | DEFAULT: "applied" | Estado de la solicitud: `applied`, `interviewed`, `hired`, `rejected` |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de creación de la solicitud |
| `updated_at` | DateTime | DEFAULT: UTC now | Fecha de última actualización |

**Relaciones:**
- Many-to-One con `User`

---

### 9. **AdminMonitor** (Monitoreo de Administradores)

Registra el monitoreo o supervisión que los administradores realizan sobre usuarios específicos.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del monitoreo |
| `admin_id` | Integer | FOREIGN KEY (user.id), NOT NULL, Indexed | ID del administrador |
| `person_id` | Integer | FOREIGN KEY (user.id), NOT NULL, Indexed | ID de la persona monitoreada |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de inicio del monitoreo |

**Relaciones:**
- Many-to-One con `User` (como admin)
- Many-to-One con `User` (como persona monitoreada)

---

### 10. **Conversation** (Conversaciones)

Almacena las conversaciones entre usuarios.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único de la conversación |
| `title` | String | NULL | Título opcional de la conversación |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de creación de la conversación |

**Relaciones:**
- One-to-Many con `Message` (inversa)

---

### 11. **Message** (Mensajes)

Almacena los mensajes dentro de las conversaciones.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|----|
| `id` | Integer | PRIMARY KEY, Auto-incremental | Identificador único del mensaje |
| `conversation_id` | Integer | FOREIGN KEY (conversation.id), NOT NULL, Indexed | ID de la conversación |
| `sender_id` | Integer | FOREIGN KEY (user.id), NOT NULL, Indexed | ID del remitente del mensaje |
| `content` | String | NOT NULL | Contenido del mensaje |
| `created_at` | DateTime | DEFAULT: UTC now | Fecha de envío del mensaje |
| `read` | Boolean | DEFAULT: False | Indica si el mensaje ha sido leído |

**Relaciones:**
- Many-to-One con `Conversation`
- Many-to-One con `User` (como remitente)

---

## Enums Utilizados

### UserRole
```
- person   (Persona individual)
- company  (Empresa)
- admin    (Administrador)
```

### SkillType
```
- hard  (Habilidad técnica)
- soft  (Habilidad blanda)
```

### ActivityType
```
- login
- apply_job
- view_job
- message_sent
- profile_update
```

### JobApplicationStatus
```
- applied      (Solicitud presentada)
- interviewed  (Entrevista realizada)
- hired        (Contratado)
- rejected     (Rechazado)
```

---

## Diagrama de Relaciones

```
User (1) ──→ (Many) UserSkill
         ──→ (Many) UserHobby
         ──→ (Many) Preference
         ──→ (Many) ActivityLog
         ──→ (Many) JobApplication
         ──→ (Many) Message
         ──→ (Many) AdminMonitor (como admin_id)
         ──→ (Many) AdminMonitor (como person_id)

Skill (1) ──→ (Many) UserSkill

Hobby (1) ──→ (Many) UserHobby

Conversation (1) ──→ (Many) Message
```

---

## Notas Técnicas

- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Base de Datos:** SQLite (desarrollo) o PostgreSQL (producción)
- **Timestamps:** Todos los registros utilizan `datetime.utcnow()` para mayor consistencia
- **Índices:** Optimizados para búsquedas frecuentes por `email`, `user_id`, `job_id`, `conversation_id`, `sender_id`
- **Foreign Keys:** Todas las relaciones están definidas con constraints de clave foránea

---

**Última actualización:** 4 de diciembre de 2025
