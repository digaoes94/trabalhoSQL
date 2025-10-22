select p.id_produto
     , p.nome as nome_produto
     , p.qtde_estoque
     , case 
          when p.qtde_estoque = 0 then 'Sem Estoque'
          when p.qtde_estoque < 10 then 'Estoque Baixo'
          else 'OK'
       end as status_estoque
  from produtos p
 order by p.qtde_estoque asc, p.nome asc