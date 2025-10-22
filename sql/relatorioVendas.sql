select v.id_venda
     , v.data_venda
     , c.nome as nome_cliente
     , c.cpf as cpf_cliente
     , v.valor_total
  from vendas v
 inner join clientes c
    on v.id_cliente = c.id_cliente
 order by v.data_venda desc