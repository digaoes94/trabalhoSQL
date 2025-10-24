SELECT f.cnpj as cnpj
     , f.razaoSocial as razaoSocial
     , f.nomeFantasia as nomeFantasia
     , f.email as email
     , f.telefone as telefone
     , e.cep as cep
     , e.logradouro as logradouro
     , e.numero as numero
     , e.complemento as complemento
     , e.bairro as bairro
     , e.cidade as cidade
     , e.estado as estado
  FROM fornecedores f
  LEFT JOIN enderecos e ON f.id_fornecedor = e.id_fornecedor
 ORDER BY f.razaoSocial