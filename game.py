import game
import random

items = {
    "Меч": {"атака": 10, "защита": 0, "описание": "Мощный меч, который наносит большой урон"},
    "Щит": {"атака": 0, "защита": 5, "описание": "Прочный щит, который защищает от атак"},
    "Зелье исцеления": {"атака": 0, "защита": 0, "описание": "Восстанавливает здоровье"},
    "Ключ": {"атака": 0, "защита": 0, "описание": "Открывает запертые двери"}
}

monsters = [
    {"имя": "Скелет", "атака": 5, "защита": 2, "здоровье": 10},
    {"имя": "Гоблин", "атака": 7, "защита": 1, "здоровье": 15},
    {"имя": "Огр", "атака": 12, "защита": 5, "здоровье": 25}
]

ROOMS = [
    {"name": "комната 1", "description": "Вы находитесь в первой комнате. Здесь темно.", "monster": None, "item": "Меч"},
    {"name": "комната 2", "description": "Вы находитесь во второй комнате. Здесь светло.", "monster": monsters[0], "item": None},
    {"name": "комната 3", "description": "Вы находитесь в третьей комнате. Здесь пахнет сыром.", "monster": None, "item": "Ключ"},
    {"name": "комната 4", "description": "Вы находитесь в четвёртой комнате. Здесь тихо.", "monster": monsters[1], "item": None},
    {"name": "комната 5", "description": "Вы находитесь в пятой комнате. Здесь много паутины.", "monster": None, "item": "Зелье исцеления"},
    {"name": "комната 6", "description": "Вы находитесь в шестой комнате.", "monster": None, "item": "Щит"},
    {"name": "комната 7", "description": "Вы находитесь в седьмой комнате. Это последняя комната. После данной комнаты следует дверь на выход, но напоследок нужно победить сильного монстра.", "monster": monsters[2], "item": None},
]

player = {
    "name": "",
    "health": 100,
    "max_health": 100,
    "inventory": set(),
    "current_room_index": 0,
}

def beginning():
    print("Вы зашли в замок, но потеряли выход. Вам нужно его найти пройдя по комнатам.")

def get_player_name():
    name = input("Введите ваше имя: ")
    player["name"] = name

def describe_room():
    room = ROOMS[player["current_room_index"]]
    print(room["description"])
    if room["monster"]:
        print(f"В этой комнате есть {room['monster']['имя']}.")
    if room["item"]:
        print(f"Вы видите {room['item']}.")

def move_to_next_room():
    if player["current_room_index"] < len(ROOMS) - 1:
        player["current_room_index"] += 1
        describe_room()
    else:
        print("Вы достигли конца замка! Вы можете выйти.")

def fight_monster(monster):
    print(f"Вы сражаетесь с {monster['имя']}!")
    
    while True:
        action = input("Вы хотите (1) атаковать или (2) убежать? ")
        if action == "1":
            damage = random.randint(10, 30)
            monster['здоровье'] -= damage
            print(f"Вы нанесли {damage} урона {monster['имя']}.")
            if monster['здоровье'] <= 0:
                print(f"Вы победили {monster['имя']}!")
                return True
            
            # Монстр отвечает
            monster_damage = random.randint(5, 20)
            player["health"] -= monster_damage
            print(f"{monster['имя']} нанес вам {monster_damage} урона!")
            
            if player["health"] <= 0:
                print("Вы погибли!")
                return False
            print(f"У вас осталось {player['health']} здоровья.")
        elif action == "2":
            print("Вы убегаете!")
            return True
        else:
            print("Некорректный ввод. Попробуйте снова.")

def collect_item(item):
    player["inventory"].add(item)
    print(f"Вы забрали {item}!")

def show_inventory():
    if player["inventory"]:
        print("Ваш инвентарь:")
        for item in player["inventory"]:
            print(f"- {item}: {items[item]['описание']}")
    else:
        print("Ваш инвентарь пуст.")

def show_health():
    print(f"Ваше текущее здоровье: {player['health']}")

def use_item(item):
    if item == "Зелье исцеления":
        if item in player["inventory"]:
            healing_amount = random.randint(20, 50)
            player["health"] += healing_amount
            if player["health"] > player["max_health"]:
                player["health"] = player["max_health"]
            player["inventory"].remove(item)
            print(f"Вы использовали {item} и восстановили {healing_amount} здоровья!")
        else:
            print("У вас нет этого предмета.")
    
    elif item == "Щит":
        if item in player["inventory"]:
            print("Вы используете щит для защиты!")
        else:
            print("У вас нет этого предмета.")
    
    else:
        print("Этот предмет не может быть использован.")

def main():
    beginning()
    get_player_name()
    describe_room()

    while True:
        command = input("Что вы хотите сделать? (переместиться/сражаться/забрать предмет/инвентарь/использовать/здоровье/выход): ").strip().lower()
        
        if command == "переместиться":
            move_to_next_room()

        elif command == "сражаться":
            room = ROOMS[player["current_room_index"]]
            if room["monster"]:
                if not fight_monster(room["monster"]):
                    break
                else:
                    room["monster"] = None 
            else:
                print("В этой комнате нет монстров.")
        
        elif command == "забрать предмет":
            room = ROOMS[player["current_room_index"]]
            if room["item"]:
                collect_item(room["item"])
                room["item"] = None 
            else:
                print("В этой комнате нет предметов для сбора.")
        
        elif command == "инвентарь":
            show_inventory()

        elif command == "использовать":
            item_to_use = input("Какой предмет вы хотите использовать? ").strip()
            use_item(item_to_use)
        
        elif command == "здоровье":
            show_health()
        
        elif command == "выход":
            if player["current_room_index"] == len(ROOMS) - 1:
                 print("Спасибо за игру! Вы покинули замок. Победа.")
                 break
            else:
                print("Спасибо за игру! Вы покинули игру. Проигрыш.")
            break
        else:
            print("Некорректная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()