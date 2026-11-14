# Ambientes e versões

## Máquinas virtuais — 13/11/2026

| Componente | Versão observada | Função |
|---|---|---|
| Windows 10 Pro | 10.0.19045, 64 bits | Hospedeiro e clientes de teste |
| VirtualBox | 7.2.22r175245 | Virtualização e rede Host-only |
| Kali Linux | 2026.3, imagem VirtualBox AMD64 | Ambiente de ferramentas |
| Medusa | 2.3 | Duas verificações individuais de FTP no Kali |
| Metasploitable 2 | Kernel Linux 2.6.24-16-server | Alvo vulnerável |
| DVWA na VM | 1.0.7 | Formulário web |
| FTP | Banner vsFTPd 2.3.4 | Serviço observado |
| Samba | 3.0.20-Debian | Autenticação SMB |
| Clientes no hospedeiro | Python 3.11 e Impacket 0.13.1 | HTTP, FTP e SMB |

Na rede 192.168.56.0/24, o Kali recebeu 192.168.56.102 e o Metasploitable, 192.168.56.101. Os endereços foram atribuídos por DHCP e podem mudar. O Kali usou temporariamente 384 MB durante os testes; depois, sua configuração foi devolvida a 2.048 MB. Essa restrição limita conclusões sobre desempenho.

O Metasploitable 2 é uma [VM Ubuntu intencionalmente vulnerável da Rapid7](https://help.rapid7.com/metasploit/Content/getting-started/setting-up-test-env.html); a versão exata do Ubuntu não foi coletada. Metasploit Framework não foi usado neste projeto.

### Preparação das VMs

1. Crie uma rede Host-only no VirtualBox e mantenha apenas esse adaptador nas duas VMs, sem NAT ou Bridged.
2. Desative pastas compartilhadas, área de transferência e arrastar e soltar na VM vulnerável.
3. Confira os endereços e as rotas dentro das VMs. Use `ip -4 addr` e `ip route`; no sistema antigo, `ifconfig` e `route -n`.
4. Verifique a comunicação entre as VMs e a ausência de rota externa utilizável. Uma falha isolada de ping não comprova isolamento.
5. Crie snapshots antes dos exercícios e use somente contas fictícias. Desligue as VMs ao encerrar.

As verificações efetivamente realizadas estão no [relatório das VMs](relatorio.md). Para configuração do hipervisor, consulte a [documentação do VirtualBox](https://www.virtualbox.org/manual/).

## Containers — 14/11/2026

Docker CLI e Engine **29.2.1**, Compose **v5.0.2**.

| Serviço | Imagem configurada | Observação em execução |
|---|---|---|
| `dvwa` | `ghcr.io/digininja/dvwa:latest` | Debian 13 (trixie), PHP 8.5.11; aplicação identificada pelo digest |
| `db` | `mariadb:10.11` | Ubuntu 22.04.5 LTS, MariaDB 10.11.19 |
| `web` | `nginx:stable-alpine` | Nginx 1.30.6; acesso local em 127.0.0.1:4280 |
| `kali` | `kalilinux/kali-rolling:latest`, com Dockerfile local | Perfil opcional, não usado nos testes web |

A [imagem oficial do Kali](https://www.kali.org/docs/containers/official-kalilinux-docker-images/) recebe Medusa, Python e ferramentas auxiliares pelo [Dockerfile](../docker/kali/Dockerfile). Containers compartilham o kernel do mecanismo Docker; não reproduzem o kernel antigo do Metasploitable.

As tags podem mudar. Os digests das três imagens executadas estão em [testes-docker.json](evidencias/testes-docker.json) e identificam o ambiente observado. O DVWA desse container não deve ser confundido com a versão 1.0.7 da VM.
