package br.com.luzvital.exception;

/**
 * Falha inesperada ao acessar o banco (HTTP 500).
 * A causa original fica só no log do servidor; o cliente recebe uma mensagem genérica.
 */
public class PersistenciaException extends RuntimeException {

    public PersistenciaException(String mensagem, Throwable causa) {
        super(mensagem, causa);
    }
}
