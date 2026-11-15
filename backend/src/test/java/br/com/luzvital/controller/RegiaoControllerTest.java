package br.com.luzvital.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import br.com.luzvital.bo.RegiaoBO;
import br.com.luzvital.exception.GlobalExceptionHandler;
import br.com.luzvital.fakes.FakeRegiaoDAO;
import br.com.luzvital.model.Regiao;

/** Controller + handler de exceções, sem subir o Spring inteiro e sem banco. */
class RegiaoControllerTest {

    private MockMvc mvc;

    @BeforeEach
    void setUp() {
        FakeRegiaoDAO dao = new FakeRegiaoDAO().com(new Regiao(1L, "Vila Mariana", "São Paulo", "SP"));
        mvc = MockMvcBuilders.standaloneSetup(new RegiaoController(new RegiaoBO(dao)))
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
    }

    @Test
    void getPorIdDevolveJsonEmCamelCase() throws Exception {
        mvc.perform(get("/api/regioes/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.idRegiao").value(1))
                .andExpect(jsonPath("$.nome").value("Vila Mariana"));
    }

    @Test
    void postDevolve201ComLocation() throws Exception {
        mvc.perform(post("/api/regioes").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"nome\":\"Mooca\",\"cidade\":\"São Paulo\",\"uf\":\"sp\"}"))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/api/regioes/2"))
                .andExpect(jsonPath("$.uf").value("SP"));
    }

    @Test
    void naoEncontradoDevolve404NoFormatoPadrao() throws Exception {
        mvc.perform(get("/api/regioes/99"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.erro").value("Região não encontrada"))
                .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    void validacaoDevolve400() throws Exception {
        mvc.perform(post("/api/regioes").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"nome\":\"Mooca\",\"cidade\":\"São Paulo\"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.erro").value("Campo 'uf' é obrigatório"));
    }

    @Test
    void jsonMalformadoDevolve400() throws Exception {
        mvc.perform(post("/api/regioes").contentType(MediaType.APPLICATION_JSON).content("{nome:"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400));
    }

    @Test
    void idNaoNumericoDevolve400() throws Exception {
        mvc.perform(get("/api/regioes/abc")).andExpect(status().isBadRequest());
    }

    @Test
    void deleteDevolve204() throws Exception {
        mvc.perform(delete("/api/regioes/1")).andExpect(status().isNoContent());
    }
}
