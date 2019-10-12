import sqlite3,os,json


class VanUsers():

    def __init__(self,data_base,*args, **kwargs):
        
        self.userName = os.environ["userName"]
        self.dataBase = data_base
        
        with open("VanTools\\config.json","r") as f:
            data = json.load(f)

        self.version = data["Version"]
        


    def checkUser(self):
        '''
        Check if the User is already in the Database
        '''

        con = sqlite3.connect(self.dataBase)
        cur = con.cursor()
        selectName = cur.execute("SELECT name FROM USERS  ")
        self.nameList = [i[0] for i in selectName]
        self.sumUser = len(self.nameList)
        con.close()

        if self.userName in self.nameList:
            print("{} is existed ".format(self.userName))
            pass
        else:
            self.createUser()


    def addUsedDate(self):
        '''
        Add the first time User used the tools
        '''
    
    def updateUsedDate(self):
        '''
        Update the last time User used the tools
        '''
    
    def createUser(self):
        '''
        Add user into database
        '''
        con = sqlite3.connect(self.dataBase)
        cur = con.cursor()
        countRow = cur.execute("SELECT name FROM USERS  ")
        print(self.sumUser, self.userName)
        cur.execute(
            '''
                INSERT INTO USERS (ID, NAME, version, CreatTime)
                VALUES(?, ?, ?, date('now'));
            ''',(self.sumUser+1, self.userName, self.version))
        con.commit()
        con.close()

fan = VanUsers(r"C:\Users\Fanziwen\Desktop\testPackage\test.db")

fan.checkUser() 