package br.com.luzvital.bo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

import br.com.luzvital.bo.GeradorAlertas.PlanoAlertas;
import br.com.luzvital.model.Alerta;
import br.com.luzvital.model.CategoriaEquipamento;
import br.com.luzvital.model.Equipamento;
import br.com.luzvital.model.Paciente;
import br.com.luzvital.model.PacienteContato;
import br.com.luzvital.model.PacienteEquipamento;
import br.com.luzvital.model.StatusAlerta;

class GeradorAlertasTest {

    private static final Map<Long, Equipamento> CATALOGO = Map.of(
            1L, new Equipamento(1L, "Ventilador mecânico", CategoriaEquipamento.RESPIRATORIO, 150, true),
            2L, new Equipamento(2L, "Bomba de dieta", CategoriaEquipamento.ALIMENTACAO, 20, false));

    private static Paciente paciente(long id) {
        Paciente p = new Paciente();
        p.setIdPaciente(id);
        return p;
    }

    @Test
    void geraUmAlertaPorContatoNaOrdemDeAcionamentoEComPrioridadeDoPaciente() {
        PlanoAlertas plano = GeradorAlertas.planejar(
                List.of(paciente(10)),
                List.of(new PacienteEquipamento(1L, 10L, 1L, 60, null)),
                CATALOGO,
                // fora de ordem de propósito
                List.of(new PacienteContato(10L, 200L, 2, "cuidadora"), new PacienteContato(10L, 100L, 1, "filha")),
                120);

        assertEquals(1, plano.pacientesAfetados());
        assertEquals(2, plano.alertas().size());
        assertEquals(100L, plano.alertas().get(0).getIdContato());
        assertEquals(200L, plano.alertas().get(1).getIdContato());
        assertTrue(plano.alertas().stream().allMatch(a -> a.getPrioridade() == 1));
        assertTrue(plano.alertas().stream().allMatch(a -> a.getStatus() == StatusAlerta.PENDENTE));
        assertTrue(plano.pacientesSemContato().isEmpty());
    }

    @Test
    void pacienteSemContatoNaoGeraAlertaMasApareceNoResultado() {
        PlanoAlertas plano = GeradorAlertas.planejar(
                List.of(paciente(10), paciente(11)),
                List.of(),
                CATALOGO,
                List.of(new PacienteContato(10L, 100L, 1, "filha")),
                60);

        assertEquals(2, plano.pacientesAfetados());
        assertEquals(1, plano.alertas().size());
        assertEquals(List.of(11L), plano.pacientesSemContato());
    }

    @Test
    void alertasSaemOrdenadosPorPrioridade() {
        PlanoAlertas plano = GeradorAlertas.planejar(
                List.of(paciente(10), paciente(11), paciente(12)),
                List.of(
                        new PacienteEquipamento(1L, 10L, 2L, 300, null),  // comum, suficiente -> 3
                        new PacienteEquipamento(2L, 11L, 2L, 30, null),   // comum, insuficiente -> 2
                        new PacienteEquipamento(3L, 12L, 1L, 30, null)),  // suporte de vida, insuficiente -> 1
                CATALOGO,
                List.of(new PacienteContato(10L, 100L, 1, null),
                        new PacienteContato(11L, 101L, 1, null),
                        new PacienteContato(12L, 102L, 1, null)),
                120);

        List<Integer> prioridades = plano.alertas().stream().map(Alerta::getPrioridade).toList();
        assertEquals(List.of(1, 2, 3), prioridades);
        assertEquals(12L, plano.alertas().get(0).getIdPaciente());
    }

    @Test
    void regiaoSemPacientesNaoGeraNada() {
        PlanoAlertas plano = GeradorAlertas.planejar(List.of(), List.of(), CATALOGO, List.of(), 60);

        assertEquals(0, plano.pacientesAfetados());
        assertTrue(plano.alertas().isEmpty());
        assertTrue(plano.pacientesSemContato().isEmpty());
    }
}
