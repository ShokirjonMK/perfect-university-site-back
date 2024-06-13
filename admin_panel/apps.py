from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    name = "admin_panel"

    def ready(self):
        import admin_panel.signals