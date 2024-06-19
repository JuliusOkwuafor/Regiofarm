import json

from channels.generic.websocket import AsyncWebsocketConsumer
from notification.models import Notification
from asgiref.sync import sync_to_async, async_to_sync


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            print("rejecting...")
            self.group_name = "disconnect"
            self.send(text_data="no or invalid token")
            self.close(reason="no or invalid token")
        else:
            print("user", self.scope["user"])
            self.group_name = str(self.scope["user"].pk)
            print("from channels", self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send_all_notifications()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("Disconnected!")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json["type"]

        if event_type == "send_message":
            message = text_data_json.get("message")
            pass
        elif event_type == "mark_read":
            notification_ids = text_data_json.get("ids")
            ids = notification_ids.split(",")
            print(ids)
            print(type(ids))
            for notfication_id in ids:
                try:

                    print(notfication_id)
                    notification = await Notification.objects.aget(
                        id=notfication_id,
                        user=self.scope["user"],
                    )
                    notification.is_read = True
                    await notification.asave()
                    await self.send(f"success updating {notfication_id}")
                except Notification.DoesNotExist:
                    pass

        # event = {
        #     "type": "send_message",
        #     "message": message,
        # }

        # await self.channel_layer.group_send(self.group_name, event)

    async def notify(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @sync_to_async
    def send_all_notifications(self):
        notifications = Notification.objects.filter(user=self.scope["user"])
        notifications_list = []
        for notification in notifications:
            notifications_list.append(
                {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "is_read": notification.is_read,
                }
            )
        async_to_sync(self.channel_layer.group_send)(
            str(self.scope["user"].pk),
            {
                "type": "notify",
                "message": notifications_list,
            },
        )
