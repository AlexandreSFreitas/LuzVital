package br.com.luzvital.model;

import java.time.LocalDate;
import java.time.LocalDateTime;

/** Tabela PACIENTE: paciente eletrodependente (somente dados fictícios), com o endereço. */
public class Paciente {

    private Long idPaciente;
    private String nome;
    private LocalDate dataNascimento;
    private String logradouro;
    private String numero;
    private String complemento;
    private String cep;
    private Long idRegiao;
    private String observacaoAtendimento;
    /** No banco é CHAR(1) 'S'/'N'. Null na entrada significa "manter" (PUT) ou "S" (POST). */
    private Boolean ativo;
    /** Preenchido pelo banco (DEFAULT SYSTIMESTAMP); ignorado na entrada. */
    private LocalDateTime dataCadastro;

    public Paciente() {
    }

    public Long getIdPaciente() {
        return idPaciente;
    }

    public void setIdPaciente(Long idPaciente) {
        this.idPaciente = idPaciente;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public LocalDate getDataNascimento() {
        return dataNascimento;
    }

    public void setDataNascimento(LocalDate dataNascimento) {
        this.dataNascimento = dataNascimento;
    }

    public String getLogradouro() {
        return logradouro;
    }

    public void setLogradouro(String logradouro) {
        this.logradouro = logradouro;
    }

    public String getNumero() {
        return numero;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }

    public String getComplemento() {
        return complemento;
    }

    public void setComplemento(String complemento) {
        this.complemento = complemento;
    }

    public String getCep() {
        return cep;
    }

    public void setCep(String cep) {
        this.cep = cep;
    }

    public Long getIdRegiao() {
        return idRegiao;
    }

    public void setIdRegiao(Long idRegiao) {
        this.idRegiao = idRegiao;
    }

    public String getObservacaoAtendimento() {
        return observacaoAtendimento;
    }

    public void setObservacaoAtendimento(String observacaoAtendimento) {
        this.observacaoAtendimento = observacaoAtendimento;
    }

    public Boolean getAtivo() {
        return ativo;
    }

    public void setAtivo(Boolean ativo) {
        this.ativo = ativo;
    }

    public LocalDateTime getDataCadastro() {
        return dataCadastro;
    }

    public void setDataCadastro(LocalDateTime dataCadastro) {
        this.dataCadastro = dataCadastro;
    }
}
