package br.com.luzvital.bo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;

import org.junit.jupiter.api.Test;

import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.fakes.FakePacienteDAO;
import br.com.luzvital.fakes.FakeRegiaoDAO;
import br.com.luzvital.model.Paciente;
import br.com.luzvital.model.Regiao;

class PacienteBOTest {

    private static final Clock HOJE = Clock.fixed(Instant.parse("2026-11-14T12:00:00Z"), ZoneId.of("America/Sao_Paulo"));

    private final FakePacienteDAO pacienteDAO = new FakePacienteDAO();
    private final FakeRegiaoDAO regiaoDAO = new FakeRegiaoDAO().com(new Regiao(1L, "Vila Mariana", "São Paulo", "SP"));
    private final PacienteBO bo = new PacienteBO(pacienteDAO, regiaoDAO, HOJE);

    /** Paciente fictício válido. */
    private static Paciente valido() {
        Paciente p = new Paciente();
        p.setNome("Maria Fictícia");
        p.setDataNascimento(LocalDate.of(1950, 3, 10));
        p.setLogradouro("Rua Exemplo");
        p.setNumero("100");
        p.setCep("04101-000");
        p.setIdRegiao(1L);
        return p;
    }

    @Test
    void criaPacienteAtivoPorPadraoComCepSoDigitos() {
        Paciente criado = bo.criar(valido());

        assertEquals(1L, criado.getIdPaciente());
        assertEquals("04101000", criado.getCep());
        assertTrue(criado.getAtivo());
    }

    @Test
    void complementoEmBrancoViraNulo() {
        Paciente p = valido();
        p.setComplemento("   ");
        assertNull(bo.criar(p).getComplemento());
    }

    @Test
    void rejeitaCepInvalido() {
        Paciente p = valido();
        p.setCep("1234-567");
        assertThrows(ValidacaoException.class, () -> bo.criar(p));
    }

    @Test
    void rejeitaNascimentoNoFuturo() {
        Paciente p = valido();
        p.setDataNascimento(LocalDate.of(2026, 11, 15));
        assertThrows(ValidacaoException.class, () -> bo.criar(p));
    }

    @Test
    void rejeitaNomeMaiorQueAColuna() {
        Paciente p = valido();
        p.setNome("x".repeat(121));
        assertThrows(ValidacaoException.class, () -> bo.criar(p));
    }

    @Test
    void regiaoInexistenteDa404() {
        Paciente p = valido();
        p.setIdRegiao(99L);
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.criar(p));
    }

    @Test
    void atualizarSemAtivoMantemOValorAtual() {
        Paciente criado = bo.criar(valido());
        Paciente desativar = valido();
        desativar.setAtivo(false);
        bo.atualizar(criado.getIdPaciente(), desativar);

        Paciente semAtivo = valido();
        Paciente atualizado = bo.atualizar(criado.getIdPaciente(), semAtivo);

        assertFalse(atualizado.getAtivo());
        assertEquals(criado.getDataCadastro(), atualizado.getDataCadastro());
    }

    @Test
    void atualizarOuRemoverInexistenteDa404() {
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.atualizar(42L, valido()));
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.remover(42L));
    }
}
