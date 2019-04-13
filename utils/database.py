def create_connection(db_uri):
    try:
        conn = sqlite3.connect(db_uri)
        return conn
    except Error as e:
        log_line(logger,level='info',msg=e,trace=False,exit=False)