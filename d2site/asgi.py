import os
from django.core.asgi import get_asgi_application
from d2site.scripts.coordinator import Coordinator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd2site.settings')
django_asgi_app = get_asgi_application()


class CustomASGIApp:
    def __init__(self, app):
        self.app = app
        self.coordinator = Coordinator()

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    await self.coordinator.connection()  # Запуск метода при старте
                    break
                elif message['type'] == 'lifespan.shutdown':
                    await self.coordinator.disconnect()  # Очистка ресурсов при остановке
                    break
                else:
                    break
        else:
            await self.app(scope, receive, send)


app = CustomASGIApp(django_asgi_app)
