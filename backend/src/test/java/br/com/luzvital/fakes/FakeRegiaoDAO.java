package br.com.luzvital.fakes;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

import br.com.luzvital.dao.RegiaoDAO;
import br.com.luzvital.model.Regiao;

/** RegiaoDAO em memória, para testar BO e controller sem Oracle. */
public class FakeRegiaoDAO extends RegiaoDAO {

    private final Map<Long, Regiao> dados = new TreeMap<>();
    private long proximoId = 1;

    public FakeRegiaoDAO() {
        super(null);
    }

    public FakeRegiaoDAO com(Regiao regiao) {
        dados.put(regiao.getIdRegiao(), regiao);
        proximoId = Math.max(proximoId, regiao.getIdRegiao() + 1);
        return this;
    }

    @Override
    public List<Regiao> listar() {
        return new ArrayList<>(dados.values());
    }

    @Override
    public Optional<Regiao> buscarPorId(Long id) {
        return Optional.ofNullable(dados.get(id));
    }

    @Override
    public Regiao inserir(Regiao regiao) {
        regiao.setIdRegiao(proximoId++);
        dados.put(regiao.getIdRegiao(), regiao);
        return regiao;
    }

    @Override
    public boolean atualizar(Regiao regiao) {
        if (!dados.containsKey(regiao.getIdRegiao())) {
            return false;
        }
        dados.put(regiao.getIdRegiao(), regiao);
        return true;
    }

    @Override
    public boolean remover(Long id) {
        return dados.remove(id) != null;
    }
}
