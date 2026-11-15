package br.com.luzvital.bo;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.luzvital.dao.PacienteDAO;
import br.com.luzvital.dao.RegiaoDAO;
import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.model.Paciente;

/** Regras de negócio de PACIENTE. */
@Service
public class PacienteBO {

    private final PacienteDAO pacienteDAO;
    private final RegiaoDAO regiaoDAO;
    private final Clock clock;

    @Autowired
    public PacienteBO(PacienteDAO pacienteDAO, RegiaoDAO regiaoDAO) {
        this(pacienteDAO, regiaoDAO, Clock.system(Fusos.BRASILIA));
    }

    PacienteBO(PacienteDAO pacienteDAO, RegiaoDAO regiaoDAO, Clock clock) {
        this.pacienteDAO = pacienteDAO;
        this.regiaoDAO = regiaoDAO;
        this.clock = clock;
    }

    public List<Paciente> listar() {
        return pacienteDAO.listar();
    }

    public Paciente buscarPorId(Long id) {
        return pacienteDAO.buscarPorId(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Paciente não encontrado"));
    }

    public Paciente criar(Paciente paciente) {
        validarENormalizar(paciente);
        paciente.setIdPaciente(null);
        if (paciente.getAtivo() == null) {
            paciente.setAtivo(true);
        }
        return pacienteDAO.inserir(paciente);
    }

    public Paciente atualizar(Long id, Paciente paciente) {
        Paciente atual = buscarPorId(id);
        validarENormalizar(paciente);
        paciente.setIdPaciente(id);
        if (paciente.getAtivo() == null) {
            paciente.setAtivo(atual.getAtivo());
        }
        if (!pacienteDAO.atualizar(paciente)) {
            throw new RecursoNaoEncontradoException("Paciente não encontrado");
        }
        paciente.setDataCadastro(atual.getDataCadastro());
        return paciente;
    }

    /**
     * Exclusão física. Se o paciente tiver contatos ou alertas, o banco bloqueia e a API devolve 409:
     * nesse caso, desative-o com PUT e "ativo": false.
     */
    public void remover(Long id) {
        if (!pacienteDAO.remover(id)) {
            throw new RecursoNaoEncontradoException("Paciente não encontrado");
        }
    }

    void validarENormalizar(Paciente p) {
        if (p == null) {
            throw new ValidacaoException("Dados do paciente não informados");
        }
        p.setNome(Validacoes.obrigatorio(p.getNome(), "nome", 120));

        Validacoes.obrigatorio(p.getDataNascimento(), "dataNascimento");
        if (p.getDataNascimento().isAfter(LocalDate.now(clock))) {
            throw new ValidacaoException("Campo 'dataNascimento' não pode estar no futuro");
        }

        p.setLogradouro(Validacoes.obrigatorio(p.getLogradouro(), "logradouro", 120));
        p.setNumero(Validacoes.obrigatorio(p.getNumero(), "numero", 10));
        p.setComplemento(Validacoes.opcional(p.getComplemento(), "complemento", 60));
        p.setObservacaoAtendimento(Validacoes.opcional(p.getObservacaoAtendimento(), "observacaoAtendimento", 255));
        p.setCep(normalizarCep(p.getCep()));

        Validacoes.obrigatorio(p.getIdRegiao(), "idRegiao");
        if (regiaoDAO.buscarPorId(p.getIdRegiao()).isEmpty()) {
            throw new RecursoNaoEncontradoException("Região não encontrada");
        }
    }

    /** Aceita "01310-100" ou "01310100" e guarda só os 8 dígitos. */
    static String normalizarCep(String cep) {
        String digitos = Validacoes.obrigatorio(cep, "cep", 20).replaceAll("[.\\-\\s]", "");
        if (!digitos.matches("\\d{8}")) {
            throw new ValidacaoException("Campo 'cep' deve ter 8 dígitos (ex.: 01310-100)");
        }
        return digitos;
    }
}
