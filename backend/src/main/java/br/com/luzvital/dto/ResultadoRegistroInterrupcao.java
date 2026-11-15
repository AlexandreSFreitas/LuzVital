package br.com.luzvital.dto;

import java.util.List;
import java.util.Map;

import br.com.luzvital.model.Alerta;
import br.com.luzvital.model.Interrupcao;

/**
 * Resposta do POST /api/interrupcoes.
 * Por privacidade, identifica pacientes e contatos só pelo ID (sem nome, endereço ou telefone).
 */
public record ResultadoRegistroInterrupcao(
        Interrupcao interrupcao,
        int pacientesAfetados,
        int alertasGerados,
        Map<Integer, Long> alertasPorPrioridade,
        List<Long> pacientesSemContato,
        List<Alerta> alertas) {
}
