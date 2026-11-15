package br.com.luzvital.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import br.com.luzvital.config.ConnectionFactory;
import br.com.luzvital.model.CategoriaEquipamento;
import br.com.luzvital.model.Equipamento;

/** Acesso à tabela EQUIPAMENTO (catálogo). Por enquanto só leitura, usada pela geração de alertas. */
@Repository
public class EquipamentoDAO {

    private final ConnectionFactory connectionFactory;

    public EquipamentoDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    public List<Equipamento> listar() {
        String sql = "SELECT id_equipamento, nome, categoria, consumo_watts, suporte_vida FROM equipamento ORDER BY nome";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            List<Equipamento> equipamentos = new ArrayList<>();
            while (rs.next()) {
                equipamentos.add(new Equipamento(
                        rs.getLong("id_equipamento"),
                        rs.getString("nome"),
                        CategoriaEquipamento.valueOf(rs.getString("categoria")),
                        rs.getInt("consumo_watts"),
                        JdbcUtil.flag(rs.getString("suporte_vida"))));
            }
            return equipamentos;
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "listar equipamentos");
        }
    }
}
