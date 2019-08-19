import sqlite3
 
class db:
    def __init__(self,chatId):
        self.chatId = chatId
  
    def checkTableExist(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
 
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=" + tablename
        c.execute(query)
         
        if c.fetchone()[0] == 1:
            conn.close()
            return True
        else:
            conn.close()
            return False
     
    def createTable(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = 'chat' + str(tablename*-1)
        query = "CREATE TABLE "+ tablename +""" ( 
            challenger text, 
            challenged text, 
            numberChallenger integer,
            numberChallenged integer,
            chosenChallenger integer,
            chosenChallenged integer
            )"""
        c.execute(query)
        conn.commit()
        conn.close()
 
    def checkPendentGame(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        #Get Challenger name (name will only by in DB if a Game is still running)
        query = "SELECT challenger FROM " + tablename
        c.execute(query)
        stillingameChallenger = c.fetchone()
 
        #Get Challenged name (name will only by in DB if a game is still running)
        query = "SELECT challenged FROM " + tablename
        c.execute(query)
        stillingameChallenged = c.fetchone()
        conn.close()
 
        return(stillingameChallenger, stillingameChallenged)
 
    def storeNameChallenger(self, nameChallenger):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        nameChallenger = """'"""+ nameChallenger +"""'"""
 
        query = "INSERT INTO "+ tablename +"(challenger) VALUES ("+ nameChallenger +")"
        c.execute(query)
        conn.commit()
        conn.close()
 
    def storeNameChallenged(self, nameChallenged):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        nameChallenged = """'"""+ nameChallenged +"""'"""
 
        query = "UPDATE "+ tablename +" SET challenged = "+ nameChallenged
        c.execute(query)
        conn.commit()
        conn.close()
 
    def storeNumberChallenger(self, numberChallenger):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        numberChallenger = """'"""+ str(numberChallenger) +"""'"""
 
        query = "UPDATE "+ tablename +" SET numberChallenger = "+ numberChallenger
        c.execute(query)
        conn.commit()
        conn.close()
 
    def storeNumberChallenged(self, numberChallenged):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        numberChallenged = """'"""+ str(numberChallenged) +"""'"""
 
        query = "UPDATE "+ tablename +" SET numberChallenged = "+ numberChallenged
        c.execute(query)
        conn.commit()
        conn.close()

    def storeChosenChallenger(self, chosenChallenger):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        chosenChallenger = """'"""+ str(chosenChallenger) +"""'"""
    
        query = "UPDATE "+ tablename +" SET chosenChallenger = "+ chosenChallenger
        c.execute(query)
        conn.commit()
        conn.close()

    def storeChosenChallenged(self, chosenChallenged):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        chosenChallenged = """'"""+ str(chosenChallenged) +"""'"""
    
        query = "UPDATE "+ tablename +" SET chosenChallenged = "+ chosenChallenged
        c.execute(query)
        conn.commit()
        conn.close()

    def getFromDb(self, requestedItem):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
    
        query = "SELECT "+ requestedItem +" FROM " + tablename
        c.execute(query)
        requestedItem = c.fetchone()
        conn.close()
        return(requestedItem)
 
    def cancleGame(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "DELETE FROM " + tablename
        c.execute(query)
        conn.commit()
        conn.close()
    
    def dropTable(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "DROP TABLE IF EXISTS" + tablename
        c.execute(query)
        conn.commit()
        conn.close()