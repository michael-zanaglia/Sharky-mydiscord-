import mysql.connector, threading

def sock():
    try :
        conn = mysql.connector.connect(
                    user = "root",
                    passwd = "mdp",
                    host = "localhost",
                    database = "mydiscord"
                )
        cursor = conn.cursor()

        while True :
            
            cursor.execute("select pseudo from run")
            conn.commit()
            liste_mail = cursor.fetchall()
            print(liste_mail)
    except mysql.connector.Error as err:
        print("Erreur MySQL:", err)


sock()
#ss = threading.Thread(target=sock)
#ss.start()
    