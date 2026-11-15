package br.com.luzvital.bo;

import java.time.ZoneId;

/** Fuso usado nas regras de data. O servidor do render.com roda em UTC; os dados são de São Paulo. */
final class Fusos {

    static final ZoneId BRASILIA = ZoneId.of("America/Sao_Paulo");

    private Fusos() {
    }
}
