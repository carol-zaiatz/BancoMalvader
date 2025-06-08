-- Criação do banco
CREATE DATABASE IF NOT EXISTS banco_malvader;
USE banco_malvader;

-- =========================
-- TABELAS
-- =========================

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    tipo_usuario ENUM('FUNCIONARIO', 'CLIENTE') NOT NULL,
    senha_hash VARCHAR(32) NOT NULL,
    otp_ativo VARCHAR(6),
    otp_expiracao DATETIME
);

CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    codigo_funcionario VARCHAR(20) UNIQUE NOT NULL,
    cargo ENUM('ESTAGIARIO', 'ATENDENTE', 'GERENTE') NOT NULL,
    id_supervisor INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_supervisor) REFERENCES funcionario(id_funcionario)
);

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    score_credito DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    cep VARCHAR(10) NOT NULL,
    local VARCHAR(100) NOT NULL,
    numero_casa INT NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    estado CHAR(2) NOT NULL,
    complemento VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE agencia (
    id_agencia INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    codigo_agencia VARCHAR(10) UNIQUE NOT NULL,
    endereco_id INT,
    FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
);

CREATE TABLE conta (
    id_conta INT AUTO_INCREMENT PRIMARY KEY,
    numero_conta VARCHAR(20) UNIQUE NOT NULL,
    id_agencia INT,
    saldo DECIMAL(15,2) NOT NULL DEFAULT 0,
    tipo_conta ENUM('POUPANCA', 'CORRENTE', 'INVESTIMENTO') NOT NULL,
    id_cliente INT,
    data_abertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ATIVA', 'ENCERRADA', 'BLOQUEADA') NOT NULL DEFAULT 'ATIVA',
    FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE conta_poupanca (
    id_conta_poupanca INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE,
    taxa_rendimento DECIMAL(5,2) NOT NULL,
    ultimo_rendimento DATETIME,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_corrente (
    id_conta_corrente INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE,
    limite DECIMAL(15,2) NOT NULL DEFAULT 0,
    data_vencimento DATE NOT NULL,
    taxa_manutencao DECIMAL(5,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_investimento (
    id_conta_investimento INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE,
    perfil_risco ENUM('BAIXO', 'MEDIO', 'ALTO') NOT NULL,
    valor_minimo DECIMAL(15,2) NOT NULL,
    taxa_rendimento_base DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE transacao (
    id_transacao INT AUTO_INCREMENT PRIMARY KEY,
    id_conta_origem INT,
    id_conta_destino INT,
    tipo_transacao ENUM('DEPOSITO', 'SAQUE', 'TRANSFERENCIA', 'TAXA', 'RENDIMENTO') NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao VARCHAR(100),
    FOREIGN KEY (id_conta_origem) REFERENCES conta(id_conta),
    FOREIGN KEY (id_conta_destino) REFERENCES conta(id_conta)
);

CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    acao VARCHAR(50) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalhes TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE relatorio (
    id_relatorio INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT,
    tipo_relatorio VARCHAR(50) NOT NULL,
    data_geracao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    conteudo TEXT NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

-- =========================
-- GATILHOS (TRIGGERS)
-- =========================

DELIMITER $$

CREATE TRIGGER atualizar_saldo AFTER INSERT ON transacao
FOR EACH ROW
BEGIN
    IF NEW.tipo_transacao = 'DEPOSITO' THEN
        UPDATE conta SET saldo = saldo + NEW.valor WHERE id_conta = NEW.id_conta_origem;
    ELSEIF NEW.tipo_transacao IN ('SAQUE', 'TAXA') THEN
        UPDATE conta SET saldo = saldo - NEW.valor WHERE id_conta = NEW.id_conta_origem;
    ELSEIF NEW.tipo_transacao = 'TRANSFERENCIA' THEN
        UPDATE conta SET saldo = saldo - NEW.valor WHERE id_conta = NEW.id_conta_origem;
        UPDATE conta SET saldo = saldo + NEW.valor WHERE id_conta = NEW.id_conta_destino;
    END IF;
END$$

CREATE TRIGGER validar_senha BEFORE UPDATE ON usuario
FOR EACH ROW
BEGIN
    IF NEW.senha_hash REGEXP '^[0-9a-f]{32}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Senha deve ser atualizada via procedure com validação';
    END IF;
END$$

CREATE TRIGGER limite_deposito BEFORE INSERT ON transacao
FOR EACH ROW
BEGIN
    DECLARE total_dia DECIMAL(15,2);
    IF NEW.tipo_transacao = 'DEPOSITO' THEN
        SELECT COALESCE(SUM(valor), 0) INTO total_dia
        FROM transacao
        WHERE id_conta_origem = NEW.id_conta_origem
          AND tipo_transacao = 'DEPOSITO'
          AND DATE(data_hora) = DATE(NEW.data_hora);
        IF (total_dia + NEW.valor) > 10000 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Limite diário de depósito excedido';
        END IF;
    END IF;
END$$

DELIMITER ;

-- =========================
-- PROCEDURES
-- =========================

DELIMITER $$

CREATE PROCEDURE gerar_otp(IN id_usuario_input INT)
BEGIN
    DECLARE novo_otp VARCHAR(6);
    SET novo_otp = LPAD(FLOOR(RAND() * 1000000), 6, '0');
    UPDATE usuario
    SET otp_ativo = novo_otp,
        otp_expiracao = NOW() + INTERVAL 5 MINUTE
    WHERE id_usuario = id_usuario_input;
    SELECT novo_otp AS codigo_gerado;
END$$

CREATE PROCEDURE calcular_score_credito(IN id_cliente_input INT)
BEGIN
    DECLARE total_trans DECIMAL(15,2);
    DECLARE media_trans DECIMAL(15,2);
    SELECT SUM(valor), AVG(valor) INTO total_trans, media_trans
    FROM transacao t
    JOIN conta c ON t.id_conta_origem = c.id_conta
    WHERE c.id_cliente = id_cliente_input
      AND t.tipo_transacao IN ('DEPOSITO', 'SAQUE');
    UPDATE cliente
    SET score_credito = LEAST(100, (total_trans / 1000) + (media_trans / 100))
    WHERE id_cliente = id_cliente_input;
END$$

DELIMITER ;

-- =========================
-- VIEWS
-- =========================

CREATE VIEW vw_resumo_contas AS
SELECT c.id_cliente, u.nome, COUNT(co.id_conta) AS total_contas, SUM(co.saldo) AS saldo_total
FROM cliente c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN conta co ON c.id_cliente = co.id_cliente
GROUP BY c.id_cliente, u.nome;

CREATE VIEW vw_movimentacoes_recentes AS
SELECT t.*, c.numero_conta, u.nome AS cliente
FROM transacao t
JOIN conta c ON t.id_conta_origem = c.id_conta
JOIN cliente cl ON c.id_cliente = cl.id_cliente
JOIN usuario u ON cl.id_usuario = u.id_usuario
WHERE t.data_hora >= NOW() - INTERVAL 90 DAY;
