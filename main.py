from utils.splash_screen import SplashScreen
from utils.config import MENU_PRINCIPAL, clear_console
from controller.Cont_Cliente import Cont_Cliente
from controller.Cont_Fornecedor import Cont_Fornecedor
from controller.Cont_Produto import Cont_Produto
from controller.Cont_Compra import Cont_Compra
from controller.Cont_Venda import Cont_Venda
from views.relatorios import Relatorio

# aqui mostramos informações iniciais vindas do utils/splash_screen.py e conexao
def mostrar_splash():
    splash = SplashScreen()
    # o splash ja deve estar mostrando a contagem de registros [cite: 189]
    print(splash.get_updated_screen())

# aqui inicializamos todos os controladores e relatorios necessários
def carregar_controladores():
    cliente_ctrl = Cont_Cliente()
    fornecedor_ctrl = Cont_Fornecedor()
    produto_ctrl = Cont_Produto()
    compra_ctrl = Cont_Compra()
    venda_ctrl = Cont_Venda()
    relatorio = Relatorio()
    return cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl, relatorio

# aqui fica o menu principal do sistema, menu gerado por utils/config.py
def menu_principal(cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl, relatorio):
    while True:
        print(MENU_PRINCIPAL)
        opcao = input("escolha uma opção: ")
        clear_console(1)
        
        # o edital pede 5 opções [cite: 181-185]
        if opcao == '1':
            # i) relatórios
            menu_relatorios(relatorio)
        elif opcao == '2':
            # ii) inserir registros
            menu_inserir(cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl)
        elif opcao == '3':
            # iii) remover registros
            menu_remover(cliente_ctrl, fornecedor_ctrl, produto_ctrl)
        elif opcao == '4':
            # iv) atualizar registros
            menu_atualizar(cliente_ctrl, fornecedor_ctrl, produto_ctrl)
        elif opcao == '5':
            # v) sair
            print("👋 Saindo do sistema... Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
            clear_console(1)

# aqui ficam as opções de relatório conforme views/relatorios.py e sql
def menu_relatorios(relatorio):
    # o menu precisa ficar constante 
    while True:
        clear_console(1)
        print("=" * 60)
        print("📊 RELATÓRIOS DISPONÍVEIS")
        print("=" * 60)
        print("1 - 👤 Clientes")
        print("2 - 🛒 Compras") 
        print("3 - 📦 Estoque")
        print("4 - 🏢 Fornecedores")
        print("5 - 📦 Produtos")
        print("6 - 💰 Vendas")
        print("0 - ⬅️  Voltar")
        print("=" * 60)
        op = input("escolha o relatório (0 para voltar): ")
        
        if op == '1':
            relatorio.get_relatorioClientes()
        elif op == '2':
            relatorio.get_relatorioCompras()
        elif op == '3':
            # relatorio especifico do trabalho [cite: 155]
            relatorio.get_relatorioEstoque()
        elif op == '4':
            relatorio.get_relatorioFornecedores()
        elif op == '5':
            relatorio.get_relatorioProdutos()
        elif op == '6':
            relatorio.get_relatorioVendas()
        elif op == '0':
            break # volta pro menu principal
        else:
            print("❌ Opção inválida!")
        
        input("\npressione enter para continuar...")


# menus das opções de inserção
def menu_inserir(cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl):
    # o menu precisa ficar constante 
    while True:
        clear_console(1)
        print("=" * 60)
        print("➕ INSERÇÃO DE REGISTROS")
        print("=" * 60)
        print("1 - 👤 Clientes")
        print("2 - 🏢 Fornecedores")
        print("3 - 📦 Produtos")
        print("4 - 🛒 Compras")
        print("5 - 💰 Vendas")
        print("0 - ⬅️  Voltar")
        print("=" * 60)
        op = input("selecione (0 para voltar): ")

        if op == '1':
            cliente_ctrl.novoCliente()
        elif op == '2':
            fornecedor_ctrl.novoFornecedor()
        elif op == '3':
            produto_ctrl.novoProduto()
        elif op == '4':
            compra_ctrl.novaCompra()
        elif op == '5':
            venda_ctrl.novaVenda()
        elif op == '0':
            break # volta pro menu principal
        else:
            print("❌ Opção inválida!")
        
        # o edital pede pra perguntar se quer inserir mais [cite: 210-211], o loop ja faz isso
        input("\npressione enter para continuar...")


# menus das opções de atualização
def menu_atualizar(cliente_ctrl, fornecedor_ctrl, produto_ctrl):
    # o menu precisa ficar constante 
    while True:
        clear_console(1)
        print("=" * 60)
        print("✏️  ATUALIZAÇÃO DE REGISTROS")
        print("=" * 60)
        print("1 - 👤 Clientes")
        print("2 - 🏢 Fornecedores")
        print("3 - 📦 Produtos")
        print("0 - ⬅️  Voltar")
        print("=" * 60)
        op = input("selecione (0 para voltar): ")

        if op == '1':
            cliente_ctrl.atualizarCliente()
        elif op == '2':
            fornecedor_ctrl.atualizarFornecedor()
        elif op == '3':
            produto_ctrl.atualizarProduto()
        elif op == '0':
            break # volta pro menu principal
        else:
            print("❌ Opção inválida!")

        input("\npressione enter para continuar...")


# menus das opções de remoção
def menu_remover(cliente_ctrl, fornecedor_ctrl, produto_ctrl):
    # o menu precisa ficar constante 
    while True:
        clear_console(1)
        print("=" * 60)
        print("🗑️  REMOÇÃO DE REGISTROS")
        print("=" * 60)
        print("1 - 👤 Clientes")
        print("2 - 🏢 Fornecedores")
        print("3 - 📦 Produtos")
        print("0 - ⬅️  Voltar")
        print("=" * 60)
        op = input("selecione (0 para voltar): ")

        if op == '1':
            cliente_ctrl.deletarCliente()
        elif op == '2':
            fornecedor_ctrl.deletarFornecedor()
        elif op == '3':
            produto_ctrl.deletarProduto()
        elif op == '0':
            break # volta pro menu principal
        else:
            print("❌ Opção inválida!")
        
        input("\npressione enter para continuar...")


# ponto de entrada do sistema
if __name__ == "__main__":
    mostrar_splash()
    
    # arrumando o unpack das variaveis que tava quebrado
    cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl, relatorio = carregar_controladores()
    
    # passando as variaveis certas pro menu
    menu_principal(cliente_ctrl, fornecedor_ctrl, produto_ctrl, compra_ctrl, venda_ctrl, relatorio)