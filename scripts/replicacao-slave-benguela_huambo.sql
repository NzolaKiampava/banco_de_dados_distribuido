use mercadokwanza;

# Configura a replicação no Slave Benguela:

CHANGE MASTER TO
  MASTER_HOST='no-luanda',
  MASTER_USER='root',
  MASTER_PASSWORD='kwanza2024',
  MASTER_LOG_FILE='mysql-bin.000003',
  MASTER_LOG_POS=157;

START SLAVE;
SHOW SLAVE STATUS;


# Repete para o Slave Huambo:

CHANGE MASTER TO
  MASTER_HOST='no-luanda',
  MASTER_USER='root',
  MASTER_PASSWORD='kwanza2024',
  MASTER_LOG_FILE='mysql-bin.000003',
  MASTER_LOG_POS=157;

START SLAVE;
SHOW SLAVE STATUS