SELECT p.id_produto as id_produto
     , p.nome as nome_produto
     , p.descricao as descricao
     , p.preco_unitario as preco_unitario
     , p.qtde_estoque as qtde_estoque
     , CASE
          WHEN p.qtde_estoque = 0 THEN 'Sem Estoque'
          WHEN p.qtde_estoque < 10 THEN 'Estoque Baixo'
          ELSE 'OK'
       END as status_estoque
  FROM produtos p
 ORDER BY p.nome