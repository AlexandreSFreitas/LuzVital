package br.com.luzvital.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Repository;

import br.com.luzvital.config.ConnectionFactory;
import br.com.luzvital.model.Paciente;

/** Acesso à tabela PACIENTE com JDBC puro. */
@Repository
public class PacienteDAO {

    private static final String COLUNAS = "id_paciente, nome, data_nascimento, logradouro, numero, complemento, "
            + "cep, id_regiao, observacao_atendimento, ativo, data_cadastro";

    private final ConnectionFactory connectionFactory;

    public PacienteDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    public List<Paciente> listar() {
        return consultar("SELECT " + COLUNAS + " FROM paciente ORDER BY nome", null, "listar pacientes");
    }

    /** Pacientes ativos de uma região: são os afetados quando falta energia ali. */
    public List<Paciente> listarAtivosPorRegiao(Long idRegiao) {
        String sql = "SELECT " + COLUNAS + " FROM paciente WHERE id_regiao = ? AND ativo = 'S' ORDER BY id_paciente";
        return consultar(sql, idRegiao, "listar pacientes da região");
    }

    public Optional<Paciente> buscarPorId(Long id) {
        String sql = "SELECT " + COLUNAS + " FROM paciente WHERE id_paciente = ?";
        return consultar(sql, id, "buscar paciente").stream().findFirst();
    }

    public Paciente inserir(Paciente p) {
        String sql = "INSERT INTO paciente (nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, "
                + "observacao_atendimento, ativo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, new String[] {"id_paciente"})) {
            preencher(ps, p);
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    p.setIdPaciente(chaves.getLong(1));
                }
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "inserir paciente");
        }
        // relê para devolver a data_cadastro gerada pelo banco
        return buscarPorId(p.getIdPaciente()).orElse(p);
    }

    /** @return true se alguma linha foi atualizada */
    public boolean atualizar(Paciente p) {
        String sql = "UPDATE paciente SET nome = ?, data_nascimento = ?, logradouro = ?, numero = ?, complemento = ?, "
                + "cep = ?, id_regiao = ?, observacao_atendimento = ?, ativo = ? WHERE id_paciente = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            preencher(ps, p);
            ps.setLong(10, p.getIdPaciente());
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "atualizar paciente");
        }
    }

    /**
     * Remove o paciente. Os equipamentos dele saem junto (ON DELETE CASCADE);
     * se houver contatos ou alertas vinculados, o Oracle bloqueia (ORA-02292 -> 409).
     * @return true se alguma linha foi removida
     */
    public boolean remover(Long id) {
        String sql = "DELETE FROM paciente WHERE id_paciente = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "remover paciente");
        }
    }

    private List<Paciente> consultar(String sql, Long parametro, String operacao) {
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            if (parametro != null) {
                ps.setLong(1, parametro);
            }
            try (ResultSet rs = ps.executeQuery()) {
                List<Paciente> pacientes = new ArrayList<>();
                while (rs.next()) {
                    pacientes.add(mapear(rs));
                }
                return pacientes;
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, operacao);
        }
    }

    /** Preenche os parâmetros 1 a 9, na ordem das colunas do INSERT/UPDATE. */
    private void preencher(PreparedStatement ps, Paciente p) throws SQLException {
        ps.setString(1, p.getNome());
        JdbcUtil.setDate(ps, 2, p.getDataNascimento());
        ps.setString(3, p.getLogradouro());
        ps.setString(4, p.getNumero());
        ps.setString(5, p.getComplemento());
        ps.setString(6, p.getCep());
        ps.setLong(7, p.getIdRegiao());
        ps.setString(8, p.getObservacaoAtendimento());
        ps.setString(9, JdbcUtil.flag(Boolean.TRUE.equals(p.getAtivo())));
    }

    private Paciente mapear(ResultSet rs) throws SQLException {
        Paciente p = new Paciente();
        p.setIdPaciente(rs.getLong("id_paciente"));
        p.setNome(rs.getString("nome"));
        p.setDataNascimento(JdbcUtil.getLocalDate(rs, "data_nascimento"));
        p.setLogradouro(rs.getString("logradouro"));
        p.setNumero(rs.getString("numero"));
        p.setComplemento(rs.getString("complemento"));
        p.setCep(rs.getString("cep"));
        p.setIdRegiao(rs.getLong("id_regiao"));
        p.setObservacaoAtendimento(rs.getString("observacao_atendimento"));
        p.setAtivo(JdbcUtil.flag(rs.getString("ativo")));
        p.setDataCadastro(JdbcUtil.getLocalDateTime(rs, "data_cadastro"));
        return p;
    }
}
