USE mercadokwanza;

# 3 views de fragmentação horizontal de VENDA:
CREATE OR REPLACE VIEW frag_venda_luanda AS
  SELECT v.* FROM VENDA v
  JOIN LOJA l ON v.loja_id = l.id
  WHERE l.provincia_id = 1;

CREATE OR REPLACE VIEW frag_venda_benguela AS
  SELECT v.* FROM VENDA v
  JOIN LOJA l ON v.loja_id = l.id
  WHERE l.provincia_id = 2;

CREATE OR REPLACE VIEW frag_venda_huambo AS
  SELECT v.* FROM VENDA v
  JOIN LOJA l ON v.loja_id = l.id
  WHERE l.provincia_id = 3;
  
#Verifica a completude (soma deve ser igual ao total):
SELECT 'Luanda'      AS provincia, COUNT(*) AS total FROM frag_venda_luanda
UNION ALL
SELECT 'Benguela',                 COUNT(*)           FROM frag_venda_benguela
UNION ALL
SELECT 'Huambo',                   COUNT(*)           FROM frag_venda_huambo
UNION ALL
SELECT 'TOTAL GERAL',              COUNT(*)           FROM VENDA;



# Cria a fragmentação vertical de PRODUTO:

CREATE OR REPLACE VIEW produto_catalogo AS
  SELECT id, descricao, categoria FROM PRODUTO;

CREATE OR REPLACE VIEW produto_comercial AS
  SELECT id, preco, activo FROM PRODUTO;