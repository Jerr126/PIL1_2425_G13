# PIL1 2425 G13 Backend

## Description
This project is a Django-based backend for a ride-sharing application. It supports two user roles: passenger and driver. Each user can switch between these roles and will receive notifications and messaging capabilities based on their current role.

## Features
- User authentication and role management (passenger/driver)
- Notification system for ride requests and responses
- Messaging system for communication between passengers and drivers
- RESTful API endpoints for user, ride, notification, and messaging management

## Project Structure
```
pil1_2425_g13_backend
├── manage.py
├── pil1_2425_g13_backend
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── rides
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── notifications
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── messaging
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd pil1_2425_g13_backend
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Users can register and log in to the application.
- Users can switch between passenger and driver modes.
- Notifications will be displayed based on the current user role.
- Messaging is enabled only when a ride request is accepted.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License.