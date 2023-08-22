from common import *
import db

if __name__ == "__main__":

    init()
    db.init()

    db.new_users_db()
    clear_log_file()
    print(f"Log path: {log_path()}")

    df = db.get_users_df()

    ejovo = db.User("ejovo13", "test_hash", 0)
    jonbo = db.User("jonbo10", "test_hash", 0)

    try:
        db.add_user(ejovo)
        db.add_user(jonbo)
    except:
        print("Users already in database")


    print(db.get_users_df())
    print(db.get_users())

    print("New key:")
    print(generate_api_key(128))