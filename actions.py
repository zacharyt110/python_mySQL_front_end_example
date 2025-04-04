import mysql.connector

def database_credentials():
    """
    Returns the database connection details as a dictionary.
    """
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'BlackHoles!1',
        'database': 'testdatabase',
        'port': 3306
    }

def fetch_all_data():
    """
    Fetches all rows from the V1550A table.
    """
    try:
        db_credentials = database_credentials()
        connection = mysql.connector.connect(**db_credentials)
        cursor = connection.cursor()

        query = "SELECT * FROM V1550A;"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            return "\n".join(str(row) for row in results)
        else:
            return "No data found in the table."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def fetch_serial_number_data(serial_number):
    """
    Fetches rows from the V1550A table where the serial number matches the given value.
    """
    try:
        db_config = database_credentials()
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT * FROM V1550A WHERE serial_number = %s;"
        cursor.execute(query, (serial_number,))
        results = cursor.fetchall()

        if results:
            return "\n".join(str(row) for row in results)
        else:
            return f"No data found for serial number: {serial_number}"

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_data(model_number, serial_number, operator, voa_sn, connectorization, min_attenuation, max_attenuation, max_current, per_a, per_b, qc_inspector, date_closed):
    """
    Inserts a new row into the V1550A table.
    """
    try:
        db_config = database_credentials()
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = """
        INSERT INTO V1550A (model_number, serial_number, operator, VOA_sn, connectorization, min_attenuation, max_attenuation, max_current, per_a, per_b, qc_inspector, date_closed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (model_number, serial_number, operator, voa_sn, connectorization, min_attenuation, max_attenuation, max_current, per_a, per_b, qc_inspector, date_closed))
        connection.commit()
        return "Data inserted successfully."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def search_data(serial_number=None, model_number=None):
    """
    Searches the V1550A table using serial number, model number, or both.
    """
    try:
        db_config = database_credentials()
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT * FROM V1550A WHERE 1=1"
        params = []

        if serial_number:
            query += " AND serial_number = %s"
            params.append(serial_number)
        if model_number:
            query += " AND model_number = %s"
            params.append(model_number)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        if results:
            return "\n".join(str(row) for row in results)
        else:
            return None

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
