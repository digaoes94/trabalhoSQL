from model.Endereco import Endereco
from model.Pessoa import Pessoa
from model.Fornecedor import Fornecedor
from model.Cliente import Cliente
from model.Produto import Produto
from model.Compra import Compra
from model.Venda import Venda
from model.ItemCompra import ItemCompra
from model.ItemVenda import ItemVenda
from datetime import date


"""MAIN CRIADO APENAS PARA TESTE DE CLASSE"""

def main():
    print("=== teste básico das classes ===\n")
    
    # teste 1: criar endereço
    print("1. testando endereco:")
    endereco = Endereco(
        cep="29027-419",
        logradouro="Rua Mário Rosendo",
        numero=456,
        bairro="Bela Vista",
        cidade="Vitória",
        estado="ES"
    )
    print(f"   {endereco.to_string()}\n")
    
    # teste 2: criar fornecedor
    print("2. testando fornecedor:")
    fornecedor = Fornecedor(
        id_fornecedor=1,
        cnpj="12.345.678/0001-90",
        razao_social="Bispo Tech Solutions Ltda",
        nome_fantasia="BTech Store",
        endereco=endereco,
        email="guilherme@techstore.com",
        telefones=["(27) 98855-2967"]
    )
    print(f"   {fornecedor.to_string()}\n")
    
    # teste 3: criar cliente
    print("3. testando cliente:")
    cliente = Cliente(
        id_cliente=1,
        cpf="123.456.789-00",
        nome="Guilherme Gonçalves",
        endereco=endereco,
        email="guilherme@gmail.com",
        telefones=["(27) 98855-2967"]
    )
    print(f"   {cliente.to_string()}\n")
    
    # teste 4: criar produto
    print("4. testando produto:")
    produto = Produto(
        id_produto=1,
        nome="Notebook Gamer",
        preco=3500.00,
        descricao="Notebook Gamer com RTX 4060 braba"
    )
    print(f"   {produto.to_string()}\n")
    
    # teste 5: criar itemcompra
    print("5. testando itemcompra:")
    item_compra = ItemCompra(
        produto=produto,
        quantidade=2,
        preco_unitario=3000.00,
        subtotal=6000.00
    )
    print(f"   {item_compra.to_string()}\n")
    
    # teste 6: criar compra
    print("6. testando compra:")
    compra = Compra(
        id_compra=1,
        fornecedor=fornecedor,
        itens=[item_compra],
        data=date.today(),
        total=6000.00
    )
    print(f"   {compra.to_string()}\n")
    
    # teste 7: criar itemvenda
    print("7. testando itemvenda:")
    item_venda = ItemVenda(
        produto=produto,
        quantidade=1,
        preco_unitario=3500.00,
        subtotal=3500.00
    )
    print(f"   {item_venda.to_string()}\n")
    
    # teste 8: criar venda
    print("8. testando venda:")
    venda = Venda(
        id_venda=1,
        cliente=cliente,
        itens=[item_venda],
        data=date.today(),
        total=3500.00
    )
    print(f"   {venda.to_string()}\n")
    
    print("=== tudo correto aqui! ===")

if __name__ == "__main__":
    main()
