
## **CustomUser Model Documentation**

The `CustomUser` model represents a custom user for the application, which inherits from Django’s `AbstractBaseUser` and `PermissionsMixin`. This model is designed to provide a flexible user system with roles such as "Agent" and "Customer."

### **Fields**

1. **email (EmailField)**
   - **Description**: The email address is used as the unique identifier for the user, replacing the default `username`.
   - **Constraints**: Must be unique. 
   - **Example**: `example@example.com`

2. **first_name (CharField)**
   - **Description**: The user's first name.
   - **Max Length**: 30 characters.
   - **Blank**: Yes (optional field).
   - **Example**: `John`

3. **last_name (CharField)**
   - **Description**: The user's last name.
   - **Max Length**: 30 characters.
   - **Blank**: Yes (optional field).
   - **Example**: `Doe`

4. **username (CharField)**
   - **Description**: A username for the user. This field is optional and can be left blank if not needed.
   - **Max Length**: 30 characters.
   - **Blank**: Yes (optional field).
   - **Example**: `johndoe`

5. **is_active (BooleanField)**
   - **Description**: A flag indicating if the user is active. If `False`, the user is effectively disabled.
   - **Default**: `True`

6. **is_staff (BooleanField)**
   - **Description**: A flag indicating if the user is a staff member. Staff members have access to the Django admin interface.
   - **Default**: `False`

7. **is_agent (BooleanField)**
   - **Description**: A flag indicating if the user is an agent in the system.
   - **Default**: `False`

8. **is_customer (BooleanField)**
   - **Description**: A flag indicating if the user is a customer in the system.
   - **Default**: `False`

### **CustomUserManager**

The `CustomUserManager` is the manager for the `CustomUser` model, and it is responsible for creating users and superusers.

#### **Methods**

1. **create_user(email, password=None, **extra_fields)**
   - **Description**: Creates a regular user with an email, password, and any additional fields provided.
   - **Arguments**:
     - `email` (string): The user’s email address.
     - `password` (string, optional): The user's password.
     - `**extra_fields`: Any extra fields such as `first_name`, `last_name`, `is_agent`, or `is_customer`.
   - **Returns**: A new `CustomUser` object with the provided details.

2. **create_superuser(email, password=None, **extra_fields)**
   - **Description**: Creates a superuser with admin-level access to the system, including `is_staff`, `is_superuser`, and `is_active` set to `True`.
   - **Arguments**:
     - `email` (string): The superuser’s email address.
     - `password` (string): The superuser’s password.
     - `**extra_fields`: Extra fields like `is_staff` and `is_superuser` are automatically set to `True` for superusers.
   - **Returns**: A new `CustomUser` object with superuser privileges.

### **USERNAME_FIELD and REQUIRED_FIELDS**

- **USERNAME_FIELD**: The unique identifier for the user. In this case, it is set to `email` instead of the default `username` field.
- **REQUIRED_FIELDS**: A list of additional fields required when creating a user via `create_user` or `create_superuser`. In this case, it includes `email` and `password`.

### **Usage Example**

Here is an example of how to create a user or superuser using the `CustomUserManager`:

```python
# Create a regular user
user = CustomUser.objects.create_user(
    email='user@example.com',
    password='securepassword',
    first_name='John',
    last_name='Doe',
    is_agent=False,
    is_customer=True
)

# Create a superuser
superuser = CustomUser.objects.create_superuser(
    email='admin@example.com',
    password='adminpassword',
    first_name='Admin',
    last_name='User'
)
