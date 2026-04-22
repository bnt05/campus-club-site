from django.apps import AppConfig


class ClubsConfig(AppConfig):
    name = 'clubs'
    
    def ready(self):
        # 导入profile模块以连接信号
        import clubs.profile
