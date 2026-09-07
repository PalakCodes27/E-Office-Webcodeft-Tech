import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import UserStatus


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    # =====================================================
    # CONNECT
    # =====================================================

    async def connect(self):

        self.user = self.scope["user"]

        # -------------------------------------------------
        # LOGIN CHECK
        # -------------------------------------------------

        if self.user.is_anonymous:

            await self.close()

            return

        # -------------------------------------------------
        # PERSONAL USER GROUP
        # -------------------------------------------------

        self.user_group = f"user_{self.user.id}"

        # -------------------------------------------------
        # ALL CHAT USERS GROUP
        # Used for online/offline updates
        # -------------------------------------------------

        self.chat_users_group = "chat_users"

        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.chat_users_group,
            self.channel_name
        )

        # -------------------------------------------------
        # ACCEPT CONNECTION
        # -------------------------------------------------

        await self.accept()

        # -------------------------------------------------
        # MARK USER ONLINE
        # -------------------------------------------------

        await self.set_user_online()

        # -------------------------------------------------
        # SEND USER LIST
        # -------------------------------------------------

        users = await self.get_chat_users()

        await self.send(
            text_data=json.dumps({
                "type": "user_list",
                "users": users,
            })
        )

        # -------------------------------------------------
        # BROADCAST ONLINE STATUS
        # -------------------------------------------------

        await self.channel_layer.group_send(
            self.chat_users_group,
            {
                "type": "user_status",
                "user_id": self.user.id,
                "is_online": True,
            }
        )

    # =====================================================
    # DISCONNECT
    # =====================================================

    async def disconnect(self, close_code):

        if hasattr(self, "user_group"):

            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )

        if hasattr(self, "chat_users_group"):

            await self.channel_layer.group_discard(
                self.chat_users_group,
                self.channel_name
            )

        # -------------------------------------------------
        # MARK USER OFFLINE
        # -------------------------------------------------

        if hasattr(self, "user") and not self.user.is_anonymous:

            await self.set_user_offline()

            # -------------------------------------------------
            # BROADCAST OFFLINE STATUS
            # -------------------------------------------------

            await self.channel_layer.group_send(
                "chat_users",
                {
                    "type": "user_status",
                    "user_id": self.user.id,
                    "is_online": False,
                }
            )

    # =====================================================
    # RECEIVE MESSAGE
    # =====================================================

    async def receive(self, text_data):

        try:

            data = json.loads(text_data)

        except json.JSONDecodeError:

            return

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        message = data.get("message")

        if not message:

            return

        # -------------------------------------------------
        # RECEIVER
        # -------------------------------------------------

        receiver_id = data.get("receiver_id")

        if not receiver_id:

            return

        # -------------------------------------------------
        # RECEIVER GROUP
        # -------------------------------------------------

        receiver_group = f"user_{receiver_id}"

        await self.channel_layer.group_send(
            receiver_group,
            {
                "type": "chat_message",
                "sender_id": self.user.id,
                "message": message,
            }
        )

    # =====================================================
    # CHAT MESSAGE
    # =====================================================

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "chat_message",
                "sender_id": event["sender_id"],
                "message": event["message"],
            })
        )

    # =====================================================
    # USER STATUS EVENT
    # =====================================================

    async def user_status(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "user_status",
                "user_id": event["user_id"],
                "is_online": event["is_online"],
            })
        )

    # =====================================================
    # DATABASE — ONLINE
    # =====================================================

    @database_sync_to_async
    def set_user_online(self):

        status, created = UserStatus.objects.get_or_create(
            user=self.user
        )

        status.is_online = True

        status.last_seen = timezone.now()

        status.save(
            update_fields=[
                "is_online",
                "last_seen"
            ]
        )

    # =====================================================
    # DATABASE — OFFLINE
    # =====================================================

    @database_sync_to_async
    def set_user_offline(self):

        status, created = UserStatus.objects.get_or_create(
            user=self.user
        )

        status.is_online = False

        status.last_seen = timezone.now()

        status.save(
            update_fields=[
                "is_online",
                "last_seen"
            ]
        )

    # =====================================================
    # GET CHAT USERS
    # =====================================================

    @database_sync_to_async
    def get_chat_users(self):

        users = User.objects.filter(
            role="employee"
        ).order_by(
            "first_name",
            "last_name",
            "username"
        )

        result = []

        for user in users:

            try:

                status = user.chat_status

                is_online = status.is_online

                last_seen = status.last_seen

            except UserStatus.DoesNotExist:

                is_online = False

                last_seen = None

            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            full_name = user.get_full_name().strip()

            if not full_name:

                full_name = user.username

            # -------------------------------------------------
            # USER DATA
            # -------------------------------------------------

            result.append({

                "id": user.id,

                "name": full_name,

                "username": user.username,

                "is_online": is_online,

                "last_seen": (
                    last_seen.isoformat()
                    if last_seen
                    else None
                ),

            })

        return result