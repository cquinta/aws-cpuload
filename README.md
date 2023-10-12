# aws-cpuload
App de teste para ELB e Auto Scaling Groups

* "/books" apresenta uma lista de livros em um banco mysql
* "/books/create" acresenta um livro no banco

É preciso ter um schema já criado e um usuário com poderes para criar as tabelas 

É necessário passar uma variável de ambiente para o container com a string de conexão por exemplo 
```bash

docker run -p 8080:5000 -d -e DBSTRING='mysql://<usuario>:<senha>@<endpoint>:<porta>/<banco>' cquinta/aws-cpuload  

```


    
