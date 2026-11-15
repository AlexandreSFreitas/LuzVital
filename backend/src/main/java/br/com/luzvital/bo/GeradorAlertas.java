package br.com.luzvital.bo;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import br.com.luzvital.bo.RegraPrioridade.ItemAutonomia;
import br.com.luzvital.model.Alerta;
import br.com.luzvital.model.Equipamento;
import br.com.luzvital.model.Paciente;
import br.com.luzvital.model.PacienteContato;
import br.com.luzvital.model.PacienteEquipamento;

/**
 * Cruza os pacientes afetados com os equipamentos e contatos deles e monta os alertas.
 * Não acessa o banco: recebe os dados prontos e devolve o plano, o que permite testar a regra isoladamente.
 */
public final class GeradorAlertas {

    /** Resultado do cruzamento: alertas a gravar e pacientes que não têm a quem avisar. */
    public record PlanoAlertas(List<Alerta> alertas, int pacientesAfetados, List<Long> pacientesSemContato) {
    }

    private GeradorAlertas() {
    }

    public static PlanoAlertas planejar(List<Paciente> pacientesAfetados,
                                        List<PacienteEquipamento> equipamentosDosPacientes,
                                        Map<Long, Equipamento> catalogo,
                                        List<PacienteContato> contatosDosPacientes,
                                        Integer duracaoEstimadaMin) {
        Map<Long, List<ItemAutonomia>> itensPorPaciente = new LinkedHashMap<>();
        for (PacienteEquipamento pe : equipamentosDosPacientes) {
            Equipamento equipamento = catalogo.get(pe.getIdEquipamento());
            boolean suporteVida = equipamento != null && equipamento.isSuporteVida();
            itensPorPaciente.computeIfAbsent(pe.getIdPaciente(), id -> new ArrayList<>())
                    .add(new ItemAutonomia(pe.getAutonomiaBateriaMin(), suporteVida));
        }

        Map<Long, List<PacienteContato>> contatosPorPaciente = new LinkedHashMap<>();
        for (PacienteContato pc : contatosDosPacientes) {
            contatosPorPaciente.computeIfAbsent(pc.getIdPaciente(), id -> new ArrayList<>()).add(pc);
        }

        List<Alerta> alertas = new ArrayList<>();
        List<Long> semContato = new ArrayList<>();
        for (Paciente paciente : pacientesAfetados) {
            Long id = paciente.getIdPaciente();
            int prioridade = RegraPrioridade.calcular(itensPorPaciente.getOrDefault(id, List.of()), duracaoEstimadaMin);

            List<PacienteContato> contatos = contatosPorPaciente.getOrDefault(id, List.of());
            if (contatos.isEmpty()) {
                // ALERTA exige um par (paciente, contato): sem contato não há alerta, mas a equipe precisa saber
                semContato.add(id);
                continue;
            }
            contatos.stream()
                    .sorted((a, b) -> Integer.compare(a.getOrdemAcionamento(), b.getOrdemAcionamento()))
                    .forEach(pc -> alertas.add(new Alerta(id, pc.getIdContato(), prioridade)));
        }

        // Prioridade 1 primeiro; dentro da mesma prioridade mantém a ordem de acionamento
        alertas.sort((a, b) -> Integer.compare(a.getPrioridade(), b.getPrioridade()));
        return new PlanoAlertas(alertas, pacientesAfetados.size(), semContato);
    }
}
