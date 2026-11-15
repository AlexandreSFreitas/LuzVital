package br.com.luzvital.exception;

import java.time.OffsetDateTime;

/** Corpo padrão de erro da API: { "status": 404, "erro": "...", "timestamp": "..." }. */
public record ErroResponse(int status, String erro, OffsetDateTime timestamp) {

    public static ErroResponse of(int status, String erro) {
        return new ErroResponse(status, erro, OffsetDateTime.now());
    }
}
