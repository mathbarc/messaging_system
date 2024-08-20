from typing import List

import mariadb
from mariadb import connect
from messaging_api.schema import User
from messaging_api.config import SYSTEMDB_USERNAME, SYSTEMDB_PASSWORD, SYSTEMDB_ADDR, SYSTEMDB_PORT, SYSTEMDB_DBNAME
from ..exceptions import WrongCredentialsException, UserAlreadyExists, AlreadyContactException

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
                               id BIGINT AUTO_INCREMENT,
                               username VARCHAR(32) UNIQUE,
                               name VARCHAR(32),
                               password VARCHAR(64),
                               email VARCHAR(128),
                               PRIMARY KEY(id)
                           );""")
        
        connection.execute("""
                           create table if not exists ContactList (
                                contact_list_owner_id BIGINT PRIMARY KEY,
                                contact_id BIGINT,
                                constraint FK_ContactListOwner FOREIGN KEY (contact_list_owner_id) REFERENCES User(id),
                                constraint FK_ContactListContact FOREIGN KEY (contact_id) REFERENCES User(id),
                                constraint UNI_OwnerContact UNIQUE (contact_list_owner_id, contact_id)
                           );""")
        
        connection.execute("""
                           create table if not exists Chat (
                               id BIGINT AUTO_INCREMENT PRIMARY KEY,
                               name VARCHAR(32) UNIQUE
                           );""")
        
        connection.execute("""
                           create table if not exists ChatUser (
                               chat_id BIGINT PRIMARY KEY,
                               user_id BIGINT,
                               is_admin BIT DEFAULT FALSE,
                               constraint FK_Chat FOREIGN KEY (chat_id) REFERENCES Chat(id),
                               constraint FK_User FOREIGN KEY (user_id) REFERENCES User(id),
                               constraint UNI_ChatUser UNIQUE (chat_id, user_id)
                           );""")

        connection.close()
    
    def register_user(self, name:str, username:str, password:str, email:str) -> User:
        connection = self._db.cursor()
        try:
            connection.execute("insert into User (name, username, password, email) values (?,?,PASSWORD(?),?)",(name, username, password, email))
        except mariadb.IntegrityError:
            raise UserAlreadyExists(username)
        self._db.commit()
        id = connection.lastrowid
        
        connection.execute("select id, name, username, email from User where id = ?",(id,))
        
        for id, name, username, email in connection:
            response = User(id=id, name=name, username=username, email=email)
        
        connection.close()
        return response

    def login(self, username, password):
        connection = self._db.cursor()
        connection.execute("select id, name, username, email from User where name = ? and password = PASSWORD(?) LIMIT 1",(username, password))
        
        row = connection.fetchone()
        if row is None:
            raise WrongCredentialsException()
        
        user = User(id=row[0], name=row[1], username=row[2], email=row[3])
            
        return user.create_token()
        
    def list_contacts(self, user:User, itens_per_page:int=10, offset:int=0) -> List[User]:
        connection = self._db.cursor()
        connection.execute("select c.id, c.name, c.username, c.email from ContactList con left join User c on con.contact_id = c.id where con.contact_list_owner_id = ? LIMIT ? OFFSET ?",(user.id,itens_per_page, offset))
        
        users = []
        
        for id, name, username, email in connection:
            user = User(id=id, name=name, username=username, email=email)
            users.append(user)
        
        return users
        


    def add_contact(self, owner:User, contact:User):
        connection = self._db.cursor()
        try:
            connection.execute("insert into ContactList (contact_list_owner_id, contact_id) values (?,?)",(owner.id, contact.id))
        except mariadb.IntegrityError:
            raise AlreadyContactException()
        self._db.commit()
        
    

    


if __name__ == "__main__":
    db = SystemDBController()
    # user1 = db.register_user("matheus", "Matheus", "123456", "matheusbarcelosoliveira@gmail.com")
    # user2 = db.register_user("wedsney", "Wedsney", "123456", "matheusbarcelosoliveira@gmail.com")
    
    # db.add_contact(user1, user2)
    # db.add_contact(user2, user1)
    
    token = db.login("matheus", "123456")
    user = User.from_token(token)
    
    contacts = db.list_contacts(user)
    ...
    