from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import random


class Item(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    inventory = models.ManyToManyField(Item)
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def connect_rooms(self, destination_room, direction):
        destination_room_ID = destination_room.id
        try:
            destination_room = Room.objects.get(id=destination_room_ID)
        except Room.DoesNotExist:
            raise Exception("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destination_room_ID
            elif direction == "s":
                self.s_to = destination_room_ID
            elif direction == "e":
                self.e_to = destination_room_ID
            elif direction == "w":
                self.w_to = destination_room_ID
            else:
                print("Invalid direction")
                return
            self.save()

    def player_names(self, currentPlayerID):
        return [
            p.user.username
            for p in Player.objects.filter(current_room=self.id)
            if p.id != int(currentPlayerID)
        ]

    def player_UUIDs(self, currentPlayerID):
        return [
            p.uuid
            for p in Player.objects.filter(current_room=self.id)
            if p.id != int(currentPlayerID)
        ]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    inventory = models.ManyToManyField(Item)

    def initialize(self):
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

    def display(self):
        s = f"name     : {self.user.username}\n"
        s += f"location : {str(self.current_room)}"
        return print(s)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


class Monster(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    hp = models.IntegerField()
    ad = models.IntegerField()
    inventory = models.ManyToManyField(Item)

    def basic_attack(self, player: Player):
        player.hp -= self.ad
