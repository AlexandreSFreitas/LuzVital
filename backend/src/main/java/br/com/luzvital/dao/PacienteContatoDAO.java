package br.com.luzvital.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import br.com.luzvital.config.ConnectionFactory;
import br.com.luzvital.model.PacienteContato;

/** Acesso à tabela PACIENTE_CONTATO. Por enquanto só leitura, usada pela geração de alertas. */
@Repository
public class PacienteContatoDAO {

    private final ConnectionFactory connectionFactory;

    public PacienteContatoDAO(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    /** Contatos de todos os pacientes ativos de uma região, já na ordem de acionamento. */
    public List<PacienteContato> listarDePacientesAtivosDaRegiao(Long idRegiao) {
        String sql = "SELECT pc.id_paciente, pc.id_contato, pc.ordem_acionamento, pc.vinculo "
                + "FROM paciente_contato pc "
                + "INNER JOIN paciente p ON p.id_paciente = pc.id_paciente "
                + "WHERE p.id_regiao = ? AND p.ativo = 'S' "
                + "ORDER BY pc.id_paciente, pc.ordem_acionamento";
        try (Connection conn = connectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, idRegiao);
            try (ResultSet rs = ps.executeQuery()) {
                List<PacienteContato> lista = new ArrayList<>();
                while (rs.next()) {
                    lista.add(new PacienteContato(
                            rs.getLong("id_paciente"),
                            rs.getLong("id_contato"),
                            rs.getInt("ordem_acionamento"),
                            rs.getString("vinculo")));
                }
                return lista;
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "listar contatos dos pacientes");
        }
    }
}
