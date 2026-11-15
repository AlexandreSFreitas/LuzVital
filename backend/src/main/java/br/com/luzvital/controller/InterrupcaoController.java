package br.com.luzvital.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.luzvital.bo.InterrupcaoBO;
import br.com.luzvital.dto.ResultadoRegistroInterrupcao;
import br.com.luzvital.model.Interrupcao;

@RestController
@RequestMapping("/api/interrupcoes")
public class InterrupcaoController {

    private final InterrupcaoBO interrupcaoBO;

    public InterrupcaoController(InterrupcaoBO interrupcaoBO) {
        this.interrupcaoBO = interrupcaoBO;
    }

    @GetMapping
    public List<Interrupcao> listar() {
        return interrupcaoBO.listar();
    }

    @GetMapping("/{id}")
    public Interrupcao buscar(@PathVariable Long id) {
        return interrupcaoBO.buscarPorId(id);
    }

    /** Registra a interrupção e gera os alertas. Corpo: idRegiao (obrigatório), duracaoEstimadaMin, dataInicio, origem. */
    @PostMapping
    public ResponseEntity<ResultadoRegistroInterrupcao> registrar(@RequestBody Interrupcao interrupcao) {
        ResultadoRegistroInterrupcao resultado = interrupcaoBO.registrar(interrupcao);
        URI local = URI.create("/api/interrupcoes/" + resultado.interrupcao().getIdInterrupcao());
        return ResponseEntity.created(local).body(resultado);
    }
}
