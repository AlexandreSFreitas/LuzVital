package br.com.luzvital.model;

/** Tabela PACIENTE_EQUIPAMENTO: unidade de equipamento que o paciente usa, com a autonomia da bateria. */
public class PacienteEquipamento {

    private Long idPacienteEquipamento;
    private Long idPaciente;
    private Long idEquipamento;
    /** Minutos de bateria da unidade; 0 = sem bateria. */
    private int autonomiaBateriaMin;
    private String fonteAlternativa;

    public PacienteEquipamento() {
    }

    public PacienteEquipamento(Long idPacienteEquipamento, Long idPaciente, Long idEquipamento,
            int autonomiaBateriaMin, String fonteAlternativa) {
        this.idPacienteEquipamento = idPacienteEquipamento;
        this.idPaciente = idPaciente;
        this.idEquipamento = idEquipamento;
        this.autonomiaBateriaMin = autonomiaBateriaMin;
        this.fonteAlternativa = fonteAlternativa;
    }

    public Long getIdPacienteEquipamento() {
        return idPacienteEquipamento;
    }

    public void setIdPacienteEquipamento(Long idPacienteEquipamento) {
        this.idPacienteEquipamento = idPacienteEquipamento;
    }

    public Long getIdPaciente() {
        return idPaciente;
    }

    public void setIdPaciente(Long idPaciente) {
        this.idPaciente = idPaciente;
    }

    public Long getIdEquipamento() {
        return idEquipamento;
    }

    public void setIdEquipamento(Long idEquipamento) {
        this.idEquipamento = idEquipamento;
    }

    public int getAutonomiaBateriaMin() {
        return autonomiaBateriaMin;
    }

    public void setAutonomiaBateriaMin(int autonomiaBateriaMin) {
        this.autonomiaBateriaMin = autonomiaBateriaMin;
    }

    public String getFonteAlternativa() {
        return fonteAlternativa;
    }

    public void setFonteAlternativa(String fonteAlternativa) {
        this.fonteAlternativa = fonteAlternativa;
    }
}
