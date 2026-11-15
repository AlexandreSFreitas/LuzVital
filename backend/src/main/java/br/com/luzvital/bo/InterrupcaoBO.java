package br.com.luzvital.bo;

import java.sql.Connection;
import java.sql.SQLException;
import java.time.Clock;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.luzvital.bo.GeradorAlertas.PlanoAlertas;
import br.com.luzvital.config.ConnectionFactory;
import br.com.luzvital.dao.AlertaDAO;
import br.com.luzvital.dao.EquipamentoDAO;
import br.com.luzvital.dao.InterrupcaoDAO;
import br.com.luzvital.dao.PacienteContatoDAO;
import br.com.luzvital.dao.PacienteDAO;
import br.com.luzvital.dao.PacienteEquipamentoDAO;
import br.com.luzvital.dao.RegiaoDAO;
import br.com.luzvital.dao.SqlErrorTranslator;
import br.com.luzvital.dto.ResultadoRegistroInterrupcao;
import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.model.Alerta;
import br.com.luzvital.model.Equipamento;
import br.com.luzvital.model.Interrupcao;
import br.com.luzvital.model.OrigemInterrupcao;
import br.com.luzvital.model.Paciente;
import br.com.luzvital.model.StatusInterrupcao;

/**
 * Regras de negócio de INTERRUPCAO.
 * Registrar uma interrupção cruza a região com os pacientes ativos e gera os alertas para os contatos,
 * tudo numa única transação: ou grava a interrupção com todos os alertas, ou não grava nada.
 */
@Service
public class InterrupcaoBO {

    private static final Logger log = LoggerFactory.getLogger(InterrupcaoBO.class);
    private static final int DURACAO_MAXIMA_MIN = 99_999; // NUMBER(5)
    /** Folga para relógios de clientes um pouco adiantados. */
    private static final int TOLERANCIA_RELOGIO_MIN = 5;

    private final ConnectionFactory connectionFactory;
    private final InterrupcaoDAO interrupcaoDAO;
    private final AlertaDAO alertaDAO;
    private final RegiaoDAO regiaoDAO;
    private final PacienteDAO pacienteDAO;
    private final PacienteEquipamentoDAO pacienteEquipamentoDAO;
    private final PacienteContatoDAO pacienteContatoDAO;
    private final EquipamentoDAO equipamentoDAO;
    private final Clock clock;

    @Autowired
    public InterrupcaoBO(ConnectionFactory connectionFactory, InterrupcaoDAO interrupcaoDAO, AlertaDAO alertaDAO,
            RegiaoDAO regiaoDAO, PacienteDAO pacienteDAO, PacienteEquipamentoDAO pacienteEquipamentoDAO,
            PacienteContatoDAO pacienteContatoDAO, EquipamentoDAO equipamentoDAO) {
        this(connectionFactory, interrupcaoDAO, alertaDAO, regiaoDAO, pacienteDAO, pacienteEquipamentoDAO,
                pacienteContatoDAO, equipamentoDAO, Clock.system(Fusos.BRASILIA));
    }

    InterrupcaoBO(ConnectionFactory connectionFactory, InterrupcaoDAO interrupcaoDAO, AlertaDAO alertaDAO,
            RegiaoDAO regiaoDAO, PacienteDAO pacienteDAO, PacienteEquipamentoDAO pacienteEquipamentoDAO,
            PacienteContatoDAO pacienteContatoDAO, EquipamentoDAO equipamentoDAO, Clock clock) {
        this.connectionFactory = connectionFactory;
        this.interrupcaoDAO = interrupcaoDAO;
        this.alertaDAO = alertaDAO;
        this.regiaoDAO = regiaoDAO;
        this.pacienteDAO = pacienteDAO;
        this.pacienteEquipamentoDAO = pacienteEquipamentoDAO;
        this.pacienteContatoDAO = pacienteContatoDAO;
        this.equipamentoDAO = equipamentoDAO;
        this.clock = clock;
    }

    public List<Interrupcao> listar() {
        return interrupcaoDAO.listar();
    }

