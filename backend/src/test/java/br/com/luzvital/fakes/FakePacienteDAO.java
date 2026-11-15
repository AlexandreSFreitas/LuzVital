package br.com.luzvital.fakes;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

import br.com.luzvital.dao.PacienteDAO;
import br.com.luzvital.model.Paciente;

/** PacienteDAO em memória, para testar a BO sem Oracle. */
public class FakePacienteDAO extends PacienteDAO {

    private final Map<Long, Paciente> dados = new TreeMap<>();
    private long proximoId = 1;

    public FakePacienteDAO() {
        super(null);
    }

    @Override
    public List<Paciente> listar() {
        return new ArrayList<>(dados.values());
    }

    @Override
    public Optional<Paciente> buscarPorId(Long id) {
        return Optional.ofNullable(dados.get(id));
    }

    @Override
    public Paciente inserir(Paciente p) {
        p.setIdPaciente(proximoId++);
        p.setDataCadastro(LocalDateTime.of(2026, 11, 14, 10, 0));
        dados.put(p.getIdPaciente(), p);
        return p;
    }

    @Override
    public boolean atualizar(Paciente p) {
        if (!dados.containsKey(p.getIdPaciente())) {
            return false;
        }
        dados.put(p.getIdPaciente(), p);
        return true;
    }

    @Override
    public boolean remover(Long id) {
        return dados.remove(id) != null;
    }
}
