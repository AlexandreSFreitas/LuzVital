package br.com.luzvital.exception;

/** Dados de entrada inválidos (HTTP 400). */
public class ValidacaoException extends RuntimeException {

    public ValidacaoException(String mensagem) {
        super(mensagem);
    }
}
