# Pet Registration & Management System for vet centers - A Software Security Project

This is a software security project aimed at building a software for managing pets within vet centers using a secure and a well designed software infrastructure.
## Requirements

> The Following Python Packages:

**1. Python Customtkinter library**
```pip install customtkinter```

**2. mysql connector**
```pip install mysql-connector-python```

**3. Pillow**
```pip install pillow```

**4. bcrypt**
```pip install bcrypt```

**5. PyCrypto**
```pip install pycrypto```

![login_page](https://github.com/shahedmehdawi/Desktop-application/assets/140253527/56814f13-e45e-46bc-a848-c57a2892186f)

### Database Tables Utilized
> [!NOTE]
> **Make sure they are all within the same database schema**
<details>
<summary><b>Users Table</b></summary>
<pre>
CREATE TABLE users (
    UID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  #Add email for user contact
    salt BINARY(16) NOT NULL,  #Move salt before role
    role ENUM('normal_user', 'doctor', 'admin') NOT NULL DEFAULT 'normal_user'
);
</pre>
</details>

<details>
<summary><b>Available Pets Table</b></summary>
<pre>
CREATE TABLE pets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        species VARCHAR(255) NOT NULL,
        age VARCHAR(50) NOT NULL,
        image_path VARCHAR(255) NOT NULL
);
</pre>
</details>

<details>
<summary><b>Customers Table</b></summary>
<pre>
CREATE TABLE customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    adopted_pet VARCHAR(255) NOT NULL
);
</pre>
</details>



## Use Cases
<details>
<summary><b>Use Case Diagrams</b></summary>

<img src="./Assets_Cat/Diagrams/Customer Use Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/Doctor%20Use%20Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/Admin%20Use%20Cases.png" width="500" height="500">

</details>

## Misuse Cases
<details>
<summary><b>Login Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Login Misuse Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/L1.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/L2.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/L3.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/L4.png" width="500" height="500">

</details>

<details>
<summary><b>Customer Signup Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Customer Signup Misuse Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/S1.png" width="500" height="500">

</details>