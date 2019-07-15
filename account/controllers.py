from django.db import transaction
from django.db.models import Q
from django.core.signing import TimestampSigner

from base import errors
from .models import UserModel
from .models import RoleModel
from .models import UserRoleModel
from .models import ModModel
from .models import RoleModModel
from .models import UrlModel
from .models import ModUrlModel


@transaction.atomic()
def create_supper_user(username, password):
    '''
    创建超级用户
    '''
    user = create_user(username, password)
    role = create_role('超级用户', 'root')
    create_user_role(user.id, role.id)
    user_mod = create_mod('用户管理', 'user', 1)
    role_mod = create_mod('角色管理', 'role', 2)
    mod_mod = create_mod('模块管理', 'mod', 3)
    url_mod = create_mod('URL管理', 'url', 4)
    create_role_mod(role.id, user_mod.id)
    create_role_mod(role.id, role_mod.id)
    create_role_mod(role.id, mod_mod.id)
    create_role_mod(role.id, url_mod.id)
    url_list = [
        ('角色列表', '/api/v1/account/role/list/'),
        ('角色创建', '/api/v1/account/role/create/'),
        ('角色编辑', '/api/v1/account/role/update/'),
        ('角色删除', '/api/v1/account/role/delete/'),
    ]
    url_ids = []
    for name, url in url_list:
        obj = create_url(name, url)
        url_ids.append(obj.id)
    create_mod_urls(role_mod.id, url_ids)
    url_list = [
        ('模块列表', '/api/v1/account/mod/list/'),
        ('模块创建', '/api/v1/account/mod/create/'),
        ('模块编辑', '/api/v1/account/mod/update/'),
        ('模块删除', '/api/v1/account/mod/delete/'),
    ]
    url_ids = []
    for name, url in url_list:
        obj = create_url(name, url)
        url_ids.append(obj.id)
    create_mod_urls(mod_mod.id, url_ids)
    url_list = [
        ('用户列表', '/api/v1/account/user/list/'),
        ('用户创建', '/api/v1/account/user/create/'),
        ('用户编辑', '/api/v1/account/user/update/'),
        ('用户删除', '/api/v1/account/user/delete/'),
    ]
    url_ids = []
    for name, url in url_list:
        obj = create_url(name, url)
        url_ids.append(obj.id)
    create_mod_urls(user_mod.id, url_ids)
    url_list = [
        ('URL列表', '/api/v1/account/url/list/'),
        ('URL创建', '/api/v1/account/url/create/'),
        ('URL编辑', '/api/v1/account/url/update/'),
        ('URL删除', '/api/v1/account/url/delete/'),
    ]
    url_ids = []
    for name, url in url_list:
        obj = create_url(name, url)
        url_ids.append(obj.id)
    create_mod_urls(url_mod.id, url_ids)


def create_role(name, sign):
    '''
    创建角色
    '''
    role = RoleModel.objects.filter(Q(name=name)|Q(sign=sign), is_deleted=False).first()
    if role:
        raise errors.CommonError('角色名或标识符已存在')
    data = {
        'name': name,
        'sign': sign,
    }
    role = RoleModel.objects.create(**data)
    return role


def update_role(role_id, name, sign):
    '''
    编辑角色
    '''
    role = RoleModel.objects.filter(Q(name=name)|Q(sign=sign), is_deleted=False).exclude(id=role_id).first()
    if role:
        raise errors.CommonError('角色名或标识符已存在')
    role = RoleModel.objects.filter(id=role_id, is_deleted=False).first()
    if not role:
        raise errors.CommonError('角色不存在')
    role.name = name
    role.sign = sign
    role.save()
    return role


def delete_role(role_id):
    '''
    删除角色
    '''
    role = RoleModel.objects.filter(id=role_id, is_deleted=False).first()
    if not role:
        raise errors.CommonError('角色不存在')
    if UserRoleModel.objects.filter(role_id=role_id, is_deleted=False).count():
        raise errors.CommonError('此角色已被用户关联，请先取消关联后重试')
    role.is_deleted = True
    role.save()
    RoleModModel.objects.filter(role_id=role_id, is_deleted=False).update(is_deleted=True)
    return role


