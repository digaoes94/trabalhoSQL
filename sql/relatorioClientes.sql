SELECT c.cpf
     , c.nome 
     , c.email
     , c.telefone
     , e.cep
     , e.logradouro
     , e.numero
     , e.complemento
     , e.bairro
     , e.cidade
     , e.estado
  FROM clientes c
  LEFT JOIN enderecos e ON c.id_cliente = e.id_cliente
 ORDER BY c.nome