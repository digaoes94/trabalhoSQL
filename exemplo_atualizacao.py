#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE FUNCIONAMENTO: Atualização Seletiva de Campos
Demonstra como você pode atualizar só alguns campos mantendo outros
"""

def exemplo_atualizacao():
    # Dados simulados do cliente
    nome_atual = "João Silva"
    email_atual = "joao@email.com"
    telefone_atual = "27991234567"

    print("=" * 70)
    print("📋 ATUALIZANDO CLIENTE - DADOS ATUAIS")
    print("=" * 70)
    print(f"  Nome:     {nome_atual}")
    print(f"  Email:    {email_atual}")
    print(f"  Telefone: {telefone_atual}")
    print("\n" + "=" * 70)
    print("✏️  ATUALIZANDO CAMPOS (deixe em branco para manter o valor atual)")
    print("=" * 70)

    # Simulando as entradas do usuário
    print("\n1️⃣  NOME:")
    print(f"   Novo nome (Atual: {nome_atual}): ", end="")
    novo_nome = input() or nome_atual  # Se vazio, usa nome_atual

    print(f"\n2️⃣  EMAIL:")
    print(f"   Novo e-mail (Atual: {email_atual}): ", end="")
    novo_email = input() or email_atual  # Se vazio, usa email_atual

    print(f"\n3️⃣  TELEFONE:")
    print(f"   Novo telefone (Atual: {telefone_atual}): ", end="")
    novo_telefone = input() or telefone_atual  # Se vazio, usa telefone_atual

    # Mostrando o resultado
    print("\n" + "=" * 70)
    print("✅ RESULTADO DA ATUALIZAÇÃO")
    print("=" * 70)
    print(f"  Nome:     {novo_nome}")
    print(f"  Email:    {novo_email}")
    print(f"  Telefone: {novo_telefone}")
    print("=" * 70)

    # Mostrando o que mudou
    print("\n📝 RESUMO DAS ALTERAÇÕES:")
    if novo_nome != nome_atual:
        print(f"  ✏️  Nome: '{nome_atual}' → '{novo_nome}'")
    else:
        print(f"  ➖ Nome: mantido '{nome_atual}'")

    if novo_email != email_atual:
        print(f"  ✏️  Email: '{email_atual}' → '{novo_email}'")
    else:
        print(f"  ➖ Email: mantido '{email_atual}'")

    if novo_telefone != telefone_atual:
        print(f"  ✏️  Telefone: '{telefone_atual}' → '{novo_telefone}'")
    else:
        print(f"  ➖ Telefone: mantido '{telefone_atual}'")

if __name__ == "__main__":
    exemplo_atualizacao()
