import bcrypt

password="gjidf7"
salt= bcrypt.gensalt(rounds=15)
hased_pass=bcrypt.hashpw(password,salt)
print("done")