select f.cnpj
     , f.nome as nome_fornecedor
     , count(co.id_compra) as total_de_compras
     , sum(co.valor_total) as valor_total_gasto
  from compras co
 inner join fornecedores f
    on co.id_fornecedor = f.id_fornecedor
 group by f.cnpj, f.nome
 order by valor_total_gasto desc