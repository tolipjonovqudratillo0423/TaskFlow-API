

<details>
<summary><b>📋 Базовая структура таблицы Membership</b></summary>
<br>

| Поле | Тип данных | Описание |
| :--- | :--- | :--- |
| `joined_at` | `Timestamp` | 📅 Дата и время вступления |
| `invited_by` | `User_ID` (FK) | 👤 Кто пригласил пользователя |
| `status` | `Enum` | 🟢 `Pending` \| `Active` \| `Suspended` |
| `role` | `Enum` | 👑 `Owner` \| `Admin` \| `Member` |
| `organization` | `Org_ID` (FK) | 🏢 Ссылка на организацию |
| `user` | `User_ID` (FK) | 🔑 Ссылка на аккаунт пользователя |

</details>
