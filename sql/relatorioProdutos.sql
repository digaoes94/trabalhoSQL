SELECT p.id_produto as id_produto
     , p.nome as nome_produto
     , p.descricao as descricao
     , p.preco_unitario as preco_unitario
     , COALESCE(e.quantidade, 0) as qtde_estoque
     , CASE
          WHEN COALESCE(e.quantidade, 0) = 0 THEN 'Sem Estoque'
          WHEN COALESCE(e.quantidade, 0) < 10 THEN 'Estoque Baixo'
          ELSE 'OK'
       END as status_estoque
  FROM produtos p
  LEFT JOIN estoque e ON p.id_produto = e.id_produto
 ORDER BY p.nome