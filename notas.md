### Iniciar o docker-compose

```bash
docker-compose up --build
```

### Entrar nos containers

```bash
docker exec -it ransomware_attack_server_1 /bin/bash
docker exec -it ransomware_attack_client_1 /bin/bash
```

#### Em caso de emergência

```bash
docker-compose up --force-recreate
```
