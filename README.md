# Tibber Robot Cleaner

## About

This project was created as part of the code assessment from `Tibber.de` to implement the [application requirements](docs%2Frequirements.md) .


## API definition

- `POST /tibber-developer-test/enter-path`:
    - Request:
      - body: `MoveCommandRequest`
    - Response
        - code: 201 | 422
        - body: `MoveCommandResponse`

### API schema

```python
@dataclass(frozen=True)
class StartPoint:
    x: int = Field(ge=-100_000, le=100_000)
    y: int = Field(ge=-100_000, le=100_000)


@dataclass(frozen=True)
class MoveCommand:
    direction: Direction
    steps: int = Field(gt=0, lt=100_000)


@dataclass(frozen=True)
class MoveCommandRequest:
    start: StartPoint
    commands: List[MoveCommand] = Field(max_length=10_000)

    
@dataclass
class MoveCommandResponse:
    id: int
    commands: int
    result: int
    duration: float
    timestamp: datetime
```

## Running the application

The application can be run from docker, executing the command from the project's root:

```shell
docker-compose up --build -d api
```

## Testing

To run the tests, execute:

```shell
docker-compose build test
docker-compose run --rm test
```

## Tech details

The chosen tech stack to implement was the following :

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- Postgres databases


### Code Architecture

The code is organized based on the [Hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)):

- `adapters` are the implementation for the external dependencies of the application (i.e.  REST API, Database)
- `app` contains the models and business logic for the application. The communication with external dependencies are done through the defined `ports` (interfaces).

### Architecture Diagram

![tibber architecture design.jpg](docs%2Ftibber%20architecture%20design.jpg)

### Notes on large datasets

The application run successfully with a large dataset under Docker. The specs of the testing machine:

- Processor: (R) Core(TM) i9-10980HK CPU@2.40GHz
- RAM: 32GB
- OS: Windows 11 Home
- Docker desktop running under WSL2

Using this configuration, the return time of the request was in the range of `30s` and `70s`.

If you receive a memory allocation error when running with docker under macOS or Linux, try to change the kernel's `overcommit_memory` configuration executing one of the commands:


```shell
sudo sysctl vm.overcommit_memory=1
```

or

```shell
echo 1 | sudo tee /proc/sys/vm/overcommit_memory
```
