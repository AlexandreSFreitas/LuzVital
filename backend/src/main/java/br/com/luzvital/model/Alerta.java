package br.com.luzvital.model;

import java.time.LocalDateTime;

/** Tabela ALERTA: aviso para um contato de um paciente afetado por uma interrupção, com a confirmação. */
public class Alerta {

    private Long idAlerta;
    private Long idInterrupcao;
    private Long idPaciente;
    private Long idContato;
    /** 1 a 3, regra operacional acadêmica (não é índice clínico). */
    private int prioridade;
    private StatusAlerta status;
    private LocalDateTime dataCriacao;
    private LocalDateTime dataConfirmacao;

    public Alerta() {
    }

    public Alerta(Long idPaciente, Long idContato, int prioridade) {
        this.idPaciente = idPaciente;
        this.idContato = idContato;
        this.prioridade = prioridade;
        this.status = StatusAlerta.PENDENTE;
    }

    public Long getIdAlerta() {
        return idAlerta;
    }

    public void setIdAlerta(Long idAlerta) {
        this.idAlerta = idAlerta;
    }

    public Long getIdInterrupcao() {
        return idInterrupcao;
    }

    public void setIdInterrupcao(Long idInterrupcao) {
        this.idInterrupcao = idInterrupcao;
    }

    public Long getIdPaciente() {
        return idPaciente;
    }

    public void setIdPaciente(Long idPaciente) {
        this.idPaciente = idPaciente;
    }

    public Long getIdContato() {
        return idContato;
    }

    public void setIdContato(Long idContato) {
        this.idContato = idContato;
    }

    public int getPrioridade() {
        return prioridade;
    }

    public void setPrioridade(int prioridade) {
        this.prioridade = prioridade;
    }

    public StatusAlerta getStatus() {
        return status;
    }

    public void setStatus(StatusAlerta status) {
        this.status = status;
    }

    public LocalDateTime getDataCriacao() {
        return dataCriacao;
    }

    public void setDataCriacao(LocalDateTime dataCriacao) {
        this.dataCriacao = dataCriacao;
    }

    public LocalDateTime getDataConfirmacao() {
        return dataConfirmacao;
    }

    public void setDataConfirmacao(LocalDateTime dataConfirmacao) {
        this.dataConfirmacao = dataConfirmacao;
    }
}
