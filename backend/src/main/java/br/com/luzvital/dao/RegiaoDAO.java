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
import br.com.luzvital.model.Regiao;

/** Acesso à tabela REGIAO com JDBC puro. */
@Repository
public class RegiaoDAO {

    private static final String COLUNAS = "id_regiao, nome, cidade, uf";

    private final ConnectionFactory connectionFactory;

    public RegiaoDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    public List<Regiao> listar() {
        String sql = "SELECT " + COLUNAS + " FROM regiao ORDER BY cidade, nome";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            List<Regiao> regioes = new ArrayList<>();
            while (rs.next()) {
                regioes.add(mapear(rs));
            }
            return regioes;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "listar regiões");
        }
    }

    public Optional<Regiao> buscarPorId(Long id) {
        String sql = "SELECT " + COLUNAS + " FROM regiao WHERE id_regiao = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? Optional.of(mapear(rs)) : Optional.empty();
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "buscar região");
        }
    }

    public Regiao inserir(Regiao regiao) {
        String sql = "INSERT INTO regiao (nome, cidade, uf) VALUES (?, ?, ?)";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, new String[] {"id_regiao"})) {
            ps.setString(1, regiao.getNome());
            ps.setString(2, regiao.getCidade());
            ps.setString(3, regiao.getUf());
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    regiao.setIdRegiao(chaves.getLong(1));
                }
            }
            return regiao;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "inserir região");
        }
    }

    /** @return true se alguma linha foi atualizada */
    public boolean atualizar(Regiao regiao) {
        String sql = "UPDATE regiao SET nome = ?, cidade = ?, uf = ? WHERE id_regiao = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, regiao.getNome());
            ps.setString(2, regiao.getCidade());
            ps.setString(3, regiao.getUf());
            ps.setLong(4, regiao.getIdRegiao());
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "atualizar região");
        }
    }

    /** @return true se alguma linha foi removida */
    public boolean remover(Long id) {
        String sql = "DELETE FROM regiao WHERE id_regiao = ?";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "remover região");
        }
    }

    private Regiao mapear(ResultSet rs) throws SQLException {
        return new Regiao(
                rs.getLong("id_regiao"),
                rs.getString("nome"),
                rs.getString("cidade"),
                rs.getString("uf"));
    }
}
