from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.player_names(player_id)
    r = {
        "player": {
            "uuid": uuid,
            "id": player_id,
            "current_room": room.id,
            # "inventory" : player.inventory,
        },
        "room": {
            "title": room.title,
            "description": room.description,
            "players": players,
            "room_x": room.x,
            "room_y": room.y,
            "id": room.id,
            # "inventory": room.inventory,
        },
    }

    return JsonResponse(r, safe=True)


#        {
#            "uuid": uuid,
#            "name": player.user.username,
#            "title": room.title,
#            "description": room.description,
#            "players": players,
#        },
#        safe=True,
#    )


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data["direction"]
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.current_room = nextRoomID
        player.save()
        players = nextRoom.player_names(player_id)
        currentPlayerUUIDs = room.player_UUIDs(player_id)
        nextPlayerUUIDs = nextRoom.player_UUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse(
            {
                "name": player.user.username,
                "title": nextRoom.title,
                "id": room.id,
                "room_x": room.x,
                "room_y": room.y,
                "description": nextRoom.description,
                "players": players,
                "error_msg": "",
            },
            safe=True,
        )
    else:
        players = room.player_names(player_id)
        return JsonResponse(
            {
                "name": player.user.username,
                "title": room.title,
                "id": room.id,
                "description": room.description,
                "players": players,
                "error_msg": "You cannot move that way.",
            },
            safe=True,
        )


@api_view(["GET"])
def rooms(request):
    rooms = Room.objects.all()
    nodes = []
    links = []

    for i in rooms:
        nodes.append(
            {"id": i.id, "title": i.title,}
        )
        for j in ["n_to", "s_to", "e_to", "w_to"]:
            z = getattr(i, j)
            if z > 0:
                links.append({"source": i.id, "target": z})

    data = {
        "nodes": nodes,
        "links": links,
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({"error": "Not yet implemented"}, safe=True, status=500)
