import mysql.connector
import datetime

def log(no, operacao, resultado):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] [{no:10}] {operacao:35} -> {resultado}')

def conectar(porta):
    return mysql.connector.connect(
        host='127.0.0.1', port=porta,
        user='root', password='kwanza2024',
        database='mercadokwanza',
        autocommit=False
    )

PRODUTO_ID   = 5
LOJA_BENGUELA = 6
LOJA_LUANDA   = 1
CLIENTE_ID    = 42
QUANTIDADE    = 10

no_luanda   = conectar(3310)
no_benguela = conectar(3307)
cur_l = no_luanda.cursor()
cur_b = no_benguela.cursor()

try:
    # Ver stock antes
    cur_b.execute('SELECT quantidade FROM STOCK WHERE produto_id=%s AND loja_id=%s', (PRODUTO_ID, LOJA_BENGUELA))
    stock_antes = cur_b.fetchone()[0]
    print(f'Stock em Benguela ANTES: {stock_antes}')

    # Ver vendas antes
    cur_l.execute('SELECT COUNT(*) FROM VENDA')
    vendas_antes = cur_l.fetchone()[0]
    print(f'Vendas em Luanda ANTES: {vendas_antes}')

    # FASE 1 — decrementar stock em Benguela
    cur_b.execute('SELECT quantidade FROM STOCK WHERE produto_id=%s AND loja_id=%s FOR UPDATE', (PRODUTO_ID, LOJA_BENGUELA))
    resultado = cur_b.fetchone()
    if resultado is None or resultado[0] < QUANTIDADE:
        raise Exception(f'Stock insuficiente: disponivel={resultado[0] if resultado else 0}')

    cur_b.execute('UPDATE STOCK SET quantidade=quantidade-%s WHERE produto_id=%s AND loja_id=%s', (QUANTIDADE, PRODUTO_ID, LOJA_BENGUELA))
    log('Benguela', 'UPDATE STOCK', 'OK')

    # FASE 2 — registar venda em Luanda
    # cur_l.execute('INSERT INTO VENDA (loja_id, cliente_id, data_venda, total) VALUES (%s,%s,NOW(),%s)', (LOJA_LUANDA, CLIENTE_ID, QUANTIDADE * 1500))
    raise Exception('Erro simulado antes do INSERT em Luanda')
    cur_l.execute('INSERT INTO VENDA (loja_id, cliente_id, data_venda, total) VALUES (%s,%s,NOW(),%s)', (LOJA_LUANDA, CLIENTE_ID, QUANTIDADE * 1500))
    
    venda_id = cur_l.lastrowid
    cur_l.execute('INSERT INTO ITEM_VENDA (venda_id, produto_id, qtd, preco_unit, desconto) VALUES (%s,%s,%s,%s,%s)', (venda_id, PRODUTO_ID, QUANTIDADE, 1500, 0.0))
    log('Luanda', 'INSERT VENDA', 'OK')

    # COMMIT nos dois nós
    no_benguela.commit()
    no_luanda.commit()
    log('Benguela', 'COMMIT', 'OK')
    log('Luanda',   'COMMIT', 'OK')
    print('✓ Transação concluída com sucesso.')

except Exception as e:
    no_benguela.rollback()
    no_luanda.rollback()
    log('Benguela', 'ROLLBACK', 'executado')
    log('Luanda',   'ROLLBACK', 'executado')
    print(f'✗ ROLLBACK efectuado. Motivo: {e}')

finally:
    cur_l.close(); cur_b.close()
    no_luanda.close(); no_benguela.close()