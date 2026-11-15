package br.com.luzvital.bo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import br.com.luzvital.bo.RegraPrioridade.ItemAutonomia;

class RegraPrioridadeTest {

    private static ItemAutonomia suporteVida(int autonomia) {
        return new ItemAutonomia(autonomia, true);
    }

    private static ItemAutonomia comum(int autonomia) {
        return new ItemAutonomia(autonomia, false);
    }

    @Test
    @DisplayName("Prioridade 1: suporte de vida com autonomia menor que a duração")
    void suporteVidaInsuficiente() {
        assertEquals(1, RegraPrioridade.calcular(List.of(suporteVida(60)), 120));
    }

    @Test
    @DisplayName("Prioridade 1: suporte de vida e duração desconhecida")
    void suporteVidaDuracaoDesconhecida() {
        assertEquals(1, RegraPrioridade.calcular(List.of(suporteVida(600)), null));
    }

    @Test
    @DisplayName("Prioridade 1: suporte de vida sem bateria (0 min)")
    void suporteVidaSemBateria() {
        assertEquals(1, RegraPrioridade.calcular(List.of(suporteVida(0)), 30));
    }

    @Test
    @DisplayName("Prioridade 1 mesmo quando outro equipamento (não vital) tem bateria ainda menor")
    void suporteVidaNaoFicaEscondido() {
        assertEquals(1, RegraPrioridade.calcular(List.of(comum(10), suporteVida(60)), 120));
    }

    @Test
    @DisplayName("Prioridade 2: equipamento comum com autonomia insuficiente")
    void comumInsuficiente() {
        assertEquals(2, RegraPrioridade.calcular(List.of(comum(30), suporteVida(240)), 120));
    }

    @Test
    @DisplayName("Prioridade 2: equipamento comum e duração desconhecida")
    void comumDuracaoDesconhecida() {
        assertEquals(2, RegraPrioridade.calcular(List.of(comum(600)), null));
    }

    @Test
    @DisplayName("Prioridade 3: toda autonomia cobre a duração estimada")
    void autonomiaSuficiente() {
        assertEquals(3, RegraPrioridade.calcular(List.of(suporteVida(240), comum(180)), 120));
    }

    @Test
    @DisplayName("Prioridade 3: autonomia igual à duração é suficiente (regra usa 'menor que')")
    void autonomiaIgualDuracao() {
        assertEquals(3, RegraPrioridade.calcular(List.of(suporteVida(120)), 120));
    }

    @Test
    @DisplayName("Prioridade 3: paciente sem equipamento cadastrado")
    void semEquipamento() {
        assertEquals(3, RegraPrioridade.calcular(List.of(), null));
    }
}
