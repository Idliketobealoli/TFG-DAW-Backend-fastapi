# VGameShop
This is the final project for the Web Application Development course at IES Laguna de Joatzel, Getafe, Madrid.

Developed by:
- [Daniel Rodríguez Muñoz](https://github.com/Idliketobealoli)
- [Marina Guanghua Pintado Guerrero](https://github.com/darkhuo10)

---

The project consists of a ficticious game store, on which users can log in, search for games, add them to their wishlists, "buy" them, add them to their libraries and (possibly) download files.

There are other users (administrators) that can create games; adding their title, description, developer, publisher, release date, images to showcase and a file that will be the one that users download after "buying" the game.

---

This is the repository for the back-end of the application. For the front-end, visit [this repository](https://github.com/darkhuo10/DAW2-TFC-Angular).

---

## Technologies:

<div align="center">
  <img name="python" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png" height="100"></img>
  <img name="fastapi" src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" height="100"></img>
  <img name="mongoDB" src="https://cdn.worldvectorlogo.com/logos/mongodb-icon-2.svg" height="100"></img>
</div>

---

## Endpoints:

_GROUP_  | _NAME_                 | _VERB_ | _ENDPOINT_                       | _ADDITIONAL PARAMS_                                                                               | _DESCRIPTION_
---------|------------------------|--------|----------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------
PRUEBA   | Prueba                 | GET    | /prueba                          |                                                                                                   | Endpoint for testing if the connection with the server works.
GAMES    | Get All                | GET    | /games                           | OPTIONAL: genre (str), language (str), name (str), publisher (str), developer (str), rating (str) | Finds all games. If there are any parameters, it filters by them.
GAMES    | Get By ID              | GET    | /games/{id}                      |                                                                                                   | Finds a game by the given ID, if it exists.
GAMES    | Post Game              | POST   | /games                           | REQUIRED: dto (GameDtoCreate)                                                                     | Uploads a game to the database.
GAMES    | Update Game            | PUT    | /games/{id}                      | REQUIRED: dto (GameDtoUpdate)                                                                     | Updates the game with the given ID, if it exists.
GAMES    | Upload Main Image      | PUT    | /games/upload_main_img/{id}      | REQUIRED: file (UploadFile)                                                                       | Sets the main image for the game, if the file is an image and the game exists.
GAMES    | Upload Showcase Images | PUT    | /games/upload_showcase_imgs/{id} | REQUIRED: files (List(UploadFile))                                                                | Adds the showcase images for the given game, if there are images in the list and the game exists.
GAMES    | Clear Showcase Images  | PUT    | /games/clear_showcase_imgs/{id}  |                                                                                                   | Clears all showcase images for the given game.
GAMES    | Delete Game            | DELETE | /games/{id}                      |                                                                                                   | Deletes the game if it exists. (CAMBIAR ESTO A UN BORRADO LÓGICO, NO TIENE SENTIDO QUE SE BORRE DEL TODO)
LIBRARY  | Get All                | GET    | /libraries                       |                                                                                                   | Finds all libraries.
LIBRARY  | Get By ID              | GET    | /libraries/{id}                  |                                                                                                   | Finds a library by the given ID, if it exists. (ELIMINAR ESTO, TIENE MAS SENTIDO QUE EL ID DE LA LIBRERIA SEA EL MISMO QUE EL DEL USUARIO ASOCIADO. LO MISMO PARA WISHLIST)
LIBRARY  | Get By User ID         | GET    | /libraries/user/{id}             |                                                                                                   | Finds a library by their associated user's ID, if it exists.
LIBRARY  | Post Library           | POST   | /libraries                       | REQUIRED: dto (LibraryDtoCreate)                                                                  | Uploads a library to the database. (ELIMINAR ESTE ENDPOINT Y MODIFICAR EL POST DE USUARIO PARA QUE SE CREE LA LIBRERÍA DE ESTE AUTOMÁTICAMENTE. LO MISMO PARA LA WISHLIST)
LIBRARY  | Add Game               | PUT    | /libraries/add_game/{id}         | REQUIRED: game_id (str)                                                                           | Adds the game with the given game_id to the library with the given ID.
LIBRARY  | Delete Library         | DELETE | /libraries/{id}                  |                                                                                                   | Deletes the library associated with the given ID. (CAMBIAR ESTO A UN BORRADO LÓGICO, LO MISMO PARA USUARIO Y WISHLIST)
REVIEW   | Get All                | GET    | /reviews                         | OPTIONAL: user_id (str), game_id (str), rating (float), publish_date (datetime)                   | Finds all reviews
REVIEW   | Get By ID              | GET    | /reviews/{id}                    |                                                                                                   | Finds a review by the given ID, if it exists.
REVIEW   | Get All From User      | GET    | /reviews/user/{user_id}          |                                                                                                   | Finds all reviews made by the user with the given ID.
REVIEW   | Get All From Game      | GET    | /reviews/user/{game_id}          |                                                                                                   | Finds all reviews made for the game with the given ID.
REVIEW   | Post Review            | POST   | /reviews                         | REQUIRED: dto (ReviewDtoCreate)                                                                   | Uploads a review to the database.
REVIEW   | Update Review          | PUT    | /reviews/{id}                    | REQUIRED: dto (ReviewDtoUpdate)                                                                   | Updates the review with the given ID, if it exists.
REVIEW   | Delete Review          | DELETE | /reviews/{id}                    |                                                                                                   | Deletes the review if it exists.
USER     | Login                  | POST   | /login                           | REQUIRED: dto (UserDtoLogin)                                                                      | Login.
USER     | Register               | POST   | /register                        | REQUIRED: dto (UserDtoRegister)                                                                   | Register.
USER     | Me                     | GET    | /me                              |                                                                                                   | Gets the information of the user that called this endpoint.
USER     | Get All                | GET    | /users                           | OPTIONAL: active (bool)                                                                           | Finds all users. If the active parameter is passed, then it filters by it.
USER     | Get By ID              | GET    | /users/{id}                      |                                                                                                   | Finds a user by the given ID, if it exists.
USER     | Post User              | POST   | /users                           | REQUIRED: dto (UserDtoCreate)                                                                     | Uploads a user to the database.
USER     | Update User            | PUT    | /users/{id}                      | REQUIRED: dto (UserDtoUpdate)                                                                     | Updates the user with the given ID, if it exists.
USER     | Upload Profile Picture | PUT    | /users/upload_pfp/{id}           | REQUIRED: file (UploadFile)                                                                       | Updates the user profile picture for the user with the given ID, if it exists.
USER     | Delete User            | DELETE | /user/{id}                       |                                                                                                   | Deletes the user if it exists. (CAMBIAR ESTO A UN BORRADO LÓGICO, NO TIENE SENTIDO QUE SE BORRE DEL TODO)
WISHLIST | Get All                | GET    | /wishlists                       |                                                                                                   | Finds all libraries.
WISHLIST | Get By ID              | GET    | /wishlists/{id}                  |                                                                                                   | Finds a wishlist by the given ID, if it exists. (ELIMINAR ESTO, TIENE MAS SENTIDO QUE EL ID DE LA WISHLIST SEA EL MISMO QUE EL DEL USUARIO ASOCIADO. LO MISMO PARA LIBRARY)
WISHLIST | Get By User ID         | GET    | /wishlists/user/{id}             |                                                                                                   | Finds a wishlist by their associated user's ID, if it exists.
WISHLIST | Post Wishlist          | POST   | /wishlists                       | REQUIRED: dto (WishlistDtoCreate)                                                                 | Uploads a wishlist to the database. (ELIMINAR ESTE ENDPOINT Y MODIFICAR EL POST DE USUARIO PARA QUE SE CREE LA LIBRERÍA DE ESTE AUTOMÁTICAMENTE. LO MISMO PARA LA WISHLIST)
WISHLIST | Add Game               | PUT    | /wishlists/add_game/{id}         | REQUIRED: game_id (str)                                                                           | Adds the game with the given game_id to the wishlist with the given ID.
WISHLIST | Remove Game            | PUT    | /wishlists/remove_game/{id}      | REQUIRED: game_id (str)                                                                           | Adds the game with the given game_id to the wishlist with the given ID.
WISHLIST | Delete Library         | DELETE | /wishlists/{id}                  |                                                                                                   | Deletes the wishlist associated with the given ID. (CAMBIAR ESTO A UN BORRADO LÓGICO, LO MISMO PARA USUARIO Y LIBRARY)

---

















