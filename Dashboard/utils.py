import random
import string


def slug_generator(cls, start, end):
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)

    while True:
        randomStr = "".join(random.choices(letters, k=random.randint(start, end)))
        qs = cls.objects.filter(slug=randomStr)
        if not qs.exists():
            break
    return randomStr
