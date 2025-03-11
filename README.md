# Tech Hub Web Application

## Description
The Tech Hub Web Application is a dynamic web-based platform that allows users to rent technical equipment, such as laptops and projectors. Users can browse available items, add them to their cart, and confirm bookings, while administrators can manage bookings, items, and user accounts. The application uses JSON and TXT files for data storage and manipulation.

## Features
### User Features:
- **User Registration:** New users can register using a username and password.
- **User Login:** Existing users can log in to view and manage their bookings.
- **Item Browsing:** Users can browse categories of technical items and view pricing.
- **Cart Management:** Users can add or remove items from their cart.
- **Booking Confirmation:** Users can confirm their bookings and view booking statuses.
- **Booking Status:** Displays whether a booking is `Pending`, `Granted`, or `Canceled`.
- **Logout:** Users can securely log out of the system.

### Admin Features:
- **Admin Login:** Admins can log in with a predefined username and password.
- **Portfolio Management:** Admins can add, update, and remove items available for booking.
- **Manage Bookings:** Admins can view all bookings, approve or cancel bookings, and clear specific bookings.
- **Registered Accounts:** Admins can view all registered user accounts.
- **Logout:** Admins can securely log out of the system.

## Project Setup
### Prerequisites:
- Python 3.x installed on your system.
- Flask library installed.
- Basic understanding of Python and Flask.

### Installation:
Clone the repository from GitHub:
```
git clone https://github.com/your-username/tech-hub-web-app.git
cd tech-hub-web-app
```

Install required Python packages:
```bash
pip install flask
```

Ensure the following files are present in the project directory:
- `portfolio.json`: Stores technical equipment data.
- `bookings.json`: Stores user booking information.
- `users.txt`: Stores registered user credentials.

If these files are missing, they will be initialized automatically when the application runs for the first time.

### Running the Application:
Start the Flask development server:
```
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## File Structure
```
tech-hub-web-app/
├── app.py                   # Main application file
├── portfolio.json           # Stores technical items
├── bookings.json            # Stores bookings
├── users.txt                # Stores user accounts
├── templates/               # HTML templates for the web pages
│   ├── about.html           # About page
│   ├── index.html           # Landing/Login page
│   ├── user.html            # User dashboard
│   ├── admin.html           # Admin dashboard
│   ├── register.html        # User registration page
│   ├── confirmation.html    # Booking confirmation page
│   ├── booking.html         # Booking management page for admin
│   ├── accounts.html        # View registered user accounts
│   ├── Cart_.html           # Empty cart fallback template
├── static/                  # Static files
│   ├── styles.css           # Styling for the app
│   ├── images/              # Images for the project (e.g., bg.jpg)
```

## How It Works
### User Flow:
1. **Register/Login:**
   - New users register their account using the Register page.
   - Existing users can log in using valid credentials.
2. **Browse Items:**
   - View available items categorized by type (e.g., laptops, projectors).
3. **Add Items to Cart:**
   - Add desired items to the cart.
4. **Confirm Booking:**
   - Confirm the booking and wait for admin approval.
5. **View Status:**
   - View the status of the booking as `Pending`, `Granted`, or `Canceled`.

### Admin Flow:
1. **Admin Login:**
   - Admin logs in using predefined credentials (default: `admin/admin123`).
2. **Manage Portfolio:**
   - Add, update, or remove items from the portfolio.
3. **Manage Bookings:**
   - Approve or cancel user bookings.
   - Clear individual bookings if necessary.
4. **View User Accounts:**
   - View all registered users on the platform.


## Technologies Used
- **Backend:** Python (Flask framework)
- **Frontend:** HTML, CSS (Bootstrap optionally)
- **Data Storage:** JSON and TXT files

## Future Enhancements
- Transition to a database like SQLite3 for more robust data handling.
- Add email notifications for booking statuses.
- Implement a password recovery mechanism.
- Optimize the UI for mobile responsiveness.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions or bug reports.
