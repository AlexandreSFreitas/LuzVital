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
import br.com.luzvital.model.Interrupcao;
import br.com.luzvital.model.OrigemInterrupcao;
import br.com.luzvital.model.StatusInterrupcao;

/** Acesso à tabela INTERRUPCAO com JDBC puro. */
@Repository
public class InterrupcaoDAO {

    private static final String COLUNAS =
            "id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status";

    private final ConnectionFactory connectionFactory;

    public InterrupcaoDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    public List<Interrupcao> listar() {
        String sql = "SELECT " + COLUNAS + " FROM interrupcao ORDER BY data_inicio DESC";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            List<Interrupcao> lista = new ArrayList<>();
            while (rs.next()) {
                lista.add(mapear(rs));
            }
            return lista;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "listar interrupções");
        }
    }

    public Optional<Interrupcao> buscarPorId(Long id) {
        String sql = "SELECT " + COLUNAS + " FROM interrupcao WHERE id_interrupcao = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? Optional.of(mapear(rs)) : Optional.empty();
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "buscar interrupção");
        }
    }

    /**
     * Insere usando a conexão recebida, sem commit: quem chama controla a transação
     * (a interrupção e os alertas são gravados juntos ou nada é gravado).
     */
    public Interrupcao inserir(Connection conn, Interrupcao i) throws SQLException {
        String sql = "INSERT INTO interrupcao (id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status) "
                + "VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement ps = conn.prepareStatement(sql, new String[] {"id_interrupcao"})) {
            ps.setLong(1, i.getIdRegiao());
            JdbcUtil.setTimestamp(ps, 2, i.getDataInicio());
            JdbcUtil.setTimestamp(ps, 3, i.getDataFim());
            JdbcUtil.setInteger(ps, 4, i.getDuracaoEstimadaMin());
            ps.setString(5, i.getOrigem().name());
            ps.setString(6, i.getStatus().name());
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    i.setIdInterrupcao(chaves.getLong(1));
                }
            }
            return i;
        }
    }

    private Interrupcao mapear(ResultSet rs) throws SQLException {
        Interrupcao i = new Interrupcao();
        i.setIdInterrupcao(rs.getLong("id_interrupcao"));
        i.setIdRegiao(rs.getLong("id_regiao"));
        i.setDataInicio(JdbcUtil.getLocalDateTime(rs, "data_inicio"));
        i.setDataFim(JdbcUtil.getLocalDateTime(rs, "data_fim"));
        i.setDuracaoEstimadaMin(JdbcUtil.getInteger(rs, "duracao_estimada_min"));
        i.setOrigem(OrigemInterrupcao.valueOf(rs.getString("origem")));
        i.setStatus(StatusInterrupcao.valueOf(rs.getString("status")));
        return i;
    }
}
