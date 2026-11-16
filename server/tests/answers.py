TEST_SERIALIZING_ONE_POKEMON_ANSWER = {
    "id": 1,
    "name": "Pikachu",
    "level": 13,
    "type": "electric",
    "description": "Unknown",
    "captured": True,
    "date_encountered": "2026-11-09",
    "current_moves": [
        {
            "id": 1,
            "move": {
                "id": 1,
                "name": "Thunderbolt",
                "description": "A strong electric blast that may also leave the target paralyzed.",
                "type": "electric",
                "power": 90,
                "pp": 15,
            },
            "current_pp": 15,
            "disabled": False,
        },
        {
            "id": 2,
            "move": {
                "id": 2,
                "name": "Quick Attack",
                "description": "An extremely fast attack that always strikes first.",
                "type": "normal",
                "power": 40,
                "pp": 30,
            },
            "current_pp": 12,
            "disabled": False,
        },
        {
            "id": 3,
            "move": {
                "id": 3,
                "name": "Thunder Shock",
                "description": "A jolt of electricity that may also leave the target paralyzed.",
                "type": "electric",
                "power": 40,
                "pp": 30,
            },
            "current_pp": 30,
            "disabled": True,
        },
    ],
}
TEST_SERIALIZING_EVERY_POKEMON = ["Pikachu", "Bulbasaur", "Charizard", "Mew", "Snorlax"]
TEST_GET_A_MOVE_ANSWER = {
    "id": 1,
    "name": "Thunderbolt",
    "description": "A strong electric blast that may also leave the target paralyzed.",
    "type": "electric",
    "power": 90,
    "pp": 15,
}
TEST_GET_A_POKEMON_MOVE_ANSWER = {
    "id": 1,
    "move": TEST_GET_A_MOVE_ANSWER,
    "current_pp": 15,
    "disabled": False,
}