def create_user(username, password, name=None, phone=None, email=None):
    '''
    创建用户
    '''
    user = UserModel.objects.filter(username=username, is_deleted=False).first()
    if user:
        raise errors.CommonError('用户已存在')
    data = {
        'username': username,
        'name': name,
        'phone': phone,
        'email': email,
    }
    user = UserModel.objects.create(**data)
    user.set_password(password)
    return user


def update_user(user_id, name=None, password=None, phone=None, email=None):
    '''
    编辑用户
    '''
    user = UserModel.objects.filter(id=user_id, is_deleted=False).first()
    if not user:
        raise errors.CommonError('用户不存在')
    user.name = name
    user.phone = phone
    user.email = email
    if password:
        user.set_password(password)
    user.save()
    return user


def delete_user(user_id):
    '''
    删除用户
    '''
    user = UserModel.objects.filter(id=user_id, is_deleted=False).first()
    if not user:
        raise errors.CommonError('用户不存在')
    if user.username == 'root':
        raise errors.CommonError('超级用户不允许删除')
    user.is_deleted = True
    user.save()
    UserRoleModel.objects.filter(user_id=user_id, is_deleted=False).update(is_deleted=True)
    return user


def create_user_role(user_id, role_id):
    '''
    创建用户与角色关联关系
    '''
    data = {
        'user_id': user_id,
        'role_id': role_id,
    }
    UserRoleModel.objects.create(**data)


def create_mod(name, sign, rank):
    '''
    创建模块
    '''
    mod = ModModel.objects.filter(Q(name=name)|Q(sign=sign), is_deleted=False).first()
    if mod:
        raise errors.CommonError('模块名或标识符已存在')
    data = {
        'name': name,
        'sign': sign,
        'rank': rank,
    }
    mod = ModModel.objects.create(**data)
    return mod


def update_mod(mod_id, name, sign, rank):
    '''
    编辑模块
    '''
    mod = ModModel.objects.filter(Q(name=name)|Q(sign=sign), is_deleted=False).exclude(id=mod_id).first()
    if mod:
        raise errors.CommonError('模块名或标识符已存在')
    mod = ModModel.objects.filter(id=mod_id, is_deleted=False).first()
    if not mod:
        raise errors.CommonError('模块不存在')
    mod.name = name
    mod.sign = sign
    mod.rank = rank
    mod.save()
    return mod


def delete_mod(mod_id):
    '''
    删除模块
    '''
    mod = ModModel.objects.filter(id=mod_id, is_deleted=False).first()
    if not mod:
        raise errors.CommonError('模块不存在')
    if RoleModModel.objects.filter(mod_id=mod_id, is_deleted=False).count():
        raise errors.CommonError('此模块已被角色关联，请先取消关联后重试')
    mod.is_deleted = True
    mod.save()
    ModUrlModel.objects.filter(mod_id=mod_id, is_deleted=False).update(is_deleted=True)
    return mod


def create_role_mod(role_id, mod_id):
    '''
    创建角色与模块关联关系
    '''
    data = {
        'role_id': role_id,
        'mod_id': mod_id,
    }
    RoleModModel.objects.create(**data)


def login(username, password):
    '''
    登录
    '''
    user = UserModel.objects.filter(username=username, is_deleted=False).first()
    if not user:
        raise errors.CommonError('用户名或密码错误')
    if not user.check_password(password):
        raise errors.CommonError('用户名或密码错误')
    return user


def gen_token(user_id):
    signer = TimestampSigner()
    token = signer.sign(user_id)
    return token


def get_mod_list_by_user_id(user_id):
    '''
    获取用户对应的模型列表
    '''
    user_roles = UserRoleModel.objects.filter(user_id=user_id, role__is_deleted=False, is_deleted=False).all()
    role_ids = [user_role.role_id for user_role in user_roles]
    role_mods = RoleModModel.objects.filter(role__id__in=role_ids, mod__is_deleted=False, is_deleted=False)\
            .order_by('mod__rank').all()
    mods = [role_mod.mod.to_dict() for role_mod in role_mods]
    return mods


