package br.com.luzvital.config;

import java.sql.Connection;
import java.sql.SQLException;

import javax.sql.DataSource;

import org.springframework.stereotype.Component;

/**
 * Entrega conexões JDBC para os DAOs.
 * O DataSource (pool HikariCP) é montado pelo Spring a partir de DB_URL, DB_USERNAME e DB_PASSWORD.
 * Quem pede a conexão é responsável por fechá-la (try-with-resources), o que a devolve ao pool.
 */
@Component
public class ConnectionFactory {

    private final DataSource dataSource;

    public ConnectionFactory(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
}
