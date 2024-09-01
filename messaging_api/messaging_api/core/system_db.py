from typing import List

import mariadb
from mariadb import connect
from messaging_api.schema import User, create_token
from messaging_api.config import SYSTEMDB_USERNAME, SYSTEMDB_PASSWORD, SYSTEMDB_ADDR, SYSTEMDB_PORT, SYSTEMDB_DBNAME
from messaging_api.exceptions import WrongCredentialsException, UserAlreadyExists, AlreadyContactException

class SystemDBController:
    
    def __init__(self, 
                 user = SYSTEMDB_USERNAME, 
                 password = SYSTEMDB_PASSWORD, 
                 host = SYSTEMDB_ADDR, 
                 port = SYSTEMDB_PORT, 
                 dbname = SYSTEMDB_DBNAME):
        
        self._db = connect( host = host,
                            port = port,
                            user = user,
                            password = password,
                            database = dbname)
        
        self._create_db_v1()
    
    def _create_db_v1(self):
        connection = self._db.cursor()
        connection.execute("""
                           create table if not exists User (
                               id UUID DEFAULT SYS_GUID(),
                               username VARCHAR(32) UNIQUE,
                               name VARCHAR(32) NOT NULL,
                               password VARCHAR(41) NOT NULL,
                               email VARCHAR(128) NOT NULL,
                               photo VARCHAR(128),
                               PRIMARY KEY(id)
                           );""")
        
        connection.execute("""
                           create table if not exists ContactList (
                                contact_list_owner_id UUID NOT NULL,
                                contact_id UUID NOT NULL,
                                constraint PK_OwnerContact PRIMARY KEY(contact_list_owner_id, contact_id),
                                constraint FK_ContactListOwner FOREIGN KEY (contact_list_owner_id) REFERENCES User(id),
                                constraint FK_ContactListContact FOREIGN KEY (contact_id) REFERENCES User(id)
                           );""")
        
        connection.execute("""
                           create table if not exists Chat (
                               id UUID DEFAULT SYS_GUID(),
                               name VARCHAR(32) UNIQUE NOT NULL,
                               PRIMARY KEY (id)
                           );""")
        
        connection.execute("""
                           create table if not exists ChatUser (
                               chat_id UUID NOT NULL,
                               user_id UUID NOT NULL,
                               is_admin BIT DEFAULT FALSE,
                               constraint PK_ChatUser PRIMARY KEY (chat_id, user_id),
                               constraint FK_Chat FOREIGN KEY (chat_id) REFERENCES Chat(id),
                               constraint FK_User FOREIGN KEY (user_id) REFERENCES User(id)
                           );""")

        connection.close()
    
    def register_user(self, name:str, username:str, password:str, email:str) -> User:
        connection = self._db.cursor()
        try:
            connection.execute("insert into User (name, username, password, email) values (?,?,PASSWORD(?),?)",(name, username, password, email))
        except mariadb.IntegrityError:
            raise UserAlreadyExists(username)
        self._db.commit()
        
                
        connection.close()
        return True

    def login(self, username, password):
        connection = self._db.cursor()
        connection.execute("select id from User where name = ? and password = PASSWORD(?) LIMIT 1",(username, password))
        
        row = connection.fetchone()
        if row is None:
            raise WrongCredentialsException()
            
        token = create_token(row[0])
        connection.close()
        
        return token
    
    def user(self, user_id:str):
        connection = self._db.cursor()
        connection.execute("select id, name, username, email, photo from User where id = ? LIMIT 1",(user_id))
    
        
    def list_contacts(self, user_id:str, itens_per_page:int=10, offset:int=0) -> List[User]:
        connection = self._db.cursor()
        connection.execute("select c.id, c.name, c.username, c.email, c.photo from ContactList con left join User c on con.contact_id = c.id where con.contact_list_owner_id = ? LIMIT ? OFFSET ?",(user_id, itens_per_page, offset))
        
        users = []
        
        for uuid, name, username, email, photo in connection:
            user = User(uuid, username, name, email, photo)
            users.append(user)
        
        return users
        


    def add_contact(self, owner_id:str, contact_id:str):
        connection = self._db.cursor()
        try:
            connection.execute("insert into ContactList (contact_list_owner_id, contact_id) values (?,?)",(owner_id, contact_id))
        except mariadb.IntegrityError:
            raise AlreadyContactException()
        self._db.commit()
        
    

    


if __name__ == "__main__":
    db = SystemDBController()
    # user1 = db.register_user("matheus", "Matheus", "123456", "matheusbarcelosoliveira@gmail.com")
    # # user2 = db.register_user("wedsney", "Wedsney", "123456", "matheusbarcelosoliveira@gmail.com")
    
    # # db.add_contact(user1, user2)
    # # db.add_contact(user2, user1)
    
    # token = db.login("matheus", "123456")
    # user = User.from_token(token)
    
    contacts = db.list_contacts("6f0f97d5-6819-11ef-afe5-0242ac130004")
    ...
    