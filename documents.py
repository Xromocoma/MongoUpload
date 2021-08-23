from mongoengine import fields, DynamicDocument,DynamicEmbeddedDocument


# Chat Room
class Room(DynamicDocument):
    room_avatar_id = fields.StringField(required=True, default="")

    meta = {
        'collection': 'room',
        'db_alias': 'src-chat'
    }


# Chat Room Message
class MessageContent(DynamicEmbeddedDocument):
    data_id = fields.StringField(required=True, default="")
    preview_id = fields.StringField(required=True, default="")


class RoomMessage(DynamicDocument):
    message_content = fields.EmbeddedDocumentField(MessageContent, required=True)
    meta = {
        'collection': 'room_message',
        'db_alias': 'src-chat'
    }


# DialogMessage
class DialogMessageContent(DynamicEmbeddedDocument):
    data_id = fields.StringField(default='')
    preview_id = fields.StringField(default='')


class DialogMessage(DynamicDocument):
    message_content = fields.EmbeddedDocumentField(DialogMessageContent)
    meta = {
        'collection': 'dialog_message',
        'db_alias': 'src-chat'
    }


# Event
class EventImageData(DynamicEmbeddedDocument):
    id = fields.StringField()


class EventImage(DynamicEmbeddedDocument):
    avatar = fields.EmbeddedDocumentField(EventImageData)
    cover = fields.EmbeddedDocumentField(EventImageData)
    banner = fields.EmbeddedDocumentField(EventImageData)


class Event(DynamicDocument):
    event_image = fields.EmbeddedDocumentField(EventImage)
    meta = {
        'collection': 'event',
        'db_alias': 'src-event'
    }


# Greetings

class Greetings(DynamicDocument):
    greeting_avatar_id = fields.StringField(required=True)
    meta = {
        'collection': 'greeting',
        'db_alias': 'src-profile'
    }


# Photo

class Photo(DynamicDocument):
    photo_content_id = fields.StringField()
    meta = {
        'collection': 'photo',
        'db_alias': 'src-profile'
    }


# User
class UserAvatar(DynamicEmbeddedDocument):
    id = fields.StringField()
    crop = fields.DynamicField()


class User(DynamicDocument):
    user_avatar = fields.EmbeddedDocumentField(UserAvatar)
    meta = {
        'collection': 'user',
        'db_alias': 'src-profile'
    }
