package br.com.luzvital.dao;

import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.sql.Types;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** Conversões repetidas entre tipos Java e colunas Oracle (valores nulos, datas, flags S/N). */
final class JdbcUtil {

    private JdbcUtil() {
    }

    static void setInteger(PreparedStatement ps, int indice, Integer valor) throws SQLException {
        if (valor == null) {
            ps.setNull(indice, Types.NUMERIC);
        } else {
            ps.setInt(indice, valor);
        }
    }

    static void setTimestamp(PreparedStatement ps, int indice, LocalDateTime valor) throws SQLException {
        if (valor == null) {
            ps.setNull(indice, Types.TIMESTAMP);
        } else {
            ps.setTimestamp(indice, Timestamp.valueOf(valor));
        }
    }

    static void setDate(PreparedStatement ps, int indice, LocalDate valor) throws SQLException {
        if (valor == null) {
            ps.setNull(indice, Types.DATE);
        } else {
            ps.setDate(indice, Date.valueOf(valor));
        }
    }

    static Integer getInteger(ResultSet rs, String coluna) throws SQLException {
        int valor = rs.getInt(coluna);
        return rs.wasNull() ? null : valor;
    }

    static LocalDateTime getLocalDateTime(ResultSet rs, String coluna) throws SQLException {
        Timestamp ts = rs.getTimestamp(coluna);
        return ts == null ? null : ts.toLocalDateTime();
    }

    static LocalDate getLocalDate(ResultSet rs, String coluna) throws SQLException {
        // DATE no Oracle guarda hora também; lemos como Timestamp e ficamos só com a data
        Timestamp ts = rs.getTimestamp(coluna);
        return ts == null ? null : ts.toLocalDateTime().toLocalDate();
    }

    static String flag(boolean valor) {
        return valor ? "S" : "N";
    }

    static boolean flag(String valor) {
        return "S".equals(valor);
    }
}
