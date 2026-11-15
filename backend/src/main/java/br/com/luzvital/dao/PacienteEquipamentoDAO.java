package br.com.luzvital.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import br.com.luzvital.config.ConnectionFactory;
import br.com.luzvital.model.PacienteEquipamento;

/** Acesso à tabela PACIENTE_EQUIPAMENTO. Por enquanto só leitura, usada pela geração de alertas. */
@Repository
public class PacienteEquipamentoDAO {

    private final ConnectionFactory connectionFactory;

    public PacienteEquipamentoDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    /** Equipamentos de todos os pacientes ativos de uma região, numa consulta só. */
    public List<PacienteEquipamento> listarDePacientesAtivosDaRegiao(Long idRegiao) {
        String sql = "SELECT pe.id_paciente_equipamento, pe.id_paciente, pe.id_equipamento, "
                + "pe.autonomia_bateria_min, pe.fonte_alternativa "
                + "FROM paciente_equipamento pe "
                + "INNER JOIN paciente p ON p.id_paciente = pe.id_paciente "
                + "WHERE p.id_regiao = ? AND p.ativo = 'S'";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, idRegiao);
            try (ResultSet rs = ps.executeQuery()) {
                List<PacienteEquipamento> lista = new ArrayList<>();
                while (rs.next()) {
                    lista.add(new PacienteEquipamento(
                            rs.getLong("id_paciente_equipamento"),
                            rs.getLong("id_paciente"),
                            rs.getLong("id_equipamento"),
                            rs.getInt("autonomia_bateria_min"),
                            rs.getString("fonte_alternativa")));
                }
                return lista;
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "listar equipamentos dos pacientes");
        }
    }
}
