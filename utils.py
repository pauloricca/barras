import random
import shutil


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))

def get_random_char():
    return chr(random.randint(33, 126))

# Mutate error message characters
def mutate(string_or_string_list, probability):
    is_list = isinstance(string_or_string_list, list)

    string_list = string_or_string_list if is_list else [string_or_string_list]
    new_string_list = [None] * len(string_list)

    for i in range(len(string_list)):
        new_string_list[i] = "".join(
            (get_random_char() if random.random() < probability else char) for char in string_list[i]
        )

    if is_list:
        return new_string_list
    else:
        return new_string_list[0]
