from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        registered_users_group: Group = Group.objects.get_or_create(name="Normal user")[0]
        registered_users_permissions_code_names = ["add_user", "change_user", "view_user", "add_uservote",
                                                   "view_uservote", "add_vote", "view_vote", "change_vote",
                                                   "add_report"]
        for registered_users_permissions_code_name in registered_users_permissions_code_names:
            new_permission_for_registered_users_group = \
                    Permission.objects.filter(codename=registered_users_permissions_code_name).first()
            if not new_permission_for_registered_users_group:
                raise SyntaxError(
                    f"Invalid permission code name: '{registered_users_permissions_code_name}'"
                    f"Неправильно кодовое название прав: '{registered_users_permissions_code_name}'"
                )
            registered_users_group.permissions.add(new_permission_for_registered_users_group)
