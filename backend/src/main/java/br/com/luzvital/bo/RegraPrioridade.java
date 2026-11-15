package br.com.luzvital.bo;

import java.util.List;

/**
 * Regra operacional de prioridade do alerta (docs/DATABASE_MODEL.md, seção 4).
 * É uma regra acadêmica para ORDENAR avisos. Não é índice clínico e não substitui avaliação profissional.
 *
 * <ul>
 *   <li>1: algum equipamento de suporte de vida tem autonomia insuficiente;</li>
 *   <li>2: algum equipamento tem autonomia insuficiente;</li>
 *   <li>3: demais casos (inclusive paciente sem equipamento cadastrado).</li>
 * </ul>
 * "Insuficiente" = autonomia menor que a duração estimada, ou duração desconhecida (null).
 * Olhar TODOS os equipamentos (e não só o de menor autonomia) garante que um equipamento de suporte de vida
 * com pouca bateria nunca fique escondido atrás de outro equipamento com bateria ainda menor.
 */
public final class RegraPrioridade {

    public static final int PRIORIDADE_ALTA = 1;
    public static final int PRIORIDADE_MEDIA = 2;
    public static final int PRIORIDADE_BAIXA = 3;

    /** Dados mínimos de um equipamento do paciente para a regra. */
    public record ItemAutonomia(int autonomiaBateriaMin, boolean suporteVida) {
    }

    private RegraPrioridade() {
    }

    public static int calcular(List<ItemAutonomia> equipamentos, Integer duracaoEstimadaMin) {
        boolean algumInsuficiente = false;
        for (ItemAutonomia item : equipamentos) {
            if (insuficiente(item.autonomiaBateriaMin(), duracaoEstimadaMin)) {
                if (item.suporteVida()) {
                    return PRIORIDADE_ALTA;
                }
                algumInsuficiente = true;
            }
        }
        return algumInsuficiente ? PRIORIDADE_MEDIA : PRIORIDADE_BAIXA;
    }

    static boolean insuficiente(int autonomiaBateriaMin, Integer duracaoEstimadaMin) {
        return duracaoEstimadaMin == null || autonomiaBateriaMin < duracaoEstimadaMin;
    }
}
