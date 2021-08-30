from datetime import datetime
import hashlib
myHash = hashlib.md5()


class Token:
    def create_token(username, password):
        token = username + "----" + password + str(datetime.now())
        myHash.update(token.encode(encoding='utf-8'))
        return myHash.hexdigest()

    def get_token(toolRedis, username):
        try:
            store_token = toolRedis.get(username)
            if store_token == None:
                return False
            else:
                return store_token
        except:
            return False

    def check_token(toolRedis, username, token):
        try:
            old_token = Token.get_token(toolRedis, username)
            print('Redis中的token:', old_token)
            print('用户Token:', token)
            if not old_token:
                return False
            if str(old_token, encoding="utf8") != token:
                return False
            return True
        except:
            return False