def get_user_list(page_num=None, page_size=None):
    '''
    获取用户列表
    '''

    base_query = UserModel.objects.filter(is_deleted=False).exclude(username='root').order_by('id')
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def get_role_list(page_num=None, page_size=None):
    '''
    获取角色列表
    '''
    base_query = RoleModel.objects.filter(is_deleted=False).exclude(sign='root').order_by('-id')
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def get_mod_list(page_num=None, page_size=None):
    '''
    获取模块列表
    '''
    base_query = ModModel.objects.filter(is_deleted=False).order_by('-id')
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def create_role_mods(role_id, mod_ids):
    '''
    创建角色模块
    '''
    obj_list = []
    for mod_id in mod_ids:
        data = {
            'role_id': role_id,
            'mod_id': mod_id,
        }
        obj = RoleModModel(**data)
        obj_list.append(obj)
    if obj_list:
        RoleModModel.objects.bulk_create(obj_list)


def delete_role_mods(role_id, mod_ids):
    '''
    删除角色模块
    '''
    query = {
        'role_id': role_id,
        'is_deleted': False,
    }
    update_data = {
        'is_deleted': True,
    }
    RoleModModel.objects.filter(role_id=role_id, is_deleted=False, mod_id__in=mod_ids)\
            .update(is_deleted=True)


def set_role_mods(role_id, mod_ids):
    '''
    设置角色模块集
    '''
    query = {
        'is_deleted': False,
        'role_id': role_id,
    }
    objs = RoleModModel.objects.filter(is_deleted=False, role_id=role_id).all()
    existed_ids = [obj.mod_id for obj in objs]
    if existed_ids:
        add_ids = list(set(mod_ids) - set(existed_ids))
        delete_ids = list(set(existed_ids) - set(mod_ids))
    else:
        add_ids = mod_ids
        delete_ids = []
    if add_ids:
        create_role_mods(role_id, add_ids)
    if delete_ids:
        delete_role_mods(role_id, delete_ids)


def create_user_roles(user_id, role_ids):
    '''
    创建用户关联角色关系
    '''
    obj_list = []
    for role_id in role_ids:
        data = {
            'user_id': user_id,
            'role_id': role_id,
        }
        obj = UserRoleModel(**data)
        obj_list.append(obj)
    if obj_list:
        UserRoleModel.objects.bulk_create(obj_list)


def delete_user_roles(user_id, role_ids):
    '''
    删除用户关联角色关系
    '''
    query = {
        'user_id': user_id,
        'is_deleted': False,
    }
    update_data = {
        'is_deleted': True,
    }
    UserRoleModel.objects.filter(user_id=user_id, is_deleted=False, role_id__in=role_ids)\
            .update(is_deleted=True)


def set_user_roles(user_id, role_ids):
    '''
    设置用户关联角色关系
    '''
    query = {
        'is_deleted': False,
        'user_id': user_id,
    }
    objs = UserRoleModel.objects.filter(is_deleted=False, user_id=user_id).all()
    existed_ids = [obj.role_id for obj in objs]
    if existed_ids:
        add_ids = list(set(role_ids) - set(existed_ids))
        delete_ids = list(set(existed_ids) - set(role_ids))
    else:
        add_ids = role_ids
        delete_ids = []
    if add_ids:
        create_user_roles(user_id, add_ids)
    if delete_ids:
        delete_user_roles(user_id, delete_ids)


def change_password(user_id, old_password, new_password):
    '''
    修改密码
    '''
    user = UserModel.objects.filter(id=user_id, is_deleted=False).first()
    if not user:
        raise errors.CommonError('用户不存在')
    if not user.check_password(old_password):
        raise errors.CommonError('原密码不正确')
    user.set_password(new_password)
    return user


