import sys

from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'
    registered_users_permissions_code_names = ["add_user", "change_user", "view_user", "add_uservote",
                                               "view_uservote", "add_vote", "view_vote", "change_vote",
                                               "add_report"]
    moderator_group_permissions_code_names = registered_users_permissions_code_names + ["delete_user", "delete_vote",
                                                                                        "delete_report",
                                                                                        "change_report",
                                                                                        "view_report"]

    def _register_normal_user_group(self):
        from django.contrib.auth.models import Group, Permission
        registered_users_group: Group = Group.objects.get_or_create(name="Normal user")[0]
        for registered_users_permissions_code_name in self.registered_users_permissions_code_names:
            new_permission_for_registered_users_group = \
                Permission.objects.filter(codename=registered_users_permissions_code_name).first()
            if not new_permission_for_registered_users_group:
                raise SyntaxError(
                    f"Invalid permission code name: '{registered_users_permissions_code_name}'"
                    f"Неправильно кодовое название прав: '{registered_users_permissions_code_name}'"
                )
            registered_users_group.permissions.add(new_permission_for_registered_users_group)

    def _register_moderator_user_group(self):
        from django.contrib.auth.models import Group, Permission
        moderator_group: Group = Group.objects.get_or_create(name="Moderator")[0]
        for moderator_group_permission_code_name in self.moderator_group_permissions_code_names:
            new_permission_for_registered_users_group = \
                Permission.objects.filter(codename=moderator_group_permission_code_name).first()
            if not new_permission_for_registered_users_group:
                raise SyntaxError(
                    f"Invalid permission code name: '{moderator_group_permission_code_name}'"
                    f"Неправильно кодовое название прав: '{moderator_group_permission_code_name}'"
                )
            moderator_group.permissions.add(new_permission_for_registered_users_group)

    def ready(self):
        super().ready()
        if 'runserver' in sys.argv:
            self._register_normal_user_group()
            self._register_moderator_user_group()
