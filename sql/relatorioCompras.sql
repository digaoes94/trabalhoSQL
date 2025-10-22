SELECT f.cnpj
     , f.razaoSocial as nome_fornecedor
     , f.nomeFantasia
     , f.email as email_fornecedor
     , f.telefone as telefone_fornecedor
     , COUNT(co.id_compra) as total_de_compras
     , SUM(co.valor_total) as valor_total_gasto
     , AVG(co.valor_total) as valor_medio_compra
     , MAX(co.data_compra) as ultima_compra
  FROM compras co
  INNER JOIN fornecedores f ON co.id_fornecedor = f.id_fornecedor
 GROUP BY f.cnpj, f.razaoSocial, f.nomeFantasia, f.email, f.telefone
 ORDER BY valor_total_gasto DESC