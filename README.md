# The Waitlist Application

A comprehensive waitlist management project featuring both an **object-oriented Python CLI/demonstration system** leveraging [`ingabotool`](https://pypi.org/project/ingabotool/) and a **full-featured Django web application** for managing waitlist registrations.

---

## 🌟 Key Features

### 1. Python OOP Waitlist System (with `ingabotool`)
- **Robust Data Validation**: Validates user email addresses before queueing.
- **Slugification & ID Generation**: Automatically normalizes user handles and generates unique user/referral codes.
- **Privacy Protection**: Masks email addresses on public leaderboards and waitlist displays.
- **Clean CLI Formatting**: Truncates usernames to keep CLI terminal output cleanly aligned.
- **SQLite Persistence**: Stores queue entries persistently using a dedicated `StorageManager`.

### 2. Django Web Application
- **Full CRUD Waitlist Operations**: Create, view, update, and remove waitlist entries via web UI.
- **Modular Django Architecture**: Built with `waitlist_app`, `listproduct`, and `anotherapp`.
- **Admin Interface**: Built-in Django administration for monitoring queue submissions.

---

## 🛠️ How `ingabotool` is Leveraged

The CLI demonstration highlights all 5 core utilities of the [`ingabotool`](https://pypi.org/project/ingabotool/) package:

1. **`is_valid_email(email)`**: Validates user email formatting before any registration is processed.
2. **`slugify(text)`**: Normalizes human usernames into clean, standardized URL-safe handles (e.g., `"Alice In Wonderland"` ➔ `"alice-in-wonderland"`).
3. **`generate_id(prefix)`**: Generates unique identifiers for users (`usr_...`) and referral codes (`ref_...`).
4. **`mask_email(email)`**: Obfuscates email addresses for public waitlist displays to protect user privacy (e.g., `"a****@wonderland.com"`).
5. **`truncate(text, max_length)`**: Shortens long usernames cleanly so formatted CLI/web tables stay aligned without clipping.

---

## 📂 Project Architecture

```text
thewaitlist/
├── main.py                  # Interactive CLI & automated demonstration suite
├── user.py                  # User domain model integrating ingabotool
├── waitlist.py              # Waitlist business logic & validation rules
├── waitlist_manager.py      # Manager layer for waitlist operations
├── storage.py               # StorageManager handling SQLite database queries
├── manage.py                # Django CLI administrative entry point
├── waitlist/                # Django project settings and root routing
├── waitlist_app/            # Django app for waitlist CRUD operations
├── listproduct/             # Django app for product listing
├── anotherapp/              # Additional supporting Django app
├── data/                    # SQLite database storage directory
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites & Installation

Clone the repository and install the dependencies:
```bash
git clone https://github.com/IGITANGAZA23/thewaitlist.git
cd thewaitlist
pip install -r requirements.txt
```

---

### 2. Running the Python OOP Waitlist (CLI)

#### Automated Feature Demonstration:
Run the comprehensive automated test suite and feature demo:
```bash
python main.py --demo
```

#### Interactive CLI Menu:
Launch the interactive console menu:
```bash
python main.py
```
**Available Menu Options:**
- **1. Join Waitlist**: Register username, email, and optional referral code.
- **2. Check Queue Position**: Lookup queue rank by email.
- **3. View Public Waitlist**: View leaderboard with masked emails for privacy.
- **4. View Waitlist (Admin)**: View complete unmasked administrative queue.
- **5. View Stats**: Check total registrations.
- **6. Remove User (Admin)**: Remove an entry.

---

### 3. Running the Django Web Application

Apply database migrations:
```bash
python manage.py migrate
```

Start the local development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Waitlist Home / List**: `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/waitlist/`
- **Django Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## 🛡️ Privacy & Security

- **Public Display Privacy**: Public views use obfuscated emails (e.g., `a****@domain.com`) to protect user identities.
- **Referral Integrity**: Referral codes are uniquely generated and verified to prevent duplicate records.

---

## 📄 License

This project is developed for educational and practical demonstrations.
