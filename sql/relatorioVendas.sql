SELECT v.id_venda as id_venda
     , v.data_venda as data_venda
     , c.nome as nome_cliente
     , c.cpf as cpf_cliente
     , c.email as email_cliente
     , c.telefone as telefone_cliente
     , v.valor_total as valor_total
     , (SELECT SUM(quantidade) FROM item_venda iv WHERE iv.id_venda = v.id_venda) as total_itens
  FROM vendas v
  INNER JOIN clientes c ON v.id_cliente = c.id_cliente
 ORDER BY v.data_venda DESC