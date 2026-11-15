package br.com.luzvital.dao;

import java.sql.SQLException;
import java.util.Locale;
import java.util.Map;

import br.com.luzvital.exception.ConflitoException;
import br.com.luzvital.exception.PersistenciaException;
import br.com.luzvital.exception.ValidacaoException;

/**
 * Traduz os erros do Oracle (SQLException) em exceções de domínio.
 * Usa o código ORA e o nome da constraint (definidos em database/ddl.sql) para dar uma mensagem clara,
 * sem repassar o texto original do banco ao cliente.
 */
public final class SqlErrorTranslator {

    private static final int ORA_UNIQUE = 1;          // ORA-00001: unique constraint violated
    private static final int ORA_CHECK = 2290;        // ORA-02290: check constraint violated
    private static final int ORA_PAI_INEXISTENTE = 2291; // ORA-02291: parent key not found
    private static final int ORA_FILHOS_EXISTEM = 2292;  // ORA-02292: child record found
    private static final int ORA_NOT_NULL = 1400;     // ORA-01400: cannot insert NULL

    /** Mensagem amigável por constraint. */
    private static final Map<String, String> MENSAGENS = Map.ofEntries(
            Map.entry("UQ_REGIAO_NOME_CIDADE", "Já existe uma região com esse nome nessa cidade"),
            Map.entry("UQ_EQUIPAMENTO_NOME", "Já existe um equipamento com esse nome"),
            Map.entry("UQ_PAC_CONTATO_ORDEM", "O paciente já tem um contato com essa ordem de acionamento"),
            Map.entry("UQ_ALERTA", "Já existe alerta para esse contato nessa interrupção"),
            Map.entry("FK_PACIENTE_REGIAO", "A região tem pacientes vinculados"),
            Map.entry("FK_INTERRUPCAO_REGIAO", "A região tem interrupções vinculadas"),
            Map.entry("FK_PAC_CONTATO_PACIENTE",
                    "O paciente tem contatos vinculados. Para tirá-lo do monitoramento, atualize com ativo = false"),
            Map.entry("FK_ALERTA_PAC_CONTATO",
                    "O paciente tem alertas vinculados. Para tirá-lo do monitoramento, atualize com ativo = false"),
            Map.entry("FK_ALERTA_INTERRUPCAO", "A interrupção tem alertas vinculados"),
            Map.entry("FK_ACAO_APOIO_ALERTA", "O alerta tem ações de apoio vinculadas"),
            Map.entry("CK_PACIENTE_CEP", "CEP deve ter exatamente 8 dígitos"),
            Map.entry("CK_REGIAO_UF", "UF deve estar em letras maiúsculas"));

    private SqlErrorTranslator() {
    }

    public static RuntimeException traduzir(SQLException e, String operacao) {
        String constraint = extrairConstraint(e.getMessage());
        String mensagem = constraint == null ? null : MENSAGENS.get(constraint);

        return switch (e.getErrorCode()) {
            case ORA_UNIQUE -> new ConflitoException(mensagem != null ? mensagem : "Registro duplicado");
            case ORA_FILHOS_EXISTEM -> new ConflitoException(
                    mensagem != null ? mensagem : "O registro tem outros registros vinculados e não pode ser removido");
            case ORA_PAI_INEXISTENTE -> new ValidacaoException("Referência a um registro que não existe");
            case ORA_CHECK -> new ValidacaoException(mensagem != null ? mensagem : "Valor fora das regras permitidas");
            case ORA_NOT_NULL -> new ValidacaoException("Campo obrigatório não informado");
            default -> new PersistenciaException("Falha ao " + operacao + " (ORA-" + e.getErrorCode() + ")", e);
        };
    }

    /** Ex.: "ORA-00001: unique constraint (RM566278.UQ_REGIAO_NOME_CIDADE) violated" -> "UQ_REGIAO_NOME_CIDADE". */
    static String extrairConstraint(String mensagem) {
        if (mensagem == null) {
            return null;
        }
        int abre = mensagem.indexOf('(');
        int fecha = mensagem.indexOf(')', abre + 1);
        if (abre < 0 || fecha < 0) {
            return null;
        }
        String nome = mensagem.substring(abre + 1, fecha);
        int ponto = nome.lastIndexOf('.');
        return nome.substring(ponto + 1).replace("\"", "").toUpperCase(Locale.ROOT);
    }
}
