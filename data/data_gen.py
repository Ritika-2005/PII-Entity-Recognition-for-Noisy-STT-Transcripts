import json
import random
import uuid
import os

random.seed(42)

DIGIT_WORDS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]

DAY_WORDS = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty", "twenty one", "twenty two", "twenty three",
    "twenty four", "twenty five", "twenty six", "twenty seven", "twenty eight",
    "twenty nine", "thirty", "thirty one",
]

YEAR_SPOKEN = [
    "two thousand eighteen",
    "two thousand nineteen",
    "two thousand twenty",
    "two thousand twenty one",
    "two thousand twenty two",
    "two thousand twenty three",
    "twenty eighteen",
    "twenty nineteen",
    "twenty twenty",
    "twenty twenty one",
    "twenty twenty two",
]

CITY_TO_LOCATIONS = {
    "new york": ["central park", "times square", "queens street"],
    "san francisco": ["golden gate bridge", "harbor point"],
    "mumbai": ["marine drive", "gateway of india"],
    "bangalore": ["mg road", "brigade road"],
    "delhi": ["india gate", "main market"],
    "hyderabad": ["charminar circle"],
    "kolkata": ["victoria memorial"],
    "dubai": ["bayfront avenue"],
    "singapore": ["orchard street"],
    "london": ["riverfront park", "old town square"],
    "boston": ["downtown plaza"],
    "los angeles": ["sunset boulevard", "city mall"],
}

NAMES = [
    "john doe", "alex roy", "mira patel", "rahul kumar", "ravi singh",
    "sarah khan", "linda brown", "george mathew", "suresh nair",
    "anita sharma", "virat desai", "emma watson", "li wei",
    "sofia gomez", "david miller", "aarav mehta", "priya rao",
    "daniel scott", "haruto tanaka", "fatima zahra", "noah cooper",
    "isabella rossi", "arjun reddy", "kabir verma", "meera joshi",
    "olivia clark", "henry adams", "lucas baker", "nina fernandes",
]

CITIES = list(CITY_TO_LOCATIONS.keys())


def digits_to_words(digit_str: str) -> str:
    return " ".join(DIGIT_WORDS[d] for d in digit_str)


def gen_phone_numeric() -> str:
    first = random.choice("123456789")
    rest = "".join(random.choice("0123456789") for _ in range(9))
    phone = first + rest

    r = random.random()
    if r < 0.4:
        return " ".join(phone)
    else:
        return phone


def gen_phone_spoken() -> str:
    digits = [random.choice("0123456789") for _ in range(10)]
    return digits_to_words("".join(digits))


def gen_phone() -> str:
    if random.random() < 0.7:
        return gen_phone_numeric()
    else:
        return gen_phone_spoken()


def gen_credit_card() -> str:
    # 16-digit number
    cc = "".join(random.choice("0123456789") for _ in range(16))
    r = random.random()
    if r < 0.5:
        return cc
    elif r < 0.8:
        return " ".join(cc[i:i+4] for i in range(0, 16, 4))
    else:
        return cc[:8] + " " + cc[8:]


def gen_date_spoken() -> str:
    day = random.choice(DAY_WORDS)
    month = random.choice(MONTHS)
    year = random.choice(YEAR_SPOKEN)

    pattern = random.choice([
        "{month} {day} {year}",
        "{day} {month} {year}",
        "{month} {year}",
        "{day} {month}",
    ])
    return pattern.format(day=day, month=month, year=year)


def gen_date_semi_numeric() -> str:
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = random.randint(2018, 2024)
    pattern = random.choice([
        "{m} {d} {y}",
        "{m:02d} {d:02d} {y}",
        "{d} {m} {y}",
    ])
    return pattern.format(d=day, m=month, y=year)


