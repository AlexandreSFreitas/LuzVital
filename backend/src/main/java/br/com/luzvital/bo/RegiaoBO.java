package br.com.luzvital.bo;

import java.util.List;
import java.util.Locale;

import org.springframework.stereotype.Service;

import br.com.luzvital.dao.RegiaoDAO;
import br.com.luzvital.exception.RecursoNaoEncontradoException;
import br.com.luzvital.exception.ValidacaoException;
import br.com.luzvital.model.Regiao;

/** Regras de negócio de REGIAO. */
@Service
public class RegiaoBO {

    private final RegiaoDAO regiaoDAO;

    public RegiaoBO(RegiaoDAO regiaoDAO) {
        this.regiaoDAO = regiaoDAO;
    }

    public List<Regiao> listar() {
        return regiaoDAO.listar();
    }

    public Regiao buscarPorId(Long id) {
        return regiaoDAO.buscarPorId(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Região não encontrada"));
    }

    public Regiao criar(Regiao regiao) {
        validarENormalizar(regiao);
        regiao.setIdRegiao(null);
        return regiaoDAO.inserir(regiao);
    }

    public Regiao atualizar(Long id, Regiao regiao) {
        validarENormalizar(regiao);
        regiao.setIdRegiao(id);
        if (!regiaoDAO.atualizar(regiao)) {
            throw new RecursoNaoEncontradoException("Região não encontrada");
        }
        return regiao;
    }

    public void remover(Long id) {
        if (!regiaoDAO.remover(id)) {
            throw new RecursoNaoEncontradoException("Região não encontrada");
        }
    }

    void validarENormalizar(Regiao regiao) {
        if (regiao == null) {
            throw new ValidacaoException("Dados da região não informados");
        }
        regiao.setNome(Validacoes.obrigatorio(regiao.getNome(), "nome", 80));
        regiao.setCidade(Validacoes.obrigatorio(regiao.getCidade(), "cidade", 80));
        String uf = Validacoes.obrigatorio(regiao.getUf(), "uf", 2).toUpperCase(Locale.ROOT);
        if (!uf.matches("[A-Z]{2}")) {
            throw new ValidacaoException("Campo 'uf' deve ter 2 letras (ex.: SP)");
        }
        regiao.setUf(uf);
    }
}
