# E-Commerce Marketplace

A web-based e-commerce marketplace developed using Python, Flask, SQLite, HTML, CSS, and JavaScript. The application allows users to browse products, manage their shopping cart, enter delivery details, and place orders.

## 1. Project Overview

The E-Commerce Marketplace provides a simple platform for product browsing and order management. It uses Flask for backend routing and application logic, SQLite for data storage, and HTML, CSS, and JavaScript for the user interface.

### Objectives

- Provide a user-friendly shopping interface.
- Support user registration and login.
- Display available products.
- Allow users to add, update, and remove cart items.
- Calculate order totals.
- Collect customer delivery information.
- Create orders and order items.
- Update product stock after successful order placement.
- Provide an order confirmation page.

### Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling and layout |
| JavaScript | Client-side interactions |
| Git | Version control |
| GitHub | Source code hosting |
| Visual Studio Code | Development environment |

## 2. System Modules

1. **Buyer Module:** User registration, login, product browsing, cart management, and checkout.
2. **Seller Module:** Seller-related functionality, if implemented in the current application.
3. **Inventory Module:** Product information and stock management.
4. **Cart Module:** Adding products, changing quantities, removing products, and calculating cart totals.
5. **Orders Module:** Saving orders and associated order items.
6. **Payments Module:** The current checkout flow does not collect online payment. Payment processing is not implemented as a real payment gateway.
7. **Delivery Module:** Collecting the customer's name, email, address, city, and postal code.
8. **Reviews Module:** Product review functionality, if implemented.
9. **Admin Module:** Administrative functionality, if implemented.

Only modules implemented in the current source code should be presented as completed features.

## 3. OOAD and UML Documentation

Object-Oriented Analysis and Design (OOAD) is used to analyze the system requirements, identify actors and objects, and represent the system's structure and behavior using Unified Modeling Language (UML).

### 3.1 Use-Case Diagram

**Primary actor:** Buyer

Potential use cases include:

- Register an account
- Log in
- Browse products
- Manage shopping cart
- Proceed to checkout
- Enter delivery details
- Place an order
- View order confirmation

Additional actors, such as sellers and administrators, should be included only if the corresponding functionality exists.

### 3.2 Class Diagram

The following conceptual classes can be used to model the main entities of the marketplace:

- **User:** user ID and account information.
- **Product:** product ID, name, price, and stock.
- **Cart:** selected products and quantities.
- **Order:** order ID, customer information, and total.
- **OrderItem:** product details, quantity, price, and subtotal.
- **DatabaseConnection:** provides database access.

These are conceptual entities for documentation. Their exact attributes, methods, and relationships must be aligned with the implementation.

### 3.3 Activity Diagram — Order Placement

Start  
↓  
Browse Products  
↓  
Add Products to Cart  
↓  
Review Cart  
↓  
Proceed to Checkout  
↓  
Is the Cart Empty?

- Yes → Display Message → Return to Shopping
- No → Enter Delivery Details

↓  
Validate Delivery Details  
↓  
Check Product Availability  
↓  
Is Sufficient Stock Available?

- No → Display Stock Error → Update Cart
- Yes → Create Order

↓  
Save Order Items  
↓  
Update Product Stock  
↓  
Clear Shopping Cart  
↓  
Display Order Confirmation  
↓  
End

### 3.4 Sequence Diagram — Checkout

**Participants:** Buyer, Flask Application, SQLite Database.

1. Buyer requests the checkout page.
2. Flask retrieves the cart and product information.
3. SQLite returns the matching product records.
4. Flask calculates the order total and displays checkout.
5. Buyer submits delivery information.
6. Flask validates the required fields.
7. Flask checks current product stock.
8. Flask saves the order and order items.
9. Flask updates product stock.
10. Flask clears the session cart.
11. Flask redirects the buyer to the order confirmation page.

### 3.5 Component Diagram

Conceptual components:

