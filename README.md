# Little Lemon Restaurant — Meta Back-End Developer Capstone

A full-stack restaurant web application and RESTful API backend built with **Python**, **Django**, and **Django REST Framework (DRF)** for the Little Lemon restaurant.

---

## Peer Review Checklist & Features

This project satisfies all peer evaluation criteria of the Coursera Meta Back-End Developer Capstone:

- [x] **Static HTML Content:** Django serves static HTML content (`index.html`, `about.html`, `menu.html`, `book.html`, `bookings.html`, `register.html`) with CSS styles and images.
- [x] **Git Repository:** Fully tracked in Git with structured commits and pushed to GitHub under repository `littlelemon-restaurent`.
- [x] **MySQL Database Connection:** Configured for MySQL by default (`django.db.backends.mysql`) in `littlelemon/settings.py` with automatic/configurable SQLite fallback for flexible local testing.
- [x] **Menu & Table Booking APIs:** Complete CRUD endpoints implemented using DRF generics and viewsets (`MenuItemsView`, `SingleMenuItemView`, `BookingViewSet`).
- [x] **User Registration & Authentication:** Built-in registration API (`/api/registration/`), HTML registration page (`/register/`), Djoser auth (`/auth/users/`), and Token Authentication (`/api/token/login/`, `/auth/token/login/`).
- [x] **Secured Table Booking API:** Table reservations are protected with `permission_classes = [IsAuthenticated]`.
- [x] **Unit Tests:** Automated unit tests covering models and API views pass cleanly (`18 passed`).
- [x] **Insomnia REST Client:** Includes `Insomnia_LittleLemon_API.json` ready for one-click import and testing in Insomnia.
- [x] **Readme.txt:** Includes `Readme.txt` in the root repository listing all API paths to test.

---

## Tech Stack

- **Framework:** Django 5.x, Django REST Framework 3.16+
- **Authentication:** Token Authentication (`rest_framework.authtoken`), Djoser
- **Database:** MySQL (`mysqlclient`) & SQLite
- **Frontend:** Django Templates, HTML5, CSS3, Vanilla JavaScript

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/adityas7999/littlelemon-restaurent.git
cd littlelemon-restaurent
```

### 2. Set Up Virtual Environment & Dependencies

Using standard `pip`:
```bash
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Or using `pipenv`:
```bash
pipenv install
pipenv shell
```

---

## Database Configuration

### Option A: MySQL (Default / Rubric Requirement)
1. Ensure your MySQL server is running (port 3306).
2. Create the database:
   ```sql
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Set your local MySQL credentials in your environment (PowerShell example):
   ```powershell
   $env:MYSQL_DATABASE = "littlelemon"
   $env:MYSQL_USER = "root"
   $env:MYSQL_PASSWORD = "your-password"
   $env:MYSQL_HOST = "127.0.0.1"
   $env:MYSQL_PORT = "3306"
   ```

### Option B: SQLite (Quick Local Testing)
For quick local testing or environments without a running MySQL server:
```powershell
$env:LITTLELEMON_DB_ENGINE = "sqlite"
```

---

## Running Migrations & Seeding Demo Data

Apply migrations:
```bash
python manage.py migrate
```

Seed initial sample menu items, reservations, and demo accounts:
```bash
python manage.py seed_data
```

This creates:
- **Admin account:** `admin` / `LemonAdmin2026!`
- **Customer account:** `customer` / `LemonCustomer2026!`
- Sample menu items (Greek Salad, Bruschetta, Grilled Fish, etc.)
- Sample table bookings

---

## Starting the Application

```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## Web Pages (Static & HTML Content)

- `/` — Little Lemon Home page (Static HTML, CSS, images)
- `/about/` — About Little Lemon
- `/menu/` — Restaurant menu display
- `/book/` — Interactive table reservation form
- `/reservations/` — Overview of reservations
- `/register/` — User account registration form
- `/admin/` — Django Administration dashboard

---

## API Endpoints

### 1. Authentication & Registration
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/token/login/` | Obtain token for user | No |
| POST | `/auth/users/` | Djoser user registration | No |
| POST | `/auth/token/login/` | Djoser token login | No |

**Example Registration Payload:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "SecretPassword123!"
}
```

### 2. Menu Items API
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/menu-items/` | List all menu items | No |
| POST | `/api/menu-items/` | Create a new menu item | Yes (Token) |
| GET | `/api/menu-items/{id}/` | Retrieve single menu item | No |
| PUT | `/api/menu-items/{id}/` | Update menu item | Yes (Token) |
| DELETE | `/api/menu-items/{id}/` | Delete menu item | Yes (Token) |

*(Note: Also routed at `/restaurant/menu/` and `/api/menu/` for compatibility).*

**Example Menu Creation Payload:**
```json
{
  "title": "Greek Salad",
  "price": "12.00",
  "inventory": 20
}
```

### 3. Table Bookings API (Secured)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/bookings/` | List all table bookings | Yes (Token) |
| POST | `/api/bookings/` | Create a new reservation | Yes (Token) |
| GET | `/api/bookings/{id}/` | Retrieve reservation details | Yes (Token) |
| PUT | `/api/bookings/{id}/` | Update reservation | Yes (Token) |
| DELETE | `/api/bookings/{id}/` | Cancel reservation | Yes (Token) |

*(Note: Also routed at `/api/tables/` and `/restaurant/booking/tables/`).*

**Example Booking Creation Payload:**
```json
{
  "name": "John Doe",
  "no_of_guests": 4,
  "booking_date": "2026-11-25T19:30:00Z"
}
```

**Authentication Header:**
```
Authorization: Token <your_auth_token>
```

---

## Running Automated Unit Tests

Run the full automated test suite:
```bash
python manage.py test
```

The test suite validates:
- `MenuItemTest`: Model creation and string representation (`str(item) == "IceCream : 80"`).
- `MenuViewTest`: Menu items list endpoint, token-secured creation, and data serialization.
- `BookingModelTest`: Table booking model creation and formatting.
- `BookingApiTest`: Table booking API authorization rejection (401) and token-authenticated booking creation (201).
- `UserRegistrationApiTest`: User registration API.
- `StaticContentPagesTest`: Delivery of static HTML pages (`/`, `/about/`, `/menu/`, `/book/`, etc.).

---

## Testing with Insomnia REST Client

1. Open **Insomnia**.
2. Click **Create** / **Import** -> **From File**.
3. Select `Insomnia_LittleLemon_API.json` from the repository root.
4. Execute the pre-configured requests (Registration, Login, Menu CRUD, Bookings CRUD).
