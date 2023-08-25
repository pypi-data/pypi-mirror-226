from typing import Optional


def selectOptionQuestion(
    question: str, min: int, max: int, nullPossible: Optional[bool] = False
):
    invalid_input = True
    while invalid_input:
        user_input = input(f"{question} ")
        if user_input == "" and nullPossible:
            invalid_input = False
        elif inputIsInt(user_input):
            if min <= int(user_input) <= max:
                invalid_input = False
        else:
            print(f"\x1B[31mInvalid input! Please input within\x1B[37m {min}-{max}")
    return user_input


def inputIsInt(input: str):
    try:
        val = int(input)
        return True
    except ValueError:
        try:
            val = float(input)
            return False
        except ValueError:
            return False
