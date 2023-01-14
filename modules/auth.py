def login(request, cnx, table):
    user = request.headers["Username"]
    password = request.headers["Password"]
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM "' + table + ' WHERE Username="' + user + '" AND Password="' + password + '"')
    result = cursor.fetchone()
    autheduser = result[0]
    authedpassword = result[1]
    if autheduser and authedpassword:
        