package br.com.luzvital.bo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.fakes.FakeRegiaoDAO;
import br.com.luzvital.model.Regiao;

class RegiaoBOTest {

    private final FakeRegiaoDAO dao = new FakeRegiaoDAO();
    private final RegiaoBO bo = new RegiaoBO(dao);

    @Test
    void criaRegiaoNormalizandoEspacosEUf() {
        Regiao criada = bo.criar(new Regiao(99L, "  Vila Mariana ", "São Paulo", "sp"));

        assertEquals(1L, criada.getIdRegiao()); // ID enviado pelo cliente é ignorado
        assertEquals("Vila Mariana", criada.getNome());
        assertEquals("SP", criada.getUf());
    }

    @Test
    void rejeitaCamposObrigatoriosVazios() {
        ValidacaoException e = assertThrows(ValidacaoException.class,
                () -> bo.criar(new Regiao(null, " ", "São Paulo", "SP")));
        assertEquals("Campo 'nome' é obrigatório", e.getMessage());
    }

    @Test
    void rejeitaUfInvalida() {
        assertThrows(ValidacaoException.class, () -> bo.criar(new Regiao(null, "Centro", "São Paulo", "S1")));
        assertThrows(ValidacaoException.class, () -> bo.criar(new Regiao(null, "Centro", "São Paulo", "SPX")));
    }

    @Test
    void atualizarOuRemoverInexistenteDa404() {
        assertThrows(RecursoNaoEncontradoException.class,
                () -> bo.atualizar(42L, new Regiao(null, "Centro", "São Paulo", "SP")));
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.remover(42L));
        assertThrows(RecursoNaoEncontradoException.class, () -> bo.buscarPorId(42L));
    }
}
