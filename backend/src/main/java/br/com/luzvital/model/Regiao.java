package br.com.luzvital.model;

/** Tabela REGIAO: bairro ou área usada para cruzar a interrupção com os pacientes. */
public class Regiao {

    private Long idRegiao;
    private String nome;
    private String cidade;
    private String uf;

    public Regiao() {
    }

    public Regiao(Long idRegiao, String nome, String cidade, String uf) {
        this.idRegiao = idRegiao;
        this.nome = nome;
        this.cidade = cidade;
        this.uf = uf;
    }

    public Long getIdRegiao() {
        return idRegiao;
    }

    public void setIdRegiao(Long idRegiao) {
        this.idRegiao = idRegiao;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getCidade() {
        return cidade;
    }

    public void setCidade(String cidade) {
        this.cidade = cidade;
    }

    public String getUf() {
        return uf;
    }

    public void setUf(String uf) {
        this.uf = uf;
    }
}
