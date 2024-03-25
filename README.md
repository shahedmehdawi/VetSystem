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
<details>
<summary>**Users Table** (bold)</summary>
```sql
CREATE TABLE users (
    UID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  #Add email for user contact
    salt BINARY(16) NOT NULL,  #Move salt before role
    role ENUM('normal_user', 'doctor', 'admin') NOT NULL DEFAULT 'normal_user'
);
```
</details>
