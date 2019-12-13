# LyricService
[![CircleCI](https://circleci.com/gh/AwesomeMusicManager/LyricService.svg?style=svg)](https://circleci.com/gh/AwesomeMusicManager/LyricService)

# Deployment

Serviço está de pé usando o Heroku neste [endereço](https://lyric-service-app.herokuapp.com)

# Endpoints

## GET /
Endpoint para Health Check.

## GET /docs
Contém json do Swagger.

## GET /api/v1/lyric

API que retorna a letra da música.
Contém dois possíveis parâmetros:
- song -> parâmetro obrigatório, nome da música da qual a letra será buscada
- artist -> parâmetro opcional.
Caso o parâmetro `artist` não seja passado, será feita uma requisição no [SongService](https://github.com/AwesomeMusicManager/SongService) para encontrá-lo.
