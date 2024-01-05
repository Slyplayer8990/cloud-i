import jwt
import psycopg2
cnx = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432",
                        buffered=true)
def get_token(user, passw):
    file = open("secret.txt", "r")
    secret = file.read()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if not result is None:
        encoded = jwt.encode({username: user, password: passw }, secret, algorithm=["HS256"])
        return encoded


    
