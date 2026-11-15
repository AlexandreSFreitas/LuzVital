package br.com.luzvital.model;

/** Tabela PACIENTE_CONTATO: rede de apoio do paciente, com a ordem de acionamento (PK composta). */
public class PacienteContato {

    private Long idPaciente;
    private Long idContato;
    /** 1 = acionar primeiro. */
    private int ordemAcionamento;
    private String vinculo;

    public PacienteContato() {
    }

    public PacienteContato(Long idPaciente, Long idContato, int ordemAcionamento, String vinculo) {
        this.idPaciente = idPaciente;
        this.idContato = idContato;
        this.ordemAcionamento = ordemAcionamento;
        this.vinculo = vinculo;
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

    public int getOrdemAcionamento() {
        return ordemAcionamento;
    }

    public void setOrdemAcionamento(int ordemAcionamento) {
        this.ordemAcionamento = ordemAcionamento;
    }

    public String getVinculo() {
        return vinculo;
    }

    public void setVinculo(String vinculo) {
        this.vinculo = vinculo;
    }
}
