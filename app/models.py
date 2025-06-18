import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv() # This loads variables from a .env file in the current directory



def db():
    conn = MySQLdb.connect(
        host="localhost",
        user= os.getenv("user"),
        password=os.getenv("password"),
        db= os.getenv("database")
    )
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return conn, cursor


def create_tables():
    conn, cursor = db()


    #  creating doctor table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        qualification VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        image VARCHAR(255),
        address TEXT
    )
    """)


    # creating assistant table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assistant (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        qualification VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        image VARCHAR(255),
        address TEXT
    )
    """)

    # creating patient table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone_number VARCHAR(20) NOT NULL,
        address TEXT,
        blood_group VARCHAR(10),
        weight DECIMAL(5,2),
        height DECIMAL(5,2),
        age INT,
        sex VARCHAR(10),
        marital_status VARCHAR(20),
        password VARCHAR(255) NOT NULL,
        image VARCHAR(255)
    )
    """)



    # creating appointment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        time VARCHAR(255) NOT NULL,
        doctor_name VARCHAR(255) NOT NULL,
        patient_id INT NOT NULL,
        status ENUM('pending', 'approved', 'cancelled', 'on location') NOT NULL DEFAULT 'pending'
    )
    """)


# Prescription

# id
# doctor phone number
# doctor email
# doctor name
# Drug_Variations (json) (type
# strength
# dose
# duration
# advise  )



    # creating prescription table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescription (
        id INT AUTO_INCREMENT PRIMARY KEY,
        doctor_phone_number VARCHAR(20) NOT NULL,
        doctor_email VARCHAR(255) NOT NULL,
        doctor_name VARCHAR(255) NOT NULL,
        drug_variations JSON NOT NULL
    )
    """)


    # creating doctor_times table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor_times (
        id INT AUTO_INCREMENT PRIMARY KEY,
        time VARCHAR(255) NOT NULL,
        status ENUM('available', 'unavailable') NOT NULL DEFAULT 'available'
    )
    """)


    # an table for clinic open/close days
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinic_days (
        id INT AUTO_INCREMENT PRIMARY KEY,
        day VARCHAR(20) NOT NULL,
        status ENUM('open', 'closed') NOT NULL DEFAULT 'open'
    )
    """)


# drugs

# id
# Trade name
# Generic name
# Note
# Warning
# Side effect
# Additional advice
# Drug_Variations (json)
# type
# strength
# dose
# duration
# advise
# price


    # creating drugs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        trade_name VARCHAR(255) NOT NULL,
        generic_name VARCHAR(255) NOT NULL,
        note TEXT,
        warning TEXT,
        side_effect TEXT,
        additional_advice TEXT,
        drug_variations JSON NOT NULL,
        price DECIMAL(10,2)
    )
    """)

# invoice

# id
# doctor phone number
# doctor email
# doctor name
# patient name
# patient phone number

# Drug_Variations (json)
# type
# strength
# dose
# duration
# advise
# price

    # creating invoice table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        doctor_phone_number VARCHAR(20) NOT NULL,
        doctor_email VARCHAR(255) NOT NULL,
        doctor_name VARCHAR(255) NOT NULL,
        patient_name VARCHAR(255) NOT NULL,
        patient_phone_number VARCHAR(20) NOT NULL,
        drug_variations JSON NOT NULL,
        price DECIMAL(10,2) NOT NULL
    )
    """)



    # creating drug_type table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drug_type (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
    )
    """)



    # creating drug_strength table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drug_strength (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
    )
    """)



    # creating drug_dose table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drug_dose (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
    )
    """)



    # creating drug_duration table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drug_duration (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
    )
    """)



    # creating drug_advice table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drug_advice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
    )
    """)


    conn.commit()
    cursor.close()
    conn.close()
