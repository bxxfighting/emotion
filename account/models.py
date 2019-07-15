from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from base.models import BaseModel


class UserModel(BaseModel):
    '''
    用户表
    '''
    ST_NORMAL = 1
    ST_FORBIDDEN = 2
    ST_CHOICES = (
        (ST_NORMAL, '正常'),
        (ST_FORBIDDEN, '禁用'),
    )

    username = models.CharField('账户', max_length=128)
    password = models.CharField('密码', max_length=256)
    name = models.CharField('姓名', max_length=128, null=True, default='')
    email = models.CharField('邮箱', max_length=128, null=True, default='')
    phone = models.CharField('联系方式', max_length=64, null=True, default='')
    status = models.IntegerField('状态', choices=ST_CHOICES, null=True, default=ST_NORMAL)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }
        objs = UserRoleModel.objects.filter(is_deleted=False, user_id=self.id).all()
        roles = [obj.role.to_dict() for obj in objs]
        data['roles'] = roles
        return data

    def set_password(self, password):
        '''
        设置密码
        '''
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        '''
        校验密码
        '''
        return check_password(password, self.password)

    class Meta:
        db_table = 'user'


class RoleModel(BaseModel):
    '''
    角色表
    '''
    name = models.CharField('角色名', max_length=128)
    sign = models.CharField('标识', max_length=128)

    class Meta:
        db_table = 'role'

    def to_dict(self):
        data = super().to_dict()
        objs = RoleModModel.objects.filter(is_deleted=False, role_id=self.id).all()
        mods = [obj.mod.to_dict() for obj in objs]
        data['mods'] = mods
        return data


class UserRoleModel(BaseModel):
    '''
    用户与角色关联关系表
    '''
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_role'


class ModModel(BaseModel):
    '''
    模块
    '''
    name = models.CharField('模块名', max_length=128)
    sign = models.CharField('标识', max_length=128)
    rank = models.IntegerField('排序值', default=0)

    class Meta:
        db_table = 'mod'

    def to_dict(self):
        data = super().to_dict()
        objs = ModUrlModel.objects.filter(is_deleted=False, mod_id=self.id).all()
        urls = [obj.url.to_dict() for obj in objs]
        data['urls'] = urls
        return data


class RoleModModel(BaseModel):
    '''
    角色与模块关联关系表
    '''
    role = models.ForeignKey(RoleModel)
    mod = models.ForeignKey(ModModel)

    class Meta:
        db_table = 'role_mod'


class UrlModel(BaseModel):
    '''
    URL
    '''
    name = models.CharField('url名称', max_length=128)
    url = models.TextField('url地址')

    class Meta:
        db_table = 'url'


class ModUrlModel(BaseModel):
    '''
    模块与URL关联关系
    '''
    mod = models.ForeignKey(ModModel)
    url = models.ForeignKey(UrlModel)

    class Meta:
        db_table = 'mod_url'
