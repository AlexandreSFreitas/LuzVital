package br.com.luzvital.exception;

/** A operação conflita com o estado do banco: duplicidade ou registro com vínculos (HTTP 409). */
public class ConflitoException extends RuntimeException {

    public ConflitoException(String mensagem) {
        super(mensagem);
    }
}
