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
            challanger text,
            numberChallanger integer, 
            challanged text, 
            numberChallanged integer
            )"""
        c.execute(query)
        conn.commit()
        conn.close()
 
    def checkPendentGame(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        #Get Challanger name (name will only by in DB if a Game is still running)
        query = "SELECT challanger FROM " + tablename
        c.execute(query)
        stillingameChallanger = c.fetchone()
 
        #Get Challanged name (name will only by in DB if a game is still running)
        query = "SELECT challanged FROM " + tablename
        c.execute(query)
        stillingameChallanged = c.fetchone()
        conn.close()
 
        return(stillingameChallanger, stillingameChallanged)
 
    def storeNameChallanger(self, nameChallanger):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        nameChallanger = """'"""+ nameChallanger +"""'"""
 
        query = "INSERT INTO "+ tablename +"(challanger) VALUES ("+ nameChallanger +")"
        c.execute(query)
        conn.commit()
        conn.close()
 
    def storeNameChallanged(self, nameChallanged):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        nameChallanged = """'"""+ nameChallanged +"""'"""
 
        query = "UPDATE "+ tablename +" SET challanged = "+ nameChallanged
        c.execute(query)
        conn.commit()
        conn.close()
 
    def getChallangerName(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "SELECT challanger FROM " + tablename
        c.execute(query)
        challanger = c.fetchone()
        conn.close()
        return(challanger)
 
    def getChallangedName(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "SELECT challanged FROM " + tablename
        c.execute(query)
        challanged = c.fetchone()
        conn.close()
        return(challanged)
 
    def storeNumberChallanger(self, numberChallanger):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        numberChallanger = """'"""+ str(numberChallanger) +"""'"""
 
        query = "UPDATE "+ tablename +" SET numberChallanger = "+ numberChallanger
        c.execute(query)
        conn.commit()
        conn.close()
 
    def storeNumberChallanged(self, numberChallanged):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
        numberChallanged = """'"""+ str(numberChallanged) +"""'"""
 
        query = "UPDATE "+ tablename +" SET numberChallanged = "+ numberChallanged
        c.execute(query)
        conn.commit()
        conn.close()
 
    def getChallangerNumber(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "SELECT numberChallanger FROM " + tablename
        c.execute(query)
        numberChallanger = c.fetchone()
        conn.close()
        return(numberChallanger)
 
    def getChallangedNumber(self):
        conn = sqlite3.connect('1to30.db')
        c = conn.cursor()
        tablename = self.chatId
        tablename = """'""" + 'chat' + str(tablename*-1) + """'"""
 
        query = "SELECT numberChallanged FROM " + tablename
        c.execute(query)
        numberChallanged = c.fetchone()
        conn.close()
        return(numberChallanged)
 
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