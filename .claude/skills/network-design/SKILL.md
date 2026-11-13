---
name: network-design
description: Use ao projetar, configurar ou documentar a rede da LuzVital no Cisco Packet Tracer — sub-redes, VLANs, endereçamento IP, DHCP, trunk 802.1Q, router-on-a-stick, NAT/PAT, DNS, HTTP, ACLs, SSH, Wi-Fi WPA2 e os testes exigidos.
---

# network-design

Apoia **Network Architect Solutions**. Requisitos mínimos em `docs/FIAP_REQUIREMENTS_CHECKLIST.md` (seção Network).

## Cenário
Local físico da LuzVital: base de atendimento/home care com três setores:
- **Equipe** (VLAN 10), **Cidadão / Wi-Fi público** (VLAN 20), **Servidores/Sensores** (VLAN 30).
- Faixa **192.168.X.0/24**, X = número da equipe (pergunte se não souber; não invente).

## Passos
1. **Endereçamento:** calcule as sub-redes (VLSM ou /26 iguais). Gere a tabela: VLAN, nome, rede, máscara, gateway, faixa DHCP, excluídos.
2. **Switching:** VLANs por setor, portas de acesso, trunk 802.1Q até o roteador.
3. **Roteamento:** router-on-a-stick com subinterfaces `encapsulation dot1Q`.
4. **Serviços:** DHCP com um pool por VLAN (excluindo gateway e servidor); servidor da solução com **DNS** e **HTTP** (página com a Ficha da CitizenTech).
5. **Internet:** NAT/PAT (overload) até um roteador "provedor" com servidor externo.
6. **Segurança:** ACL estendida no sentido certo (Wi-Fi do cidadão: só HTTP/DNS do servidor e internet; nada da VLAN Equipe); SSH v2 com `ip domain-name`, `crypto key`, usuário local, `transport input ssh`; `enable secret`; Wi-Fi WPA2-PSK.
7. **Documentação:** blocos de config prontos para colar, em `network/configs/`, e o plano em `network/README.md`.

## Regras
- Não marque requisito como atendido sem o teste correspondente no Packet Tracer.
- Senhas de exemplo nunca são reutilizadas fora do laboratório.

## Validação (prints obrigatórios no PDF)
- [ ] Ping entre VLANs.
- [ ] PC recebendo IP por DHCP.
- [ ] Página do servidor abrindo **pelo nome** (DNS).
- [ ] `show ip nat translations` com entradas.
- [ ] Um acesso **barrado pela ACL** (Wi-Fi do cidadão → VLAN Equipe).
- [ ] Trechos de `show running-config` no PDF.
