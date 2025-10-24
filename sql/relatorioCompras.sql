SELECT f.cnpj as cnpj
     , f.razaoSocial as razaoSocial
     , f.nomeFantasia as nomeFantasia
     , f.email as email_fornecedor
     , f.telefone as telefone_fornecedor
     , COUNT(co.id_compra) as total_de_compras
     , SUM(ic.quantidade) as total_itens_comprados
     , SUM(co.valor_total) as valor_total_gasto
     , AVG(co.valor_total) as valor_medio_compra
     , MAX(co.data_compra) as ultima_compra
  FROM compras co
  INNER JOIN fornecedores f ON co.id_fornecedor = f.id_fornecedor
  LEFT JOIN item_compra ic ON co.id_compra = ic.id_compra
 GROUP BY f.cnpj, f.razaoSocial, f.nomeFantasia, f.email, f.telefone
 ORDER BY valor_total_gasto DESC