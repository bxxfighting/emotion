from django.test import TestCase
from . import controllers as account_ctl
from .models import UserModel
from .models import RoleModel
from .models import UserRoleModel
from .models import ModModel
from .models import RoleModModel
from .models import UrlModel
from .models import ModUrlModel


class AccountTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        account_ctl.create_user('tt', '123')
        # 是否创建成功
        user = UserModel.objects.filter(username='tt', is_deleted=False).first()
        self.assertIsNotNone(user)
        # 验证密码
        self.assertEqual(user.check_password('123'), True)
        # 重复创建用户
        try:
            account_ctl.create_user('tt', '123')
        except Exception as e:
            self.assertEqual(e.errmsg, '用户已存在')

    def test_update_user(self):
        user = account_ctl.create_user('tt', '123')
        account_ctl.update_user(user.id, password='456')
        user = UserModel.objects.filter(id=user.id, is_deleted=False).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.check_password('456'), True)

    def test_delete_user(self):
        user = account_ctl.create_user('tt', '123')
        user_id = user.id
        account_ctl.delete_user(user_id)
        user = UserModel.objects.filter(id=user.id, is_deleted=False).first()
        self.assertIsNone(user)
        # 重复删除用户
        try:
            account_ctl.delete_user(user_id)
        except Exception as e:
            self.assertEqual(e.errmsg, '用户不存在')

    def test_create_role(self):
        account_ctl.create_role('中国好人', 'chinese good pipo')
        role = RoleModel.objects.filter(sign='chinese good pipo', is_deleted=False).first()
        self.assertIsNotNone(role)
        self.assertEqual(role.name, '中国好人')
        try:
            account_ctl.create_role('中国好人', 'chinese good pipo 2')
        except Exception as e:
            self.assertEqual(e.errmsg, '角色名或标识符已存在')
        try:
            account_ctl.create_role('中国好人 2', 'chinese good pipo')
        except Exception as e:
            self.assertEqual(e.errmsg, '角色名或标识符已存在')

    def test_update_role(self):
        role_1 = account_ctl.create_role('中国好人', 'chinese good pipo')
        role_2 = account_ctl.create_role('中国好人 2', 'chinese good pipo 2')
        try:
            account_ctl.update_role(role_1.id, '中国好人 2', 'chinese good pipo')
        except Exception as e:
            self.assertEqual(e.errmsg, '角色名或标识符已存在')
        try:
            account_ctl.update_role(role_1.id, '中国好人', 'chinese good pipo 2')
        except Exception as e:
            self.assertEqual(e.errmsg, '角色名或标识符已存在')
        account_ctl.update_role(role_1.id, '中国好人 3', 'chinese good pipo 3')
        role = RoleModel.objects.filter(id=role_1.id, is_deleted=False).first()
        self.assertEqual(role.name, '中国好人 3')
        self.assertEqual(role.sign, 'chinese good pipo 3')

    def test_delete_role(self):
        role = account_ctl.create_role('中国好人', 'chinese good pipo')
        role_id = role.id
        account_ctl.delete_role(role_id)
        try:
            account_ctl.delete_role(role_id)
        except Exception as e:
            self.assertEqual(e.errmsg, '角色不存在')

    def test_create_user_role(self):
        user = account_ctl.create_user('tt', '123')
        role_1 = account_ctl.create_role('中国好人', 'chinese good pipo')
        role_2 = account_ctl.create_role('中国好人 2', 'chinese good pipo 2')
        account_ctl.create_user_role(user.id, role_1.id)
        account_ctl.create_user_role(user.id, role_2.id)
        role_ids = UserRoleModel.objects.values_list('role_id', flat=True).filter(user_id=user.id).all()
        self.assertEqual(sorted(role_ids), [role_1.id, role_2.id])
        try:
            account_ctl.delete_role(role_1.id)
        except Exception as e:
            self.assertEqual(e.errmsg, '此角色已被用户关联，请先取消关联后重试')

    def test_create_mod(self):
        account_ctl.create_mod('好人', 'good man', 1)
        mod = ModModel.objects.filter(sign='good man', is_deleted=False).first()
        self.assertIsNotNone(mod)
        self.assertEqual(mod.name, '好人')
        try:
            mod = account_ctl.create_mod('好人', 'good man 2', 1)
        except Exception as e:
            self.assertEqual(e.errmsg, '模块名或标识符已存在')
        else:
            self.assertTrue(False, '重复创建了模块')
        try:
            mod = account_ctl.create_mod('好人 2', 'good man', 1)
        except Exception as e:
            self.assertEqual(e.errmsg, '模块名或标识符已存在')
        else:
            self.assertTrue(False, '重复创建了模块')

    def test_update_mod(self):
        mod_1 = account_ctl.create_mod('好人', 'good man', 1)
        mod_2 = account_ctl.create_mod('好人 2', 'good man 2', 2)
        try:
            account_ctl.update_mod(mod_1.id, '好人 2', 'good man', 1)
        except Exception as e:
            self.assertEqual(e.errmsg, '模块名或标识符已存在')
        else:
            self.assertTrue(False, '重复创建了模块')

        try:
            account_ctl.update_mod(mod_1.id, '好人', 'good man 2', 1)
        except Exception as e:
            self.assertEqual(e.errmsg, '模块名或标识符已存在')
        else:
            self.assertTrue(False, '重复创建了模块')
        account_ctl.update_mod(mod_1.id, '好人 3', 'good man 3', 1)
        mod = ModModel.objects.filter(id=mod_1.id, is_deleted=False).first()
        self.assertEqual(mod.name, '好人 3')
        self.assertEqual(mod.sign, 'good man 3')

    def test_delete_mod(self):
        mod = account_ctl.create_mod('好人', 'good man', 1)
        mod_id = mod.id
        account_ctl.delete_mod(mod_id)
        try:
            account_ctl.delete_mod(mod_id)
        except Exception as e:
            self.assertEqual(e.errmsg, '模块不存在')

    def test_create_role_mod(self):
        role = account_ctl.create_role('牛人', 'nb')
        mod_1 = account_ctl.create_mod('好人', 'gp', 1)
        mod_2 = account_ctl.create_mod('好人 2', 'gp 2', 2)
        account_ctl.create_role_mod(role.id, mod_1.id)
        account_ctl.create_role_mod(role.id, mod_2.id)

        mod_ids = RoleModModel.objects.values_list('mod_id', flat=True).filter(role_id=role.id).all()
        self.assertEqual(sorted(mod_ids), [mod_1.id, mod_2.id])
        try:
            account_ctl.delete_mod(mod_1.id)
        except Exception as e:
            self.assertEqual(e.errmsg, '此模块已被角色关联，请先取消关联后重试')

    def test_create_supper_user(self):
        account_ctl.create_supper_user('root', 'root')
        user = UserModel.objects.filter(username='root', is_deleted=False).first()
        self.assertIsNotNone(user)
        # 密码正确
        self.assertEqual(user.check_password('root'), True)
        role = RoleModel.objects.filter(sign='root', is_deleted=False).first()
        self.assertIsNotNone(role)
        # 角色信息正确
        self.assertEqual(role.name, '超级用户')
        user_role = UserRoleModel.objects.filter(user_id=user.id, is_deleted=False).first()
        self.assertIsNotNone(user_role)
        self.assertEqual(user_role.role_id, role.id)
        # 模块
        user_mod = ModModel.objects.filter(sign='user', is_deleted=False).first()
        self.assertIsNotNone(user_mod)
        self.assertEqual(user_mod.name, '用户管理')
        self.assertEqual(user_mod.rank, 1)
        role_mod = ModModel.objects.filter(sign='role', is_deleted=False).first()
        self.assertIsNotNone(role_mod)
        self.assertEqual(role_mod.name, '角色管理')
        self.assertEqual(role_mod.rank, 2)
        mod_mod = ModModel.objects.filter(sign='mod', is_deleted=False).first()
        self.assertIsNotNone(mod_mod)
        self.assertEqual(mod_mod.name, '模块管理')
        self.assertEqual(mod_mod.rank, 3)
        url_mod = ModModel.objects.filter(sign='url', is_deleted=False).first()
        self.assertIsNotNone(url_mod)
        self.assertEqual(url_mod.name, 'URL管理')
        self.assertEqual(url_mod.rank, 4)
        # 角色关联到了模块
        mod_ids = RoleModModel.objects.values_list('mod_id', flat=True)\
                .filter(role_id=role.id, is_deleted=False).all()
        self.assertEqual(sorted(mod_ids), [user_mod.id, role_mod.id, mod_mod.id, url_mod.id])
        url_list = [
            ('角色列表', '/api/v1/account/role/list/'),
            ('角色创建', '/api/v1/account/role/create/'),
            ('角色编辑', '/api/v1/account/role/update/'),
            ('角色删除', '/api/v1/account/role/delete/'),
        ]
        UrlModel.objects.filter()
