# Pet Registration & Management System for vet centers - A Software Security Project

This is a software security project aimed at building a software for managing pets within vet centers using a secure and a well designed software infrastructure.
## Package Requirements

> The Following Python Packages:

**1. Python Customtkinter library**
```pip install customtkinter```

**2. Python tkinter library**
```pip install tkinter```

**3. mysql connector**
```pip install mysql-connector-python```

**4. Pillow**
```pip install pillow```

**5. bcrypt**
```pip install bcrypt```

**6. PyCrypto**
```pip install pycrypto```

**7. pycryptodome**
```pip install pycryptodome```

**8. pycryptodomex**
```pip install pycryptodomex```

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
    email VARCHAR(255) NOT NULL UNIQUE,
    salt BINARY(32) NOT NULL,
    role ENUM('normal_user', 'doctor', 'admin') NOT NULL DEFAULT 'normal_user',
    is_new BOOLEAN NOT NULL DEFAULT FALSE
);
</pre>
</details>

<details>
<summary><b>Available Pets Table</b></summary>
<pre>
CREATE TABLE pets (
    ⁠ id INT AUTO_INCREMENT PRIMARY KEY,
    ⁠ name VARCHAR(255) NOT NULL,
    ⁠ species VARCHAR(255) NOT NULL,
    ⁠ age VARCHAR(50) NOT NULL,
    ⁠ image_path VARCHAR(255) NOT NULL,
    ⁠ adopted TINYINT(1) NOT NULL DEFAULT 0, -- 0 for False, 1 for True
    ⁠ customer_id INT DEFAULT NULL, -- Foreign key to link to customer_info
    FOREIGN KEY (⁠ customer_id ⁠) REFERENCES customer_info (⁠ id ⁠)
);
</pre>
</details>

<details>
<summary><b>customer_info Table</b></summary>
<pre>
CREATE TABLE ⁠ customer_info ⁠ (
    ⁠ id ⁠ INT AUTO_INCREMENT PRIMARY KEY,
    ⁠ name ⁠ VARCHAR(255) NOT NULL,
    ⁠ number ⁠ VARCHAR(255) NOT NULL,
    ⁠ location ⁠ VARCHAR(255) NOT NULL,
    ⁠ pet_info ⁠ VARCHAR(255) NOT NULL
);
</pre>
</details>

<details>
<summary><b>login_logs Table</b></summary>
<pre>
CREATE TABLE login_logs (
    user_id INT,
    username VARCHAR(255),
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(UID)
);
</pre>
</details>

## Functional & Non-functional Requirements
<details>
<summary><b>Functional Requirements</b></summary>

* Users must be logged in before being able to view the available pets dasboard (no anonymous viewing)
* 2FA must be implemented over sensitive accounts including the admins and the doctor accounts. 
Passwords must be complex for all accounts (10 characters min - use of special characters, symbols, numbers and upper and lower characters is mandatory)
* Passwords are stored as bcrypt salted hashes along with their salt and password authentication are done by hashing to limit brute forcing activities and slow them down.
* Doctors will be able to add the available pets for adoption in which users can choose from from their adoption dashboard.
* A database backup must be held in a seperate host.
* Backups must be performed every 2 days
* Only admin users will be able to register users of any role including new doctors, new admins and new normal privileged users (Customers).
* Customer users are the only ones able to change their profile info like their email, password, and full name.
</details>

<details>
<summary><b>Non-Functional Requirements</b></summary>

* **Security** - The app must safe for use and prevents potential misuses by adversaries
* **Reliability** - App must be available to users as much as possible and is resistant to any Denial of Service attack.
* **Performance** - Delays in displaying web pages and performing app functionality are minimized.
* **Scalability** - Servers can be potentially scalled out depending on the demand by relying on additional cloud host servers that are flexible to scale in/out.
* **Usability** - A user-friendly front end is available for end users to ensure a smooth experience
</details>

## Use Cases
<details>
<summary><b>Use Case Diagrams</b></summary>

<img src="./Assets_Cat/Diagrams/Customer Use Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/Doctor%20Use%20Cases.png" width="500" height="500">

<img src="./Assets_Cat/Diagrams/Admin%20Use%20cases2.png" width="500" height="500">

</details>

## Misuse Cases
<details>
<summary><b>Login Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Login Misuse Cases.png" width="750" height="600">

<img src="./Assets_Cat/Diagrams/L1.png" width="580" height="500">

<img src="./Assets_Cat/Diagrams/L2.png" width="580" height="500">

<img src="./Assets_Cat/Diagrams/L3.png" width="580" height="500">

<img src="./Assets_Cat/Diagrams/L4.png" width="580" height="500">

</details>

<details>
<summary><b>Customer Signup Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Customer Signup Misuse Cases.png" width="780" height="550">

<img src="./Assets_Cat/Diagrams/S1.png" width="570" height="500">

</details>

<details>
<summary><b>Edit Available Pets for Adoption Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Edit Available pets Misuse cases.png" width="780" height="550">

<img src="./Assets_Cat/Diagrams/E1.png" width="570" height="500">
<img src="./Assets_Cat/Diagrams/E2.png" width="570" height="500">

</details>

<details>
<summary><b>Adopter details Misuse Cases</b></summary>

<img src="./Assets_Cat/Diagrams/Adopter's details Misuse cases.png" width="780" height="550">

<img src="./Assets_Cat/Diagrams/A1.png" width="570" height="500">
<img src="./Assets_Cat/Diagrams/A2.png" width="570" height="500">

</details>
<details>
<summary><b>editprofile Misuse Case</b></summary>

<img src="./Assets_Cat/Diagrams/editprofile usecase (2).png" width="850" height="550">

<img src="./Assets_Cat/Diagrams/D1.png" width="1040" height="770">

</details>

<details>
<summary><b>session Hijacking Misuse Case</b></summary>

<img src="./Assets_Cat/Diagrams/L5.jpg" width="850" height="550">

<img src="./Assets_Cat/Diagrams/session_hijacking.png" width="700" height="300">


</details>

<details>
<summary><b>Admin Registration Misuse Case</b></summary>
<img src="./Assets_Cat/Diagrams/admin_registration.png" width="700" height="300">
<img src="./Assets_Cat/Diagrams/R1.png" width="1040" height="770">
</details>
