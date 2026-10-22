# OOAD and UML Documentation
## E-Commerce Marketplace

## 1. Introduction

Object-Oriented Analysis and Design (OOAD) is an approach used to analyze system requirements and organize the design of software applications. The Unified Modeling Language (UML) provides diagrams to represent the structure, behavior, and interactions of a system.

The E-Commerce Marketplace is a web-based application developed using Python, Flask, SQLite, HTML, CSS, and JavaScript. It allows users to browse products, manage a shopping cart, enter delivery details, place orders, and view order confirmations.

## 2. Objectives

The main objectives of the project are:

- To provide a user-friendly online shopping interface.
- To support user registration and login.
- To display available products and their prices.
- To provide shopping cart management.
- To collect delivery information during checkout.
- To store order and order-item information in a database.
- To update product stock after successful order placement.
- To display order confirmation to the user.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Relational database |
| HTML | Web page structure |
| CSS | Styling and layout |
| JavaScript | Client-side interactions |
| Git | Version control |
| GitHub | Source code hosting |
| Visual Studio Code | Development environment |
| diagrams.net (draw.io) | UML diagram creation |

## 4. System Overview

The application follows a browser-based architecture. The user interacts with the web interface, Flask processes requests and application logic, and SQLite stores persistent data.

The main shopping workflow is:

1. Open the marketplace.
2. Register or log in.
3. Browse available products.
4. Add products to the shopping cart.
5. Review cart items and the total.
6. Enter delivery details.
7. Validate product availability.
8. Create the order and order items.
9. Update product stock.
10. Clear the shopping cart and display confirmation.

The shopping cart is maintained using Flask session data, according to the described application workflow.

## 5. Functional Requirements

The system should support the following functions:

- User registration and login.
- Product browsing.
- Shopping cart management.
- Cart total calculation.
- Delivery information entry.
- Product stock validation.
- Order creation.
- Order-item storage.
- Inventory updates.
- Order confirmation.

## 6. Use Case Diagram

**Purpose:** The Use Case Diagram represents the interactions between the buyer and the marketplace.

**Actor:** Buyer

**Main use cases:**
- Register / Log In
- Browse Products
- Manage Shopping Cart
- Review Cart and Total
- Enter Delivery Details
- Validate Stock
- Place Order
- View Order Confirmation

**Diagram:** Open the `Ecommerce_Marketplace_UML_Diagrams.drawio` file and select the **Use Case** page.

## 7. Class Diagram and Database Model

The conceptual data model is based on the four application tables identified in the existing SQLite database.

### 7.1 User

| Attribute | Description |
|---|---|
| id | Primary key |
| name | User name |
| email | User email |
| password_hash | Hashed password |

### 7.2 Product

| Attribute | Description |
|---|---|
| id | Primary key |
| name | Product name |
| category | Product category |
| price | Product price |
| stock | Available stock quantity |

### 7.3 Order

| Attribute | Description |
|---|---|
| id | Primary key |
| user_id | Associated user identifier |
| customer_name | Customer name |
| email | Customer email |
| address | Delivery address |
| city | Delivery city |
| postal_code | Delivery postal code |
| total | Order total |
| status | Order status |
| created_at | Order creation timestamp |

### 7.4 OrderItem

| Attribute | Description |
|---|---|
| id | Primary key |
| order_id | Associated order identifier |
| product_id | Associated product identifier |
| product_name | Product name recorded for the order |
| price | Recorded item price |
| quantity | Quantity ordered |
| subtotal | Subtotal for the item |

### 7.5 Relationships

The intended relationships are:

- One user can place multiple orders.
- One order can contain multiple order items.
- One product can be referenced by multiple order items.
- Each order item belongs to an order and references a product.

These relationships should be checked against the actual SQLite foreign-key constraints and application code.

**Diagram:** Open the `Class Diagram` page in the draw.io file.

## 8. Activity Diagram — Checkout Process

The Activity Diagram represents the sequence of actions performed during checkout.

**Main activities:**

1. Start.
2. Open shopping cart.
3. Check whether the cart is empty.
4. Display an empty-cart message if necessary.
5. Review products and total.
6. Enter delivery details.
7. Validate required fields.
8. Check product stock.
9. Create the order and order items.
10. Update stock.
11. Clear the cart.
12. Display order confirmation.

Validation failures and insufficient stock should prevent an invalid order from being completed.

**Diagram:** Open the `Checkout Activity` page in the draw.io file.

## 9. Sequence Diagram — Order Placement

The Sequence Diagram illustrates the interactions between the buyer, browser, Flask application, SQLite database, and session cart during checkout.

**Interaction flow:**

1. The buyer submits checkout details.
2. The browser sends the checkout request to Flask.
3. Flask validates the request and checks product stock.
4. Flask creates the order record.
5. Flask stores the order items.
6. Product stock is updated.
7. The shopping cart session is cleared after successful order placement.
8. The application returns the order confirmation response.

The sequence should reflect the actual route implementation and database operations.

**Diagram:** Open the `Order Sequence` page in the draw.io file.

## 10. Component Diagram

The Component Diagram represents the major software components.

| Component | Responsibility |
|---|---|
| Web Browser | Displays the marketplace interface |
| HTML Templates | Provides page structure |
| CSS and JavaScript | Handles presentation and client-side interactions |
| Flask Routes and Business Logic | Processes requests and executes application logic |
| Authentication and Session | Supports user sessions and cart state |
| Checkout and Inventory Logic | Handles order processing and stock updates |
| SQLite Database | Stores users, products, orders, and order items |

**Diagram:** Open the `Component Diagram` page in the draw.io file.

## 11. Deployment Diagram

The Deployment Diagram represents the local development environment.

**Deployment components:**

- **Client Device:** Runs the web browser.
- **Developer Computer:** Runs the Python application.
- **Flask Development Server:** Handles HTTP requests.
- **SQLite Database File:** Stores persistent application data.
- **Development Tools:** Visual Studio Code and the Python runtime.

The browser communicates with the Flask server, and Flask reads from and writes to the SQLite database file.

**Diagram:** Open the `Deployment Diagram` page in the draw.io file.

## 12. Database Design

The existing database contains these application tables:

- `users`
- `products`
- `orders`
- `order_items`

SQLite also maintains an internal table named `sqlite_sequence` when applicable to autoincrementing primary keys.

The database schema should be maintained in `schema.sql` and checked against the actual database structure and SQL statements used by the application. Existing database tables should not be recreated or modified without backing up the database first.

## 13. Limitations

- A real online payment gateway is not included in the described checkout workflow.
- Seller management, product reviews, and administrator functionality must be verified before being claimed as implemented.
- The application is documented for local development using Flask and SQLite.
- Production deployment would require additional security, configuration, testing, and operational controls.
- Database relationships and foreign-key enforcement must be verified against the actual database.

## 14. Future Enhancements

Possible future improvements include:

- Integration with a secure payment gateway.
- Seller product management.
- Product ratings and reviews.
- Administrator dashboard.
- Order tracking and delivery status.
- Additional input validation and security controls.
- Automated tests.
- Production deployment.

## 15. Conclusion

The E-Commerce Marketplace demonstrates a web-based shopping workflow using Flask and SQLite. The OOAD documentation describes the system's requirements, conceptual data model, checkout activities, interactions, software components, and local deployment environment.

The UML diagrams provide a visual representation of the application's structure and behavior. Before final submission, all diagrams and database documentation should be checked against the final source code and database implementation.

## 16. Project Repository

GitHub: https://github.com/akhilXbuilds/ecommerce-marketplace
