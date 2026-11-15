package br.com.luzvital.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import org.springframework.stereotype.Repository;

import br.com.luzvital.model.Alerta;

/** Acesso à tabela ALERTA com JDBC puro. Por enquanto só a inserção feita pela geração de alertas. */
@Repository
public class AlertaDAO {

    /**
     * Insere usando a conexão recebida, sem commit: faz parte da transação do registro da interrupção.
     * data_criacao fica com o DEFAULT SYSTIMESTAMP do banco e é devolvida junto com o ID.
     */
    public Alerta inserir(Connection conn, Alerta a) throws SQLException {
        String sql = "INSERT INTO alerta (id_interrupcao, id_paciente, id_contato, prioridade, status) "
                + "VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement ps = conn.prepareStatement(sql, new String[] {"id_alerta", "data_criacao"})) {
            ps.setLong(1, a.getIdInterrupcao());
            ps.setLong(2, a.getIdPaciente());
            ps.setLong(3, a.getIdContato());
            ps.setInt(4, a.getPrioridade());
            ps.setString(5, a.getStatus().name());
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    a.setIdAlerta(chaves.getLong(1));
                    var criacao = chaves.getTimestamp(2);
                    a.setDataCriacao(criacao == null ? null : criacao.toLocalDateTime());
                }
            }
            return a;
        }
    }
}
