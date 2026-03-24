# Atividade 01 - C216

Essa atividade simples tem como objetivo relembrar os fundamentos de Python para
as futuras atividades que vamos desenvolver no semestre.

## Executando

Foi criado um container Docker para executar a aplicação. Certifique-se de possuir
a infraestrutura do Docker em sua máquina local. Em seguida, é preciso construir a 
imagem para que depois consigamos executá-la localmente:

```
docker build -t student_management . # Ou o nome que preferir ao invés de student_management
docker run --rm -it student_management
```