    public Interrupcao buscarPorId(Long id) {
        return interrupcaoDAO.buscarPorId(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Interrupção não encontrada"));
    }

    /** Registra uma nova interrupção (sempre ABERTA) e gera os alertas para os pacientes ativos da região. */
    public ResultadoRegistroInterrupcao registrar(Interrupcao interrupcao) {
        validarENormalizar(interrupcao);
        Long idRegiao = interrupcao.getIdRegiao();

        // 1. Quem é afetado e com que equipamentos e contatos (leituras, fora da transação)
        List<Paciente> pacientes = pacienteDAO.listarAtivosPorRegiao(idRegiao);
        Map<Long, Equipamento> catalogo = equipamentoDAO.listar().stream()
                .collect(Collectors.toMap(Equipamento::getIdEquipamento, Function.identity()));
        PlanoAlertas plano = GeradorAlertas.planejar(
                pacientes,
                pacienteEquipamentoDAO.listarDePacientesAtivosDaRegiao(idRegiao),
                catalogo,
                pacienteContatoDAO.listarDePacientesAtivosDaRegiao(idRegiao),
                interrupcao.getDuracaoEstimadaMin());

        // 2. Grava a interrupção e os alertas numa única transação
        gravar(interrupcao, plano.alertas());

        log.info("Interrupção {} registrada na região {}: {} pacientes afetados, {} alertas, {} sem contato",
                interrupcao.getIdInterrupcao(), idRegiao, plano.pacientesAfetados(), plano.alertas().size(),
                plano.pacientesSemContato().size());

        return new ResultadoRegistroInterrupcao(
                interrupcao,
                plano.pacientesAfetados(),
                plano.alertas().size(),
                contarPorPrioridade(plano.alertas()),
                plano.pacientesSemContato(),
                plano.alertas());
    }

    private void gravar(Interrupcao interrupcao, List<Alerta> alertas) {
        try (Connection conn = connectionFactory.getConnection()) {
            conn.setAutoCommit(false);
            try {
                interrupcaoDAO.inserir(conn, interrupcao);
                for (Alerta alerta : alertas) {
                    alerta.setIdInterrupcao(interrupcao.getIdInterrupcao());
                    alertaDAO.inserir(conn, alerta);
                }
                conn.commit();
            } catch (SQLException | RuntimeException e) {
                conn.rollback();
                interrupcao.setIdInterrupcao(null);
                throw e;
            }
        } catch (SQLException e) {
            throw SqlErrorTranslator.traduzir(e, "registrar interrupção");
        }
    }

    void validarENormalizar(Interrupcao i) {
        if (i == null) {
            throw new ValidacaoException("Dados da interrupção não informados");
        }
        Validacoes.obrigatorio(i.getIdRegiao(), "idRegiao");
        Integer duracao = i.getDuracaoEstimadaMin();
        if (duracao != null && (duracao <= 0 || duracao > DURACAO_MAXIMA_MIN)) {
            throw new ValidacaoException("Campo 'duracaoEstimadaMin' deve estar entre 1 e " + DURACAO_MAXIMA_MIN);
        }
        if (regiaoDAO.buscarPorId(i.getIdRegiao()).isEmpty()) {
            throw new RecursoNaoEncontradoException("Região não encontrada");
        }

        LocalDateTime agora = LocalDateTime.now(clock).truncatedTo(ChronoUnit.SECONDS);
        if (i.getDataInicio() == null) {
            i.setDataInicio(agora);
        } else if (i.getDataInicio().isAfter(agora.plusMinutes(TOLERANCIA_RELOGIO_MIN))) {
            throw new ValidacaoException("Campo 'dataInicio' não pode estar no futuro");
        }
        if (i.getOrigem() == null) {
            i.setOrigem(OrigemInterrupcao.SIMULADA);
        }
        // Registro sempre abre a interrupção; encerrar é outra operação (PUT)
        i.setIdInterrupcao(null);
        i.setStatus(StatusInterrupcao.ABERTA);
        i.setDataFim(null);
    }

    static Map<Integer, Long> contarPorPrioridade(List<Alerta> alertas) {
        Map<Integer, Long> contagem = new LinkedHashMap<>();
        for (int p = RegraPrioridade.PRIORIDADE_ALTA; p <= RegraPrioridade.PRIORIDADE_BAIXA; p++) {
            contagem.put(p, 0L);
        }
        alertas.forEach(a -> contagem.merge(a.getPrioridade(), 1L, Long::sum));
        return contagem;
    }
}
