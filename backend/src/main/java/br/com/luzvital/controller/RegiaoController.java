package br.com.luzvital.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.luzvital.bo.RegiaoBO;
import br.com.luzvital.model.Regiao;

@RestController
@RequestMapping("/api/regioes")
public class RegiaoController {

    private final RegiaoBO regiaoBO;

    public RegiaoController(RegiaoBO regiaoBO) {
        this.regiaoBO = regiaoBO;
    }

    @GetMapping
    public List<Regiao> listar() {
        return regiaoBO.listar();
    }

    @GetMapping("/{id}")
    public Regiao buscar(@PathVariable Long id) {
        return regiaoBO.buscarPorId(id);
    }

    @PostMapping
    public ResponseEntity<Regiao> criar(@RequestBody Regiao regiao) {
        Regiao criada = regiaoBO.criar(regiao);
        return ResponseEntity.created(URI.create("/api/regioes/" + criada.getIdRegiao())).body(criada);
    }

    @PutMapping("/{id}")
    public Regiao atualizar(@PathVariable Long id, @RequestBody Regiao regiao) {
        return regiaoBO.atualizar(id, regiao);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> remover(@PathVariable Long id) {
        regiaoBO.remover(id);
        return ResponseEntity.noContent().build();
    }
}
