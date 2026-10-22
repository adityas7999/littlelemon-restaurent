Little Lemon Restaurant - Capstone Project API Endpoints
======================================================

Peers can test the following API endpoints using Insomnia, Postman, or curl:

1. User Registration:
   /api/registration/
   (POST - Body: {"username": "your_username", "email": "your_email@example.com", "password": "your_password"})
   Alternative Djoser endpoint: /auth/users/

2. User Authentication (Token Generation):
   /api/token/login/
   (POST - Body: {"username": "your_username", "password": "your_password"})
   Alternative endpoints: /api-token-auth/ and /auth/token/login/
   Returns: {"token": "<auth_token>"} or {"auth_token": "<auth_token>"}

3. Food Menu API:
   /api/menu-items/
   - GET /api/menu-items/ (List all food menu items - Public)
   - POST /api/menu-items/ (Add a new menu item - Requires 'Authorization: Token <token>' header)
     Body: {"title": "Greek Salad", "price": "12.00", "inventory": 20}
   - GET /api/menu-items/{id}/ (Retrieve single item by id)
   - PUT /api/menu-items/{id}/ (Update menu item - Requires token)
   - DELETE /api/menu-items/{id}/ (Delete menu item - Requires token)
   Alternative endpoints: /restaurant/menu/ and /api/menu/

4. Table Booking API (Secured):
   /api/bookings/
   Requires Header: 'Authorization: Token <your_auth_token>'
   - GET /api/bookings/ (List all table reservations)
   - POST /api/bookings/ (Create a new table reservation)
     Body: {"name": "John Doe", "no_of_guests": 4, "booking_date": "2026-11-20T19:00:00Z"}
   - GET /api/bookings/{id}/ (Retrieve single booking details)
   - PUT /api/bookings/{id}/ (Update reservation)
   - DELETE /api/bookings/{id}/ (Cancel reservation)
   Alternative endpoints: /api/tables/ and /restaurant/booking/tables/

5. Static HTML Web Application Pages:
   / (Home page serving static HTML, CSS, and images)
   /about/ (About page)
   /menu/ (Interactive menu page)
   /book/ (Interactive table booking page)
   /reservations/ (Reservation overview page)
   /register/ (User registration form page)

Demo Reviewer Credentials:
--------------------------
Admin / Superuser:
Username: admin
Password: LemonAdmin2026!

Customer:
Username: customer
Password: LemonCustomer2026!
