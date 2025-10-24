SELECT c.cpf
     , c.nome as nome
     , c.email as email
     , c.telefone as telefone
     , e.cep as cep
     , e.logradouro as logradouro
     , e.numero as numero
     , e.complemento as complemento
     , e.bairro as bairro
     , e.cidade as cidade
     , e.estado as estado
  FROM clientes c
  LEFT JOIN enderecos e ON c.id_cliente = e.id_cliente
 ORDER BY c.nome