def get_url_list(page_num=None, page_size=None):
    '''
    获取URL列表
    '''
    base_query = UrlModel.objects.filter(is_deleted=False).order_by('-id')
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data


def create_url(name, url):
    '''
    创建URL
    '''
    obj = UrlModel.objects.filter(Q(name=name)|Q(url=url), is_deleted=False).first()
    if obj:
        raise errors.CommonError('URL名或标识符已存在')
    data = {
        'name': name,
        'url': url,
    }
    obj = UrlModel.objects.create(**data)
    return obj


def update_url(url_id, name, url):
    '''
    编辑URL
    '''
    obj = UrlModel.objects.filter(Q(name=name)|Q(url=url), is_deleted=False).exclude(id=url_id).first()
    if obj:
        raise errors.CommonError('URL名或标识符已存在')
    obj = UrlModel.objects.filter(id=url_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('URL不存在')
    obj.name = name
    obj.url = url
    obj.save()
    return obj


def delete_url(url_id):
    '''
    删除URL
    '''
    obj = UrlModel.objects.filter(id=url_id, is_deleted=False).first()
    if not obj:
        raise errors.CommonError('URL不存在')
    if ModUrlModel.objects.filter(url_id=url_id, is_deleted=False).count():
        raise errors.CommonError('此URL已被模块关联，请先取消关联后重试')
    obj.is_deleted = True
    obj.save()
    return obj


def create_mod_urls(mod_id, url_ids):
    '''
    创建模块URL
    '''
    obj_list = []
    for url_id in url_ids:
        data = {
            'mod_id': mod_id,
            'url_id': url_id,
        }
        obj = ModUrlModel(**data)
        obj_list.append(obj)
    if obj_list:
        ModUrlModel.objects.bulk_create(obj_list)


def delete_mod_urls(mod_id, url_ids):
    '''
    删除模块URL
    '''
    query = {
        'mod_id': mod_id,
        'is_deleted': False,
    }
    update_data = {
        'is_deleted': True,
    }
    ModUrlModel.objects.filter(mod_id=mod_id, is_deleted=False, url_id__in=url_ids)\
            .update(is_deleted=True)


def set_mod_urls(mod_id, url_ids):
    '''
    设置模块URL集
    '''
    query = {
        'is_deleted': False,
        'mod_id': mod_id,
    }
    objs = ModUrlModel.objects.filter(is_deleted=False, mod_id=mod_id).all()
    existed_ids = [obj.url_id for obj in objs]
    if existed_ids:
        add_ids = list(set(url_ids) - set(existed_ids))
        delete_ids = list(set(existed_ids) - set(url_ids))
    else:
        add_ids = url_ids
        delete_ids = []
    if add_ids:
        create_mod_urls(mod_id, add_ids)
    if delete_ids:
        delete_mod_urls(mod_id, delete_ids)


def is_permission(user_id, url):
    '''
    验证权限
    这里只先进行最容易的操作，实际情况应该对用户的权限进行缓存，并且来维护
    '''
    user_roles = UserRoleModel.objects.filter(user_id=user_id, is_deleted=False).all()
    role_ids = [obj.role.id for obj in user_roles]
    role_mods = RoleModModel.objects.filter(role_id__in=role_ids, is_deleted=False).all()
    mod_ids = [obj.mod.id for obj in role_mods]
    if ModUrlModel.objects.filter(mod_id__in=mod_ids, url__url=url, is_deleted=False).count():
        return True
    else:
        return False


def list_user_by_role(role_sign):
    '''
    根据角色标识获取用户列表
    '''
    role = RoleModel.objects.filter(sign=role_sign, is_deleted=False).first()
    if not role:
        raise errors.CommonError('角色不存在')
    user_ids = UserRoleModel.objects.distinct().values_list('user_id', flat=True)\
            .filter(role_id=role.id, is_deleted=False).all()
    users = UserModel.objects.filter(id__in=user_ids, is_deleted=False).all()
    data_list = [user.to_dict() for user in users]
    data = {
        'total': len(users),
        'data_list': data_list,
    }
    return data
