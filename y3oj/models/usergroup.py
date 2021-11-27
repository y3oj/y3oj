from y3oj.modules.user import get_user, get_user_by_key


class UserGroupInitError(Exception):
    pass


class UserGroup(object):
    def __init__(self, id: str, name: str, user_list):
        self.id = id
        self.name = name

        self.id_list = []
        self.key_list = []
        self.user_list = []
        for user_str in user_list:
            if user_str.isdigit():
                user = get_user_by_key(user_str)
            else:
                user = get_user(user_str)
            if user is None:
                raise UserGroupInitError(f'用户 {user_str} 不存在')
            self.id_list.append(user.id)
            self.key_list.append(user.key)
            self.user_list.append(user)

    def __len__(self):
        return len(self.user_list)

    def __repr__(self):
        return '<UserGroup [%s]>' % (', '.join(self.id_list))
