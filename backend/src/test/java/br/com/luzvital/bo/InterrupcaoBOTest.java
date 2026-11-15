package br.com.luzvital.bo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.fakes.FakeRegiaoDAO;
import br.com.luzvital.model.Alerta;
import br.com.luzvital.model.Interrupcao;
import br.com.luzvital.model.OrigemInterrupcao;
import br.com.luzvital.model.Regiao;
import br.com.luzvital.model.StatusInterrupcao;

/** Testa as regras de entrada do registro. A gravação transacional é conferida contra o Oracle (README). */
class InterrupcaoBOTest {

    private static final Clock AGORA = Clock.fixed(Instant.parse("2026-11-14T15:00:00Z"), ZoneId.of("America/Sao_Paulo"));

    private final InterrupcaoBO bo = new InterrupcaoBO(null, null, null,
            new FakeRegiaoDAO().com(new Regiao(1L, "Vila Mariana", "São Paulo", "SP")),
            null, null, null, null, AGORA);

    private static Interrupcao nova(Long idRegiao, Integer duracao) {
        Interrupcao i = new Interrupcao();
        i.setIdRegiao(idRegiao);
        i.setDuracaoEstimadaMin(duracao);
        return i;
    }

    @Test
    void preencheValoresPadraoEForcaStatusAberta() {
        Interrupcao i = nova(1L, 120);
        i.setStatus(StatusInterrupcao.ENCERRADA);
        i.setDataFim(LocalDateTime.of(2026, 11, 14, 13, 0));

        bo.validarENormalizar(i);

        assertEquals(StatusInterrupcao.ABERTA, i.getStatus());
        assertNull(i.getDataFim());
        assertEquals(OrigemInterrupcao.SIMULADA, i.getOrigem());
        assertEquals(LocalDateTime.of(2026, 11, 14, 12, 0), i.getDataInicio()); // 15h UTC = 12h em São Paulo
    }

    @Test
    void duracaoDesconhecidaEhPermitida() {
        Interrupcao i = nova(1L, null);
        bo.validarENormalizar(i);
        assertNull(i.getDuracaoEstimadaMin());
    }

    @Test
    void rejeitaDuracaoForaDoIntervalo() {
        assertThrows(ValidacaoException.class, () -> bo.validarENormalizar(nova(1L, 0)));
        assertThrows(ValidacaoException.class, () -> bo.validarENormalizar(nova(1L, 100_000)));
    }

    @Test
    void rejeitaInicioNoFuturoAlemDaTolerancia() {
        Interrupcao i = nova(1L, 60);
        i.setDataInicio(LocalDateTime.of(2026, 11, 14, 12, 30));
        assertThrows(ValidacaoException.class, () -> bo.validarENormalizar(i));
    }

    @Test
    void regiaoObrigatoriaEExistente() {
        assertThrows(ValidacaoException.class, () -> bo.validarENormalizar(nova(null, 60)));
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.validarENormalizar(nova(99L, 60)));
    }

    @Test
    void contagemPorPrioridadeTrazAsTresFaixas() {
        Map<Integer, Long> contagem = InterrupcaoBO.contarPorPrioridade(
                List.of(new Alerta(1L, 1L, 1), new Alerta(1L, 2L, 1), new Alerta(2L, 3L, 3)));
        assertEquals(Map.of(1, 2L, 2, 0L, 3, 1L), contagem);
    }
}
