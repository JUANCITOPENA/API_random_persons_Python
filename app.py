from flask import Flask, jsonify
import random
import faker
import pytz

app = Flask(__name__)

# Crear un generador de datos aleatorios
fake = faker.Faker()

# Lista de zonas horarias
timezones = pytz.all_timezones

# Función para generar un objeto de persona aleatoria con imágenes
def generate_random_person():
    gender = random.choice(["male", "female"])
    first_name = fake.first_name()
    last_name = fake.last_name()
    street_number = fake.building_number()
    street_name = fake.street_name()
    city = fake.city()
    state = fake.state()
    country = fake.country()
    postcode = fake.zipcode()
    latitude = fake.latitude()
    longitude = fake.longitude()
    
    # Generar una zona horaria aleatoria
    timezone = random.choice(timezones)

    # Manejar el caso en el que no se puede obtener un desplazamiento válido
    try:
        utcoffset = pytz.timezone(timezone).utcoffset(None)
        offset_hours = utcoffset.total_seconds() / 3600.0
    except Exception as e:
        # Si hay un error, establece el desplazamiento en None
        utcoffset = None
        offset_hours = None

    email = fake.email()
    username = fake.user_name()
    password = fake.password()
    salt = fake.sha256()
    md5 = fake.md5()
    sha1 = fake.sha1()
    sha256 = fake.sha256()
    dob_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    dob_age = fake.random_int(min=18, max=80)
    registered_date = fake.date_this_century(before_today=True, after_today=False)
    registered_age = fake.random_int(min=1, max=10)
    phone = fake.phone_number()
    cell = fake.phone_number()
    nat = fake.country_code(representation="alpha-2")

    # Generar URLs de imágenes aleatorias
    picture_large = f"https://randomuser.me/api/portraits/men/{random.randint(1, 99)}.jpg"
    picture_medium = f"https://randomuser.me/api/portraits/med/men/{random.randint(1, 99)}.jpg"
    picture_thumbnail = f"https://randomuser.me/api/portraits/thumb/men/{random.randint(1, 99)}.jpg"

    person = {
        "gender": gender,
        "name": {
            "title": fake.prefix(),
            "first": first_name,
            "last": last_name
        },
        "location": {
            "street": {
                "number": street_number,
                "name": street_name
            },
            "city": city,
            "state": state,
            "country": country,
            "postcode": postcode,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": {
                "offset": offset_hours,
                "description": timezone
            }
        },
        "email": email,
        "login": {
            "uuid": fake.uuid4(),
            "username": username,
            "password": password,
            "salt": salt,
            "md5": md5,
            "sha1": sha1,
            "sha256": sha256
        },
        "dob": {
            "date": dob_date.isoformat(),
            "age": dob_age
        },
        "registered": {
            "date": registered_date.isoformat(),
            "age": registered_age
        },
        "phone": phone,
        "cell": cell,
        "id": {
            "name": fake.random_element(elements=["CPR", "NINO", "HETU", "TFN", "SVNR", "SIN", "FN"]),
            "value": fake.random_element(elements=[fake.random_number(digits=10), None])
        },
        "picture": {
            "large": picture_large,
            "medium": picture_medium,
            "thumbnail": picture_thumbnail
        },
        "nat": nat
    }

    return person

# Ruta para obtener datos aleatorios de personas
@app.route('/api/random_persons', methods=['GET'])
def get_random_persons():
    results = [generate_random_person() for _ in range(50)]
    response = {
        "results": results,
        "info": {
            "seed": fake.random_int(min=1000, max=9999),
            "results": 50,
            "page": 1,
            "version": "1.4"
        }
    }
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
