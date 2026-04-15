import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="arnab",
    database="school_fees"
)

cur = db.cursor()

BASE_FEE = 10000
FINE_PER_DAY = 20

print("WELCOME TO ST JOSEPH SECONDARY SCHOOL FEE MANAGEMENT SYSTEM")

while True:
    print("""
1. Signup
2. Login
3. Exit
""")
    choice = input("Enter choice: ")

    if choice == "1":
        print("\n--- SIGNUP ---")
        u = input("Username: ")
        p = input("Password: ")
        try:
            cur.execute("INSERT INTO users (username,password) VALUES (%s,%s)", (u, p))
            db.commit()
            print("Signup successful")
        except:
            print("Username already exists")

    elif choice == "2":
        print("\n--- LOGIN ---")
        u = input("Username: ")
        p = input("Password: ")

        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
        user = cur.fetchone()

        if not user:
            print("Invalid login")
            continue

        print("Login successful")

        while True:
            print("""
1. Register Student
2. Student Fee Portal
3. Feedback
4. Logout
""")
            op = input("Enter option: ")

            if op == "1":
                print("\n--- STUDENT REGISTRATION ---")
                name = input("Student Name: ")
                cls = int(input("Class (1-12): "))
                sec = input("Section (A-D): ").upper()

                while cls < 1 or cls > 12:
                    cls = int(input("Re-enter class (1-12): "))

                while sec not in ["A", "B", "C", "D"]:
                    sec = input("Re-enter section (A-D): ").upper()

                adm = random.randint(1000, 9999)

                cur.execute(
                    "INSERT INTO students VALUES (%s,%s,%s,%s)",
                    (adm, name, cls, sec)
                )
                cur.execute("INSERT INTO fees (admission_no) VALUES (%s)", (adm,))
                db.commit()

                print("Admission Number:", adm)

            elif op == "2":
                adm = int(input("Enter Admission Number: "))
                cur.execute("SELECT * FROM students WHERE admission_no=%s", (adm,))
                stu = cur.fetchone()

                if not stu:
                    print("Wrong admission number")
                    continue

                while True:
                    print("""
1. Pay First Term
2. Pay Second Term
3. Pay Third Term
4. Fee Details
5. Payment History
6. Exit
""")
                    ch = input("Choose: ")

                    if ch in ["1", "2", "3"]:
                        days = int(input("Late days: "))
                        total = BASE_FEE + days * FINE_PER_DAY
                        print("Total Fee:", total)

                        amt = int(input("Enter amount: "))
                        while amt < total:
                            amt = int(input("Amount less, re-enter: "))

                        if amt > total:
                            print("Extra amount will be transferred to bank")

                        cur.execute(f"UPDATE fees SET term{ch}=TRUE WHERE admission_no=%s", (adm,))
                        cur.execute(
                            "INSERT INTO history (admission_no,action) VALUES (%s,%s)",
                            (adm, f"Paid term {ch}")
                        )
                        db.commit()
                        print("Fee paid successfully")

                    elif ch == "4":
                        cur.execute("SELECT * FROM fees WHERE admission_no=%s", (adm,))
                        f = cur.fetchone()
                        print("\nFEE DETAILS")
                        print("First Term :", "Paid" if f[1] else "Unpaid")
                        print("Second Term:", "Paid" if f[2] else "Unpaid")
                        print("Third Term :", "Paid" if f[3] else "Unpaid")

                    elif ch == "5":
                        cur.execute("SELECT action FROM history WHERE admission_no=%s", (adm,))
                        rows = cur.fetchall()
                        if not rows:
                            print("No history available")
                        for r in rows:
                            print("-", r[0])

                    elif ch == "6":
                        break

                    else:
                        print("Wrong choice")

            elif op == "3":
                fb = input("Enter your feedback: ")
                cur.execute("INSERT INTO feedback VALUES (%s)", (fb,))
                db.commit()
                print("Thank you for your feedback")

            elif op == "4":
                break

            else:
                print("Invalid option")

    elif choice == "3":
        print("THANK YOU FOR USING\nVISIT AGAIN!")
        break

    else:
        print("Wrong input")
