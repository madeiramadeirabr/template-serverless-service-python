# template-serverless-service-python
Template para construção de API flexível com serviços ECS AWS.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=madeiramadeirabr_template-serverless-service-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=madeiramadeirabr_template-serverless-service-python)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=madeiramadeirabr_template-serverless-service-python&metric=coverage)](https://sonarcloud.io/summary/new_code?id=madeiramadeirabr_template-serverless-service-python)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=madeiramadeirabr_template-serverless-service-python&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=madeiramadeirabr_template-serverless-service-python)

## Arquitetura de serviços
Diagramas aplicados com o uso desta arquitetura

Mais detalhes [aqui](https://drive.google.com/file/d/112om-id0zfd8qGd0Q4kTaoIwIgwx6DGJ/view?usp=sharing).

### Arquitetura em nuvem
Exemplo da arquitetura que roda no AWS Cloud.

![Service-Arch](docs/ecs-service-arch.png)

### Arquitetura de Docker
Exemplo da arquitetura que funciona com o docker.
![Docker-Service-Arch](docs/ecs-docker-service-arch.png)

## Arquitetura Geral de Rotas de Serviço
Exemplo de documentação OpenApi.
![Swagger](docs/swagger.png)

Lista de rotas:
```
GET / - Root
GET /docs - Swagger docs
GET /alive - Health Check
GET /v1/product - Product List
POST /v1/product - Product Create
DELETE /v1/product/<uuid> - Soft Product Delete
GET /v1/product/<uuid> - Product Get
PATCH /v1/product/<uuid> - Soft Product Update
PUT /v1/product/<uuid> - Complete Product Update
```

# Pré requisitos
- Python >=3.6
- docker
- docker-compose
- python-dotenv
- jsonformatter
- requests
- pytz
- redis
- pyyaml
- apispec
- marshmallow
- Flask

## Componentes
- Docker-compose
- Localstack
- OpenApi
- SQS Integration
- Flask
- MySQL
- Redis
- Swagger
- Restful
- HATEOS

## Detalhes sobre os arquivos de requirements
### requirements.txt
Coleção de módulos de aplicação comum, módulos leves.

### requirements-local.txt
Coleção de módulos de desenvolvimento específicos.

### requirements-tests.txt
Coleção de módulos de aplicação de testes específicos.

### requirements-vendor.txt
Coleção de módulos de aplicação específicos, módulos pesados que podem ser convertidos em níveis, se necessário.

## Configuração Kong
Configure o Kong API Gateway para trabalhar compatívelmente com o API Gateway.


## Instalação
### Instalando AWS CLI
Documentação:
https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-cliv2.html

Execute o seguinte comando:
```bash
apt install python38-env
apt install awscli
apt install zip
app install pip
```
Execute o seguinte comando:
```bash
aws configure
```

### Instalando o suporte python venv
Execute o seguinte comando:
```bash
apt install python38-env
```

### Executando Localmente
Para criar o `venv` e instalar os modulos, execute:
```bash
./scripts/venv.sh
```
#### Executando o app
Execute o seguinte comando:
```bash
./scripts/flask/run-local.sh
```
### Executando via docker
To execute the build:
```bash
./scripts/runenv.sh --build
```

Execute o seguinte comando:
```bash
./scripts/runenv.sh
```

### Recuperando o ambiente em casos de erro
Execute o seguinte comando:
```bash
./scripts/fixenv.sh
```

## Informações sobre scripts de automação
A seguir descrevemos o uso dos scripts de automação.
Estes scripts kebab case ajudam o desenvolvedor nas tarefas em geral.

### Scripts gerais
Kebab case script para ajudar o desenvolvedor em tarefas gerais.

| Script                      | Descrição                                                                      | Context           |
|-----------------------------|-----------------------------------------------------------------------------------|-------------------|
| autopep8.sh                 | Execute the code-lint for pep8                                                    | Codelint          |
| boot.sh                     | Boot the application during de container execution                                | Local boot        |
| boot-db.sh                  | Boot the data for the database                                                    | Local boot        |
| boot-queues.sh              | Boot the queues of the application in the localstack                              | Local boot        |
| boot-validate-connection.sh | Check if localstack is ready to connect                                           | Local boot        |
| clean-env.sh                | Clean the ./vendor folder                                                         | Local install     |
 | commit.sh                   | Execute the commitizen tool for commit message                                    | Local development |
| fixenv.sh                   | In some cases where the network are deleted, you can fix the container references | Local install     |
| install.sh                  | Script to install the dependencies                                                | Local install     |
| install-local.sh            | Script to install the dependencies in the ./vendor folder                         | Local install     |
| openapi.sh                  | Script to generate the openapi.yaml                                               | CI/CD pipeline    |
| pre-commit-config.sh.sh     | Script to prepare the local enviroment to execute pre-commit tools                | Local development |
| preenv.sh                   | Script to execute the pre build commands                                          | Local boot        |
| pylint.sh                   | Script to execute the pylint analysis                                             | Local development |
| runenv.sh                   | Script to start the project locally                                               | Local development |
| testenv.sh                  | Script to run the environment with focus in the component tests                   | Local development |
| venv.sh                     | Script to install the dependencies in the venv folder                             | Local install     |
| venv-exec.sh                | Script to execute scripts to install content inside the venv                      | Local install     |
| zip.sh                      | Generate a zip file with the application content                                  | Other             |

### Docker scripts
Helper scripts to do tasks for docker context;
### Flask scripts
Helper scripts to run flask locally, not inside a docker container;
### Localstack scripts
Helper scripts to run commands over Localstack resources like S3, SQS, Lambda, etc;
### Migrations scripts
Helper scripts to execute migrations;
### OpenApi scripts
Helper scripts to generate openapi schemas and specifications;
### Tests scripts
Helper scripts to execute tests and generate reports;
## Samples
See the project samples in this folder [here](samples).

## Running tests
To run the unit tests of the project you can execute the follow command:

First you need install the tests requirements:
 ```bash
 ./scripts/venv-exec.sh ./scripts/tests/install-tests.sh
 ```


### Unit tests:
Executing the tests:
 ```bash
./scripts/venv-exec.sh ./scripts/tests/unit-tests.sh
 ```
Executing a specific file:
 ```bash
./scripts/venv-exec.sh ./scripts/tests/unit-tests.sh /tests/unit/test_app.py
 ```
### Components tests:
Start the docker containers:
 ```bash
./scripts/testenv.sh
```

Executing the tests:
 ```bash
./scripts/venv-exec.sh ./scripts/tests/component-tests.sh
```
Executing a specific file:
 ```bash
./scripts/venv-exec.sh ./scripts/tests/component-tests.sh /tests/component/test_app.py
 ```
### Integration tests:
Copy the file `env/integration.env.example` to
`env/integration.env` and edit it with de staging parameters.

Executing the tests:
 ```bash
./scripts/venv-exec.sh ./scripts/tests/integration-tests.sh
```
Executing a specific file:
```bash
./scripts/venv-exec.sh ./scripts/tests/integration-tests.sh /tests/integration/test_app.py
```

### All tests:
Executing the tests:
```bash
 ./scripts/venv-exec.sh ./scripts/tests/tests.sh
 ```

## Generating coverage reports
To execute coverage tests you can execute the follow commands:

### Unit test coverage:
Execute o seguinte comando:
```bash
./scripts/venv-exec.sh ./scripts/tests/unit-coverage.sh
```

### Component test coverage:
Start the docker containers:
```bash
./scripts/testenv.sh
```

Execute the follow command:
```bash
./scripts/venv-exec.sh ./scripts/tests/component-coverage.sh
```

### Integration test coverage:

Copy the file `env/integration.env.example` to
`env/integration.env` and edit it with de staging parameters.

Execute the follow command:
```bash
./scripts/venv-exec.sh ./scripts/tests/integration-coverage.sh
```
> Observation:

The result can be found in the folder `target/*`.


## License
See the license: [LICENSE.md](LICENSE.md).

## Contributions
* Anderson de Oliveira Contreira [andersoncontreira](https://github.com/andersoncontreira)

## IDE configuration
* For docstring syntax please use the `reStructuredText`
* For line limit use 100 chars as defined by PEP8

## Pylint
To execute the pylint in the sourcecode of the project, execute the follow command:
```bash
./scripts/pylint.sh
```
Or:

```bash
./scripts/pylint.sh ./app.py
```

## AutoPEP8
To execute the autopep8 in the sourcecode of the project, execute the follow command:
```bash
./scripts/autopep8.sh
```
Or:

```bash
./scripts/autopep8.sh ./app.py
```

## Pre-commit
To install the pre-commit for you local development environment execute:
```bash
./scripts/venv.sh
```
> the details of the lib are present in the requirements-local.txt

After you can run:

```bash
./scripts/pre-commit-config.sh
```