- User Interface: HTML templates and CSS.
- Client-Side Logic: JavaScript.
- Application Layer: Flask routes and business logic.
- Data Layer: SQLite database.
- Browser: Displays the marketplace and sends HTTP requests.

### 3.6 Deployment Diagram

The application can be deployed in a simple local development environment:

- Client device: Web browser.
- Development environment: Visual Studio Code and Python.
- Application server: Flask development server.
- Database: SQLite database file.

The browser communicates with Flask over HTTP, and Flask reads and writes data through SQLite.

## 4. Prerequisites

Install the following on Windows before running the project:

- Python 3
- Git
- Visual Studio Code
- A web browser

Verify Python and Git in a terminal:

```powershell

python --version
git --version

```

## 5. Import the Project into VS Code

### Step 1: Clone the GitHub repository

Open PowerShell or the VS Code terminal and execute:

```powershell

git clone https://github.com/akhilXbuilds/ecommerce-marketplace.git

```

### Step 2: Open the project folder

```powershell

cd ecommerce-marketplace
code .

```

If `code .` is unavailable, open VS Code and select **File → Open Folder**, then select the cloned `ecommerce-marketplace` folder.

### Step 3: Create a virtual environment

Run the following command from the project root:

```powershell

python -m venv venv

```

### Step 4: Activate the virtual environment

```powershell

.\venv\Scripts\Activate.ps1

```

If PowerShell blocks activation, use Command Prompt and run:

```bat

venv\Scripts\activate.bat

```

Alternatively, for the current PowerShell session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 6. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install Flask:

```powershell
python -m pip install flask
```

If additional third-party libraries are imported by `app.py`, install those dependencies as well. If a `requirements.txt` file is added to the repository, use:

```powershell
python -m pip install -r requirements.txt
```

## 7. Database Initialization

The application uses SQLite for persistent storage.

The database initialization process must be verified in `app.py` before first execution. If the application creates tables automatically, start the app using the instructions below. If manual initialization is required, ensure the SQL schema is complete before running it.

The `schema.sql` file must contain the appropriate table definitions before it is used to initialize the database.

## 8. Execute the Project

Ensure that the virtual environment is activated and the terminal is in the project root.

Run:

```powershell
python app.py
```

After Flask starts successfully, open the local URL displayed in the terminal. The default address is commonly:

http://127.0.0.1:5000/

Use the application through the browser.

To stop the development server, press:

```text
Ctrl + C
```

## 9. Main Application Workflow

1. Open the marketplace in a browser.
2. Register or log in.
3. Browse the available products.
4. Add products to the shopping cart.
5. Modify quantities or remove products as needed.
6. Proceed to checkout.
7. Enter the required delivery details.
8. Confirm the order.
9. View the order confirmation page.

## 10. Version Control

GitHub repository:

https://github.com/akhilXbuilds/ecommerce-marketplace

To check the working tree:

```powershell
git status
```

To save future changes:

```powershell
git add .
git commit -m "Describe your changes"
git push
```

Do not commit virtual environments, secret credentials, environment files, or private database records.

## 11. Limitations

- Online payment gateway integration is not currently implemented.
- Seller, review, and administrator features must be verified against the actual source code.
- The Flask development server is intended for development and demonstration, not production hosting.
- Production deployment would require additional security, configuration, and operational controls.

## 12. Future Enhancements

- Integrate a secure payment gateway.
- Add seller product management.
- Add product ratings and reviews.
- Develop an administrator dashboard.
- Add order tracking and delivery status.
- Improve input validation and application security.
- Add automated tests and deployment configuration.

## 13. Conclusion

The E-Commerce Marketplace demonstrates the integration of a Python Flask backend, SQLite database, and browser-based frontend. The application supports core shopping operations, cart management, checkout, order creation, inventory updates, and order confirmation. OOAD and UML provide a structured way to document the system's requirements, architecture, and workflows.
