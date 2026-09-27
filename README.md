# IoT Distributed System with MQTT

Laboratório desenvolvido para a disciplina de Redes de Computadores II.

## Objetivo

Implementar um sistema IoT orientado a eventos utilizando MQTT,
Docker e comunicação Publisher/Subscriber.

## Arquitetura

O sistema possui três componentes principais:

- **IoT Sensor Publisher** — simula sensores de temperatura
- **EMQX MQTT Broker** — recebe e distribui mensagens via tópicos
- **Event Consumer** — recebe e processa os eventos

```
Sensor IoT ──PUBLISH──> EMQX Broker ──SUBSCRIBE──> Consumer
```

O Publisher **não conhece** o Consumer. Ambos conhecem apenas o Broker e o tópico.
Isso demonstra o **desacoplamento da arquitetura orientada a eventos**.

## Tecnologias

| Tecnologia     | Finalidade                          |
|----------------|-------------------------------------|
| Python         | Linguagem dos componentes           |
| Paho MQTT      | Cliente MQTT para Python            |
| MQTT           | Protocolo de mensageria             |
| EMQX           | Broker MQTT                         |
| Docker         | Containerização do broker           |
| Docker Compose | Orquestração do ambiente            |

## Estrutura do Projeto

```
iot-mqtt-lab/
├── src/
│   ├── publisher.py          # Sensor IoT simulado
│   └── consumer.py           # Consumidor de eventos
├── docs/
│   └── diagrams/
│       ├── c4-context.puml   # Diagrama C4 de Contexto
│       ├── c4-container.puml # Diagrama C4 de Containers
│       └── mqtt-sequence.puml# Diagrama de sequência MQTT
├── evidences/                # Screenshots de execução
├── docker-compose.yml        # Configuração do EMQX
├── requirements.txt          # Dependências Python
├── .gitignore
└── README.md
```

## Execução

### 1. Subir o Broker EMQX

```bash
docker compose up -d
```

Verificar:

```bash
docker compose ps
```

Acesse o Dashboard EMQX em: http://localhost:18083  
Credenciais padrão: `admin` / `public`

### 2. Instalar dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Iniciar o Consumer (Terminal 1)

```bash
python src/consumer.py
```

### 4. Iniciar o Publisher — QoS 0 (Terminal 2)

```bash
python src/publisher.py --device-id sensor-01 --qos 0
```

### 5. Iniciar o Publisher — QoS 1 (Terminal 3)

```bash
python src/publisher.py --device-id sensor-02 --qos 1
```

### 6. Múltiplos dispositivos

```bash
python src/publisher.py --device-id sensor-01 --qos 0
python src/publisher.py --device-id sensor-02 --qos 1
python src/publisher.py --device-id sensor-03 --qos 0
```

## Tópicos MQTT

Cada sensor publica em:

```
iot/temperature/{device_id}
```

O Consumer se inscreve com wildcard:

```
iot/temperature/+
```

O `+` captura qualquer device no nível do tópico.

## QoS (Quality of Service)

Foram utilizados dois níveis de QoS:

| QoS | Nome            | Garantia                          |
|-----|-----------------|-----------------------------------|
| 0   | At Most Once    | Sem confirmação, pode perder       |
| 1   | At Least Once   | Broker confirma com PUBACK         |

## Processamento de Eventos

O Consumer processa cada evento recebido:

- **Temperatura < 30°C** → `Temperature normal`
- **Temperatura ≥ 30°C** → `HIGH TEMPERATURE ALERT`

## Testes Realizados

- [x] Conexão com o broker EMQX
- [x] Publicação de eventos (QoS 0)
- [x] Publicação de eventos (QoS 1)
- [x] Consumo e processamento dos eventos
- [x] Múltiplos dispositivos simultâneos
- [x] Publicação periódica a cada 2 segundos
- [x] Wildcard subscription (`+`)

## Diagramas

Os diagramas C4 e de sequência estão disponíveis em `docs/diagrams/`:

- **C4 Contexto** — visão de alto nível do sistema
- **C4 Containers** — detalhamento dos componentes
- **Sequência MQTT** — fluxo de mensagens e QoS 1

## Autor

Hudson Silva
