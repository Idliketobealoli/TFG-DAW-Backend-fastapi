<h1 align="center">🔹🔷 VgameStore 🔷🔹</h1>

<p align="center">This is the final project for the Web Application Development course at IES Laguna de Joatzel, Getafe, Madrid.</p>

---

The project consists of a ficticious game store, on which users can log in, search for games, add them to their wishlists, "buy" them, add them to their libraries and (possibly) download files.

There are other users (administrators) that can create games; adding their title, description, developer, publisher, release date, images to showcase and a file that will be the one that users download after "buying" the game.

> This is the repository for the back-end of the application. For the front-end, visit [this repository](https://github.com/darkhuo10/DAW2-TFC-Angular).

<h2 align="center">🔹 Technologies: 🔹</h2>

<div align="center">
  <a href="https://devdocs.io/python~3.12/"><img name="python" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png" height="100"></img></a>
  <a href="https://devdocs.io/fastapi/"><img name="fastapi" src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" height="100"></img></a>
  <a href="https://www.mongodb.com/docs/"><img name="mongoDB" src="https://cdn.worldvectorlogo.com/logos/mongodb-icon-2.svg" height="100"></img></a>
</div>

<h2 align="center">🔹 Endpoints: 🔹</h2>

_GROUP_  | _NAME_                 | _VERB_ | _ENDPOINT_                       | _ADDITIONAL PARAMS_                                                                               | _DESCRIPTION_
---------|------------------------|--------|----------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------
SWAGGER  | Swagger documentation  | GET    | /docs                            |                                                                                                   | Swagger documentation for the endpoints.
PRUEBA   | Prueba                 | GET    | /prueba                          |                                                                                                   | Endpoint for testing if the connection with the server works.
GAMES    | Get All                | GET    | /games                           | OPTIONAL: genre (str), language (str), name (str), publisher (str), developer (str), rating (float), visible(bool) | Finds all games. If there are any parameters, it filters by them.
GAMES    | Get By ID              | GET    | /games/{id}                      |                                                                                                   | Finds a game by the given ID, if it exists.
GAMES    | Post Game              | POST   | /games/                          | REQUIRED: dto (GameDtoCreate)                                                                     | Uploads a game to the database.
GAMES    | Update Game            | PUT    | /games/{id}                      | REQUIRED: dto (GameDtoUpdate)                                                                     | Updates the game with the given ID, if it exists.
GAMES    | Upload Main Image      | PUT    | /games/upload_main_img/{id}      | REQUIRED: file (UploadFile)                                                                       | Sets the main image for the game, if the file is an image and the game exists.
GAMES    | Upload Showcase Images | PUT    | /games/upload_showcase_imgs/{id} | REQUIRED: files (List(UploadFile))                                                                | Adds the showcase images for the given game, if there are images in the list and the game exists.
GAMES    | Clear Showcase Images  | PUT    | /games/clear_showcase_imgs/{id}  |                                                                                                   | Clears all showcase images for the given game.
GAMES    | Delete Game            | DELETE | /games/{id}                      |                                                                                                   | Deletes the game if it exists. (logical deletion)
GAMES    | Get main image         | GET    | /games/main_image/{game_id_str}  |                                                                                                   | Gets the main image of the game.
GAMES    | Get showcase image     | GET    | /games/showcase_image/{name}     |                                                                                                   | Gets the showcase image with the given name.
GAMES    | Download               | GET    | /games/download/{game_id_str}    | REQUIRED: user_id (str)                                                                           | Downloads the game file.
GAMES    | Upload                 | PUT    | /games/upload/{game_id_str}      | REQUIRED: file (UploadFile)                                                                       | Uploads the game file.
GAMES    | Get genres             | GET    | /genres                          |                                                                                                   | Gets all supported genre tags.
GAMES    | Get languages          | GET    | /languages                       |                                                                                                   | Gets all supported language tags.
LIBRARY  | Get All                | GET    | /libraries                       |                                                                                                   | Finds all libraries.
LIBRARY  | Get By ID              | GET    | /libraries/{library_id}          |                                                                                                   | Finds a library by the given user ID, if it exists.
LIBRARY  | Add Game               | PUT    | /libraries/add_game/{library_id} | REQUIRED: game_id (str)                                                                           | Adds the game with the given game_id to the library with the given ID.
REVIEW   | Get All                | GET    | /reviews                         | OPTIONAL: user_id (str), game_id (str), rating (float), publish_date (datetime)                   | Finds all reviews
REVIEW   | Get By ID              | GET    | /reviews/{id}                    |                                                                                                   | Finds a review by the given ID, if it exists.
REVIEW   | Get All From User      | GET    | /reviews/user/{user_id}          |                                                                                                   | Finds all reviews made by the user with the given ID.
REVIEW   | Get All From Game      | GET    | /reviews/user/{game_id}          |                                                                                                   | Finds all reviews made for the game with the given ID.
REVIEW   | Post Review            | POST   | /reviews                         | REQUIRED: dto (ReviewDtoCreate)                                                                   | Uploads a review to the database, and if it exists, it instead edits the review only if you are the same user that posted it or an administrator.
REVIEW   | Delete Review          | DELETE | /reviews/{id}                    |                                                                                                   | Deletes the review if it exists. (physical deletion)
USER     | Login                  | POST   | /login                           | REQUIRED: dto (UserDtoLogin)                                                                      | Login.
USER     | Register               | POST   | /register                        | REQUIRED: dto (UserDtoCreate)                                                                     | Register.
USER     | Me                     | GET    | /me                              |                                                                                                   | Gets the information of the user that called this endpoint.
USER     | Get All                | GET    | /users                           | OPTIONAL: active (bool)                                                                           | Finds all users. If the active parameter is passed, then it filters by it.
USER     | Get By ID              | GET    | /users/{id}                      |                                                                                                   | Finds a user by the given ID, if it exists.
USER     | Update User            | PUT    | /users/{id}                      | REQUIRED: dto (UserDtoUpdate)                                                                     | Updates the user with the given ID, if it exists.
USER     | Upload Profile Picture | PUT    | /users/upload_pfp/{id}           | REQUIRED: file (UploadFile)                                                                       | Updates the user profile picture for the user with the given ID, if it exists.
USER     | Get profile picture    | GET    | /users/pfp/{user_id_str}         |                                                                                                   | Gets the profile picture of the user with the given ID. Returns a 404 NOT FOUND if the user does not exist, or a default image if it does exist but has no profile picture.
USER     | Delete User            | DELETE | /user/{id}                       |                                                                                                   | Deletes the user if it exists. (logical deletion)
WISHLIST | Get All                | GET    | /wishlists                       |                                                                                                   | Finds all libraries.
WISHLIST | Get By ID              | GET    | /wishlists/{id}                  |                                                                                                   | Finds a wishlist by the given user ID, if it exists.
WISHLIST | Game exists in wishlist | GET   | /wishlists/exists/{user_id}      | REQUIRED: game_id (str)                                                                           | Returns whether a game is in the given wishlist or not.
WISHLIST | Add Game               | PUT    | /wishlists/add_game/{id}         | REQUIRED: game_id (str)                                                                           | Adds the game with the given game_id to the wishlist with the given ID.
WISHLIST | Remove Game            | PUT    | /wishlists/remove_game/{id}      | REQUIRED: game_id (str)                                                                           | Removes the game with the given game_id from the wishlist with the given ID.

<h2 align="center">🔹 Developed by: 🔹</h2>

<div align="center">
  <a href="https://github.com/Idliketobealoli"><img name="Daniel Rodriguez" src="https://avatars.githubusercontent.com/u/80858419?v=4" height="150"></a>
  <a href="https://github.com/darkhuo10"><img name="Marina Pintado" src="https://avatars.githubusercontent.com/u/105634828?v=4" height="150" ></a>
</div>















