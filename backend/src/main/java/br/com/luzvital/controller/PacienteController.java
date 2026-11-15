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

import br.com.luzvital.bo.PacienteBO;
import br.com.luzvital.model.Paciente;

@RestController
@RequestMapping("/api/pacientes")
public class PacienteController {

    private final PacienteBO pacienteBO;

    public PacienteController(PacienteBO pacienteBO) {
        this.pacienteBO = pacienteBO;
    }

    @GetMapping
    public List<Paciente> listar() {
        return pacienteBO.listar();
    }

    @GetMapping("/{id}")
    public Paciente buscar(@PathVariable Long id) {
        return pacienteBO.buscarPorId(id);
    }

    @PostMapping
    public ResponseEntity<Paciente> criar(@RequestBody Paciente paciente) {
        Paciente criado = pacienteBO.criar(paciente);
        return ResponseEntity.created(URI.create("/api/pacientes/" + criado.getIdPaciente())).body(criado);
    }

    @PutMapping("/{id}")
    public Paciente atualizar(@PathVariable Long id, @RequestBody Paciente paciente) {
        return pacienteBO.atualizar(id, paciente);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> remover(@PathVariable Long id) {
        pacienteBO.remover(id);
        return ResponseEntity.noContent().build();
    }
}
