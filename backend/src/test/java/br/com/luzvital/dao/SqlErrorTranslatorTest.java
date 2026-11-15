package br.com.luzvital.dao;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import java.sql.SQLException;

import org.junit.jupiter.api.Test;

import br.com.luzvital.exception.ConflitoException;
import br.com.luzvital.exception.PersistenciaException;
import br.com.luzvital.exception.ValidacaoException;

class SqlErrorTranslatorTest {

    private static SQLException ora(int codigo, String mensagem) {
        return new SQLException(mensagem, "23000", codigo);
    }

    @Test
    void uniqueViraConflitoComMensagemDaConstraint() {
        RuntimeException e = SqlErrorTranslator.traduzir(
                ora(1, "ORA-00001: unique constraint (RM000000.UQ_REGIAO_NOME_CIDADE) violated"), "inserir região");
        assertInstanceOf(ConflitoException.class, e);
        assertEquals("Já existe uma região com esse nome nessa cidade", e.getMessage());
    }

    @Test
    void registroComFilhosViraConflito() {
        RuntimeException e = SqlErrorTranslator.traduzir(
                ora(2292, "ORA-02292: integrity constraint (RM000000.FK_PACIENTE_REGIAO) violated - child record found"),
                "remover região");
        assertInstanceOf(ConflitoException.class, e);
        assertEquals("A região tem pacientes vinculados", e.getMessage());
    }

    @Test
    void checkViraValidacao() {
        assertInstanceOf(ValidacaoException.class, SqlErrorTranslator.traduzir(
                ora(2290, "ORA-02290: check constraint (RM000000.CK_PACIENTE_CEP) violated"), "inserir paciente"));
    }

    @Test
    void erroDesconhecidoViraPersistencia() {
        assertInstanceOf(PersistenciaException.class,
                SqlErrorTranslator.traduzir(ora(17002, "IO Error: connection reset"), "listar regiões"));
    }

    @Test
    void extraiNomeDaConstraint() {
        assertEquals("UQ_ALERTA", SqlErrorTranslator.extrairConstraint(
                "ORA-00001: unique constraint (\"RM000000\".\"UQ_ALERTA\") violated"));
    }
}
