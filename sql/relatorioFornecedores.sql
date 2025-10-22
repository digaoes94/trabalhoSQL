SELECT f.cnpj
     , f.razaoSocial
     , f.nomeFantasia
     , f.email
     , f.telefone
     , e.cep
     , e.logradouro
     , e.numero
     , e.complemento
     , e.bairro
     , e.cidade
     , e.estado
  FROM fornecedores f
  LEFT JOIN enderecos e ON f.id_fornecedor = e.id_fornecedor
 ORDER BY f.razaoSocial