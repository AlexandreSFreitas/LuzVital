package br.com.luzvital.model;

import java.time.LocalDateTime;

/** Tabela INTERRUPCAO: falta de energia numa região (no MVP, simulada). */
public class Interrupcao {

    private Long idInterrupcao;
    private Long idRegiao;
    private LocalDateTime dataInicio;
    /** Null enquanto ABERTA. */
    private LocalDateTime dataFim;
    /** Null = duração desconhecida. */
    private Integer duracaoEstimadaMin;
    private OrigemInterrupcao origem;
    private StatusInterrupcao status;

    public Interrupcao() {
    }

    public Long getIdInterrupcao() {
        return idInterrupcao;
    }

    public void setIdInterrupcao(Long idInterrupcao) {
        this.idInterrupcao = idInterrupcao;
    }

    public Long getIdRegiao() {
        return idRegiao;
    }

    public void setIdRegiao(Long idRegiao) {
        this.idRegiao = idRegiao;
    }

    public LocalDateTime getDataInicio() {
        return dataInicio;
    }

    public void setDataInicio(LocalDateTime dataInicio) {
        this.dataInicio = dataInicio;
    }

    public LocalDateTime getDataFim() {
        return dataFim;
    }

    public void setDataFim(LocalDateTime dataFim) {
        this.dataFim = dataFim;
    }

    public Integer getDuracaoEstimadaMin() {
        return duracaoEstimadaMin;
    }

    public void setDuracaoEstimadaMin(Integer duracaoEstimadaMin) {
        this.duracaoEstimadaMin = duracaoEstimadaMin;
    }

    public OrigemInterrupcao getOrigem() {
        return origem;
    }

    public void setOrigem(OrigemInterrupcao origem) {
        this.origem = origem;
    }

    public StatusInterrupcao getStatus() {
        return status;
    }

    public void setStatus(StatusInterrupcao status) {
        this.status = status;
    }
}
