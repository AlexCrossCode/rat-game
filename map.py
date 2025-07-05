import os

def load_map(room_number):
    folder = "maps"
    filename = f"{room_number}.txt"
    path = os.path.join(folder, filename)

    with open(path, "r") as file:
        lines = file.readlines()
    return [line.rstrip("\n") for line in lines]
