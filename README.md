# Shopping-App-Backend-using-Flask
This Flask application serves as a simple online marketplace with user and admin functionalities It utilizes in-memory databases for user credentials, admin credentials, and the product catalog.

### Features: 
1. **User Authentication:**
   - Users can log in using a username and password. 
   - Admins also have a separate login route.
2. **Product Catalog:**
   - The catalog contains items categorized as footwear, clothing, and electronics.
   - Each item has an ID, name, and price.
3. **User Actions:**
   - Users can add products to their cart, remove items from the cart, and view their current cart.
   - The application supports basic error handling for invalid inputs.
4. **Checkout:**
   - Users can proceed to checkout, where the total price of items in the cart is calculated.
   - Upon successful checkout, the user's cart is cleared.
5. **Admin Operations:**
   - Admins can add, modify, and delete products.
   - Admins can add and remove product categories.
6. **Error Handling:**
  - The application handles various types of errors, such as invalid input, non-existent products, and unauthorized access.

### Usage: 
1. **User Login:**
   - Users log in using their credentials, stored in the `user_database`.
   - Admins log in through a separate route using credentials stored in the `admin_database`.
2. **Product Actions:**
   - Users can add products to their cart, remove items, and view the current cart.
3. **Checkout:**
   - Users can proceed to checkout, where the total price is calculated based on the items in the cart.
4. **Admin Operations:**
   - Admins can manage the product catalog by adding, modifying, and deleting products.
   - Admins can also add and remove product categories.
   
### How to Run: 
1. Install Flask:
   ``` pip install flask ```
2. Run the application:
   ``` python shopping_app.py ```
3. Access the application in a web browser or through API testing tools like Postman.
