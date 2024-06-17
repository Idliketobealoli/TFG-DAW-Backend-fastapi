import random
from bson import ObjectId
from model.review import Review
from model.user import User, Role
from model.game import Game, Language, Genre
from repositories.game_repository import GameRepository
import datetime
from repositories.review_repository import ReviewRepository
from repositories.wishlist_repository import WishlistRepository
from repositories.library_repository import LibraryRepository
from repositories.user_repository import UserRepository
import asyncio
from services.cipher_service import encode
from services.wishlist_service import WishlistService

user_repository = UserRepository()
game_repository = GameRepository()
library_repository = LibraryRepository()
wishlist_repository = WishlistRepository()
wishlist_service = WishlistService()


async def load_games():
    """
    Función encargada de generar los juegos por defecto de la aplicación.
    """
    initial_games = [
        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b1"), name="Dark Souls", developer="From Software",
             publisher="From Software",
             genres=[genre for genre in {Genre.ARPG, Genre.SOULSLIKE, Genre.SINGLEPLAYER, Genre.MULTIPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.GM}],
             description="Es Dark Souls, ¿de verdad necesitas leer la descripción de este juego?",
             release_date=datetime.datetime(2011, 9, 22), sell_number=35_000_000, price=70,
             main_image="60a7b2f7c0f2b441d4f6e9b1.png"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b2"), name="Portal", developer="Valve", publisher="Valve",
             genres=[genre for genre in {Genre.PUZZLE, Genre.PLATFORMER, Genre.SINGLEPLAYER, Genre.MULTIPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.KR, Language.FR}],
             description="Estás en un laboratorio siendo el sujeto de pruebas de una IA llamada GlaDOS, " +
                         "pero tienes una pistola de portales. Podrás escapar?",
             release_date=datetime.datetime(2007, 10, 9), sell_number=4_000_000, price=20,
             main_image="60a7b2f7c0f2b441d4f6e9b2.png", file="Portal-Valve.txt"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b3"), name="Ratchet & Clank", developer="Insomniac Games",
             publisher="Sony", genres=[genre for genre in {Genre.RPG, Genre.PUZZLE, Genre.PLATFORMER, Genre.CASUAL,
                                                           Genre.TPS, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.RU, Language.CN}],
             description="Es literalmente el juego de mi infancia. Cómpralo.",
             release_date=datetime.datetime(2002, 11, 8), sell_number=4_008_499, price=40,
             main_image="60a7b2f7c0f2b441d4f6e9b3.png"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b4"), name="Tales of Arise", developer="Bandai Namco Entertainment",
             publisher="Bandai Namco Studios",
             genres=[genre for genre in {Genre.ARPG, Genre.CASUAL, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="300 years of tyranny. A mysterious mask. Lost pain and memories. Wield the Blazing Sword "
                         "and join a mysterious, untouchable girl to fight your oppressors. Experience a tale of "
                         "liberation, featuring characters with next-gen graphical expressiveness!",
             release_date=datetime.datetime(2021, 9, 10), sell_number=30_000_000, price=39.99,
             main_image="60a7b2f7c0f2b441d4f6e9b4.jpg",
             showcase_images=["60a7b2f7c0f2b441d4f6e9b4-showcase1", "60a7b2f7c0f2b441d4f6e9b4-showcase2",
                              "60a7b2f7c0f2b441d4f6e9b4-showcase3", "60a7b2f7c0f2b441d4f6e9b4-showcase4"]),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b5"), name="Scarlet Nexus", developer="Bandai Namco Studios Inc",
             publisher="Bandai Namco Entertainment",
             genres=[genre for genre in {Genre.ARPG, Genre.CASUAL, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="Choose between Yuito and Kasane, elite psionics each armed with a talent in psychokinesis "
                         "and their own reason to fight. Complete both of their stories to unlock all the mysteries "
                         "of a Brain Punk future caught between technology and psychic abilities.",
             release_date=datetime.datetime(2021, 6, 25), sell_number=25_000_000, price=49.99,
             main_image="60a7b2f7c0f2b441d4f6e9b5.jpg"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b6"), name="Fire Emblem: Three Houses", developer="Intelligent Systems",
             publisher="Intelligent Systems",
             genres=[genre for genre in {Genre.RPG, Genre.STRATEGY, Genre.CASUAL, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="""Un RPG táctico por turnos tradicional que añade nuevos elementos de estrategia al combate. Ahora, cuando un jugador maneja una unidad, tropas de gran dimensión se moverán con él para ofrecerle apoyo durante el combate.
                         En algunas zonas, el personaje principal podrá moverse libremente, interactuar con otros personajes y reunir información.
                         El juego se ambienta en un nuevo mundo, Fódlan, donde la Iglesia de Seiros detenta gran poder sobre la tierra y sus gentes.
                         Tu protagonista se encontrará con tres personajes —Edelgard, Dimitri y Claude— que desempeñan importantes papeles en la historia.""",
             release_date=datetime.datetime(2019, 7, 26), sell_number=20_000_000, price=59.99,
             main_image="60a7b2f7c0f2b441d4f6e9b6.jpg"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b7"), name="Left 4 Dead 2", developer="Valve",
             publisher="Valve",
             genres=[genre for genre in {Genre.FPS, Genre.CASUAL, Genre.MULTIPLAYER, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="Set in the zombie apocalypse, Left 4 Dead 2 (L4D2) is the highly anticipated sequel to the "
                         "award-winning Left 4 Dead, the #1 co-op game of 2008. This co-operative action horror FPS "
                         "takes you and your friends through the cities, swamps and cemeteries of the Deep South, "
                         "from Savannah to New Orleans across five expansive campaigns.",
             release_date=datetime.datetime(2009, 11, 17), sell_number=35_000_000, price=9.75,
             main_image="60a7b2f7c0f2b441d4f6e9b7.png"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b8"), name="Tales of Xillia 2", developer="Bandai Namco Entertainment",
             publisher="Bandai Namco Studios",
             genres=[genre for genre in {Genre.ARPG, Genre.CASUAL, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="""Ha pasado un año tras los dramáticos sucesos de Tales of Xillia en los que ambos mundos, Rieze Maxia y Elympios, se unieron tras la eliminación de la barrera que los separaba. Elympios es una nación moderna con un alto nivel de progreso tecnológico logrado mediante el uso de spyrix, mientras que Rieze Maxia es una tierra que antaño vivió aislada y que se basa en las artes espirituales y la naturaleza. Aunque ambos mundos trabajan por la paz común, aún se producen numerosos choques por las diferencias culturales. Pasará algún tiempo hasta que se logre la paz real. Jude, Milla y los personajes de Rieze Maxia del primer Tales of Xillia luchan por vivir su vida y lograr la paz en este nuevo mundo unido.
                         Tales of Xillia 2 gira en torno a Ludger Kresnik, un joven y hábil chef que vive en la ciudad de Trigleph, en Elympios, con su hermano Julius y su gato Rollo. Se esfuerza mucho por seguir los pasos de su hermano y trabajar como agente en la prestigiosa corporación Spirius, una gran compañía que desarrolla tecnología para cualquier campo imaginable. Un día, por casualidad, conoce a Elle Marta, una chica que viaja sola con la idea de reunirse con su padre en la mítica “Tierra de Canaan” y a quien termina acompañando. Su decisión de ir con ella les llevará en un viaje que cambiará el destino de ambos mundos para siempre.""",
             release_date=datetime.datetime(2012, 11, 1), sell_number=45_000_000, price=24.99,
             main_image="60a7b2f7c0f2b441d4f6e9b8.jpg"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b9"), name="Tales of Xillia", developer="Bandai Namco Entertainment",
             publisher="Bandai Namco Studios",
             genres=[genre for genre in {Genre.ARPG, Genre.CASUAL, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.IT, Language.CN}],
             description="Tales of Xillia narra la historia de Jude Mathis, un inteligente estudiante de medicina que "
                         "estudia en la capital, y de Milla Maxwell, una misteriosa mujer que está acompañada por "
                         "cuatro entes invisibles. Los jugadores podrán seleccionar a Jude o a Milla a su inicio de "
                         "su aventura a través del mundo de Rieze Maxia, donde humanos y espíritus pueden vivir "
                         "juntos y en armonía. El reino de Rashugal ha estado experimentando con un poderoso "
                         "artefacto que ha estado absorbiendo el maná del mundo. Conscientes del daño que esto le "
                         "puede provocar al mundo, Milla y Jude parten en una aventura cuyo objetivo será destruir "
                         "dicho artefacto y devolverle el maná al mundo.",
             release_date=datetime.datetime(2011, 9, 8), sell_number=55_000_000, price=24.99,
             main_image="60a7b2f7c0f2b441d4f6e9b9.jpg")
    ]

    await asyncio.gather(*[game_repository.create_game(game) for game in initial_games])


async def load_users():
    """
    Función encargada de generar los usuarios por defecto de la aplicación.
    """
    initial_users = [
        User(id=ObjectId("60a7b2f7c0f2b441d4f6e9a1"), name="Marina Guanghua", surname="Pintado", username="darkhuo10",
             email="admin1@gmail.com", password=encode("admin1234"), birthdate=datetime.datetime(2003, 12, 10),
             role=Role.ADMIN, profile_picture="darkhuo10.png"),

        User(id=ObjectId("60a7b2f7c0f2b441d4f6e9a2"), name="Daniel", surname="Rodríguez", username="Idliketobealoli",
             email="admin2@gmail.com", password=encode("loli1707"), birthdate=datetime.datetime(2002, 5, 26),
             role=Role.ADMIN, profile_picture="Idliketobealoli.png"),

        User(id=ObjectId("60a7b2f7c0f2b441d4f6e9a3"), name="User 1", surname="Apellido", username="usuario1",
             email="user1@gmail.com", password=encode("password1"), birthdate=datetime.datetime(2002, 5, 26),
             profile_picture="asdf.png"),

        User(id=ObjectId("60a7b2f7c0f2b441d4f6e9a4"), name="User 2", surname="Apellido 2", username="usuario2",
             email="user2@gmail.com", password=encode("password2"), birthdate=datetime.datetime(2002, 5, 26)),

        User(id=ObjectId("60a7b2f7c0f2b441d4f6e9a5"), name="User 3", surname="Apellido 3", username="usuario3",
             email="user4@gmail.com", password=encode("password4"), birthdate=datetime.datetime(2002, 5, 26))
    ]

    # Los usuarios con sus libraries y wishlists se crean a la vez (en hilos distintos), pero dentro de la creación
    # de cada usuario, primero se crea el usuario, luego la wishlist y luego la library, para evitar problemas.
    await asyncio.gather(*[create_user_with_library_and_wishlist(user) for user in initial_users])


async def create_user_with_library_and_wishlist(user):
    """
    Función encargada de insertar en la base de datos el usuario pasado por parámetro,
    y además crear su librería y lista de deseados.
    """
    await user_repository.create_user(user)
    await wishlist_repository.create_wishlist(user.id)
    await library_repository.create_library(user.id)


async def load_reviews():
    """
    Función encargada de generar las reviews por defecto de la aplicación.
    """
    initial_reviews = [
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b9"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a2"), rating=4,
               description="Juegazo. La historia es sublime y el combate también. Buena rejugabilidad debido a que "
                           "hay dos protagonistas y su historia, pese a que en muchas partes es común, "
                           "cambia en algunos momentos."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b9"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a3"), rating=5,
               description="Muy buen juego, me ha gustado mucho (para nada soy la misma persona que el de la review "
                           "que empieza por 'Juegazo.' desde otra cuenta, que va.)"),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b8"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a4"), rating=3.9,
               description="La segunda entrega de Xillia incluye muchas mejoras en el sistema de combate y una "
                           "historia tan disfrutable como el primer título. Sin embargo, esta vez no podemos optar "
                           "entre varios protagonistas, lo que hace que pierda algo de rejugabilidad."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b7"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a5"), rating=5,
               description="Pegas tiros a zombies, es frenético y está hecho por Valve; ¿hace falta decir más? "
                           "Cómpralo, tremenda joyita."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b7"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a2"), rating=4.9,
               description="Pium pium. Mucho weapon, mucho damage. Con amigos la experiencia es 10/10."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b6"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a3"), rating=5,
               description="Estrategia, buena historia, buenos personajes y waifus. ¿Qué más quieres?"),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b6"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a4"), rating=3.5,
               description="El juego está muy bien, pero le pongo 3.5 estrellas porque no sabía que era de estrategia "
                           "y no me gustan los juegos de estrategia. (No se leer los tags)"),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b5"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a5"), rating=3.7,
               description="Múltiples protagonistas con sus propias historias, gameplay divertido, y destrucción de "
                           "cosas. Está bien."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b4"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a2"), rating=4.8,
               description="Otra maravilla de juego de los creadores de Tales of Xillia 1 y 2. Notoria mejora gráfica "
                           "y de gameplay."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b3"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a3"), rating=4.3,
               description="Clasicazo de la PS2. Plataformas y disparos, nada puede salir mal."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b2"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a4"), rating=3.1,
               description="Puzles y portales. Lo único malo es que es cortísimo."),
        Review(id=ObjectId(), game_id=ObjectId("60a7b2f7c0f2b441d4f6e9b1"),
               user_id=ObjectId("60a7b2f7c0f2b441d4f6e9a2"), rating=4.8,
               description="Plin plin plon. Plin plon plin, plin plon. Plon. Plin plin plon. Plin plon plin, "
                           "plin plon. Plon. Plon plin, plin plin plin plin. Plin plin plon."),
    ]

    review_repository = ReviewRepository()
    await asyncio.gather(*[review_repository.create_review(review) for review in initial_reviews])


async def load_wishlists():
    """
    Función encargada de cargar un número aleatorio de juegos (aleatorios) en la lista de deseados de cada usuario.
    """
    users = await user_repository.get_users()
    games = await game_repository.get_games()

    # Queremos añadir un numero aleatorio de juegos a la wishlist de cada usuario,
    # y que dichos juegos sean aleatorios.
    for user in users:

        # Por cada usuario, cambiamos el orden de la lista de juegos
        random.shuffle(games)

        # Después, iteramos entre 0 y N veces, donde N es el último índice de la lista.
        # Así, puede que haya usuarios sin juegos en la wishlist, y otros con X juegos.
        for i in range(random.randint(0, len(games) - 1)):
            await wishlist_service.add_to_wishlist(user.id, games[i].id)
