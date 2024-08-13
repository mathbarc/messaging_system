import mariadb
from mariadb import connect
from messaging_api.schema import User


class SystemDBController:
    
    def __init__(self, user, password, host, port, dbname="message-system"):
        self._db = connect( host = host,
                            port = port,
                            user = user,
                            password = password,
                            database = dbname)
        
        connection = self._db.cursor()
        connection.execute("""
                           create table if not exists User (
                               id BIGINT AUTO_INCREMENT,
                               uuid UUID DEFAULT (uuid()) UNIQUE,
                               name VARCHAR(32) UNIQUE,
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
                               uuid UUID DEFAULT (uuid()) UNIQUE,
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
    
    def register_user(self, name, password, email) -> User:
        connection = self._db.cursor()
        connection.execute("insert into User (name, password, email) values (?,?,?)",(name, password, email))
        self._db.commit()
        id = connection.lastrowid
        
        connection.execute("select id, uuid, name, email from User where id = ?",(id,))
        
        for id, uuid, name, email in connection:
            response = User(_id=id, uuid=uuid, name=name, email=email)
        
        connection.close()
        return response

    def add_contact(self, owner:User, contact:User):
        connection = self._db.cursor()
        connection.execute("insert into ContactList (contact_list_owner_id, contact_id) values (?,?)",(owner._id, contact._id))
        self._db.commit()
    
    


if __name__ == "__main__":
    db = SystemDBController("root", "message-system", "127.0.0.1", 3001)
    user1 = db.register_user("matheus", "123456", "matheusbarcelosoliveira@gmail.com")
    user2 = db.register_user("wedsney", "123456", "matheusbarcelosoliveira@gmail.com")
    
    db.add_contact(user1, user2)
    db.add_contact(user2, user1)
    
    ...
    