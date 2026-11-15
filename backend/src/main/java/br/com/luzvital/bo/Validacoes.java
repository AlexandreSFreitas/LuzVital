package br.com.luzvital.bo;

import br.com.luzvital.exception.ValidacaoException;

/** Validações de campos de texto reaproveitadas pelas BOs. */
final class Validacoes {

    private Validacoes() {
    }

    /** Campo obrigatório: remove espaços das pontas, não pode ficar vazio nem passar do tamanho da coluna. */
    static String obrigatorio(String valor, String campo, int tamanhoMaximo) {
        if (valor == null || valor.isBlank()) {
            throw new ValidacaoException("Campo '" + campo + "' é obrigatório");
        }
        return tamanho(valor.strip(), campo, tamanhoMaximo);
    }

    /** Campo opcional: texto em branco vira null. */
    static String opcional(String valor, String campo, int tamanhoMaximo) {
        if (valor == null || valor.isBlank()) {
            return null;
        }
        return tamanho(valor.strip(), campo, tamanhoMaximo);
    }

    static void obrigatorio(Object valor, String campo) {
        if (valor == null) {
            throw new ValidacaoException("Campo '" + campo + "' é obrigatório");
        }
    }

    private static String tamanho(String valor, String campo, int tamanhoMaximo) {
        if (valor.length() > tamanhoMaximo) {
            throw new ValidacaoException("Campo '" + campo + "' aceita no máximo " + tamanhoMaximo + " caracteres");
        }
        return valor;
    }
}
