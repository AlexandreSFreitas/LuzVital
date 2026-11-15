package br.com.luzvital.model;

/** Tabela EQUIPAMENTO: catálogo de tipos de equipamento médico e o consumo de cada um. */
public class Equipamento {

    private Long idEquipamento;
    private String nome;
    private CategoriaEquipamento categoria;
    private Integer consumoWatts;
    /** CHAR(1) 'S'/'N' no banco. Informação de cadastro ou fabricante, não é avaliação clínica. */
    private boolean suporteVida;

    public Equipamento() {
    }

    public Equipamento(Long idEquipamento, String nome, CategoriaEquipamento categoria, Integer consumoWatts,
            boolean suporteVida) {
        this.idEquipamento = idEquipamento;
        this.nome = nome;
        this.categoria = categoria;
        this.consumoWatts = consumoWatts;
        this.suporteVida = suporteVida;
    }

    public Long getIdEquipamento() {
        return idEquipamento;
    }

    public void setIdEquipamento(Long idEquipamento) {
        this.idEquipamento = idEquipamento;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public CategoriaEquipamento getCategoria() {
        return categoria;
    }

    public void setCategoria(CategoriaEquipamento categoria) {
        this.categoria = categoria;
    }

    public Integer getConsumoWatts() {
        return consumoWatts;
    }

    public void setConsumoWatts(Integer consumoWatts) {
        this.consumoWatts = consumoWatts;
    }

    public boolean isSuporteVida() {
        return suporteVida;
    }

    public void setSuporteVida(boolean suporteVida) {
        this.suporteVida = suporteVida;
    }
}