def gen_date_numeric() -> str:
    year = random.randint(2018, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    pattern = random.choice([
        "{y} {m:02d} {d:02d}",
        "{y}-{m:02d}-{d:02d}",
        "{y} {m} {d}",
    ])
    return pattern.format(y=year, m=month, d=day)


def gen_date() -> str:
    r = random.random()
    if r < 0.5:
        return gen_date_spoken()
    elif r < 0.8:
        return gen_date_semi_numeric()
    else:
        return gen_date_numeric()


def gen_email(first_name: str, last_name: str) -> str:
    providers = ["gmail", "yahoo", "outlook", "g mail", "icloud", "mail"]
    provider = random.choice(providers)

    patterns = [
        "{first} at {provider} dot com",
        "{first} dot {last} at {provider} dot com",
        "{first} underscore {last} at {provider} dot com",
        "{first} {last} at {provider} dot com",
        "{first} plus one at {provider} dot com",
    ]
    pattern = random.choice(patterns)
    return pattern.format(first=first_name, last=last_name, provider=provider)


def maybe_noisy_name(name: str) -> str:
    if random.random() < 0.15:
        parts = name.split()
        if len(parts) == 2 and len(parts[1]) > 2:
            # eg "john doe" to "john do"
            parts[1] = parts[1][:-1]
            return " ".join(parts)
    return name



SINGLE_PI_TEMPLATES = [
    # phone
    "my phone number is {phone}",
    "can you please call me on {phone}",
    "contact me on {phone}",
    "reach me on {phone} later today",

    # email
    "send it to {email}",
    "email me at {email}",
    "you can also write to {email}",

    # credit-card
    "my credit card number is {cc}",
    "the payment was done using card {cc}",

    # name
    "the booking is under {name}",
    "register it under the name {name}",
    "the reservation is in the name {name}",

    # city
    "i am staying in {city}",
    "i currently live in {city}",
    "we moved to {city} last year",

    # location
    "deliver it to {location}",
    "the meeting point is {location}",
    "please come to {location}",

    # date
    "schedule on {date}",
    "set the reminder for {date}",
    "let us meet on {date}",
]

MULTI_PII_TEMPLATES = [
    "contact {name} on {phone}",
    "you can mail {name} at {email}",
    "pick up {name} from {location} on {date}",
    "send the invoice to {email} before {date}",
    "book a table in {city} at {location} on {date}",
    "please call {name} on {phone} and confirm the date {date}",
    "ship it to {name} at {location} in {city}",
    "use the card {cc} and send receipt to {email}",
    "for {name} in {city} call on {phone}",
    "the meeting with {name} is in {city} on {date}",
    "save my contact as {name} and phone as {phone}",
    "for the reservation under {name} use card {cc} on {date}",
]

# multi-PII
LONG_TEMPLATES = [
    "hey so basically i need you to book the appointment for {name} in {city} on {date} and also make sure you call on {phone} once it is confirmed",
    "can you please send all the documents to {email} and if there is any issue just reach out to {name} on {phone} sometime tomorrow or on {date}",
    "we are meeting at {location} in {city} on {date} so please remind {name} by calling on {phone} a few hours before",
    "use the card {cc} for the payment today and then share the confirmation mail with {name} on {email} before {date}",
]

NEGATIVE_TEMPLATES = [
    "i will let you know later about the details",
    "can you send me the update tomorrow morning",
    "lets plan the trip sometime next month",
    "i am not sure about the exact time right now",
    "we can discuss all of this in the meeting",
    "that is all i wanted to say for now",
    "i think the schedule has already been shared with you",
]


# Example generation

def gen_example():
    # choose city + location combo
    city = random.choice(CITIES)
    location = random.choice(CITY_TO_LOCATIONS[city])

    full_name = random.choice(NAMES)
    first_name, last_name = full_name.split()[0], full_name.split()[-1]
    name_used = maybe_noisy_name(full_name)

    phone = gen_phone()
    email = gen_email(first_name, last_name)
    cc = gen_credit_card()
    date = gen_date()

    data = {
        "phone": phone,
        "email": email,
        "cc": cc,
        "name": name_used,
        "city": city,
        "location": location,
        "date": date,
    }

    r = random.random()
    # ~15% negative (no PII)
    if r < 0.15:
        template = random.choice(NEGATIVE_TEMPLATES)
        text = template  
        entities = []

    # ~10% long, multi-PII
    elif r < 0.25:
        template = random.choice(LONG_TEMPLATES)
        text = template.format(**data)
        entities = []

    # ~35% regular multi-PII
    elif r < 0.60:
        template = random.choice(MULTI_PII_TEMPLATES)
        text = template.format(**data)
        entities = []

    # remaining ~40% single-PII
    else:
        template = random.choice(SINGLE_PI_TEMPLATES)
        text = template.format(**data)
        entities = []

    # all texts should be lowercase
    text = text.lower()

    label_value_pairs = [
        ("PHONE", phone),
        ("EMAIL", email),
        ("CREDIT_CARD", cc),
        ("PERSON_NAME", name_used),
        ("CITY", city),
        ("LOCATION", location),
        ("DATE", date),
    ]

    for label, value in label_value_pairs:
        value = value.lower()
        start = text.find(value)
        if start != -1:
            entities.append(
                {
                    "start": start,
                    "end": start + len(value),
                    "label": label,
                }
            )

    example = {
        "id": f"utt_{uuid.uuid4().hex[:8]}",
        "text": text,
        "entities": entities,
    }
    return example


def write_jsonl(path, n):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(n):
            ex = gen_example()
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    write_jsonl("data/train.jsonl", 1000)
    write_jsonl("data/dev.jsonl", 200)
    print("wrote data/train.jsonl (1000) and data/dev.jsonl (200)")
