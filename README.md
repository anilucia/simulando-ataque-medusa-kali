# Auditoria defensiva de autenticação: Kali Linux e Medusa

Laboratório de estudo sobre tentativas repetidas de login em FTP, DVWA e SMB, com evidências sanitizadas e recomendações de mitigação.

O projeto utiliza a adaptação permitida pelo desafio da DIO: compara respostas e controles de autenticação com contas fictícias e credenciais conhecidas. O Medusa foi usado em verificações individuais de FTP no Kali; os testes web usaram um cliente HTTP Python. Não houve descoberta de senhas desconhecidas, uso de wordlists ou enumeração de usuários.

## Documentação

- [Ambientes, distribuições e preparação das VMs](docs/ambientes.md)
- [Como executar o laboratório Docker](docs/laboratorio-docker.md)
- [Relatório de FTP, DVWA e SMB nas VMs](docs/relatorio.md)
- [Relatório da comparação web no Docker](docs/relatorio-docker.md)

## Ambientes utilizados

| Etapa | Configuração | Data dos testes |
|---|---|---|
| Máquinas virtuais | Kali Linux e Metasploitable 2 no VirtualBox, somente em rede Host-only | 13/11/2026 |
| Containers | DVWA e MariaDB em rede interna, com acesso local por proxy Nginx | 14/11/2026 |

O Docker também inclui um perfil opcional de Kali com Medusa, que não foi usado na comparação web. A versão do DVWA instalada na VM é diferente da imagem Docker; os resultados são apresentados separadamente.

Com os containers ligados, o DVWA fica acessível em **http://127.0.0.1:4280/**. Os comandos de inicialização e encerramento estão no [guia Docker](docs/laboratorio-docker.md).

## Resultados

| Cenário | Observação principal | Evidência |
|---|---|---|
| FTP | Pelo hospedeiro: três falhas e um sucesso. Pelo Medusa no Kali: uma falha e um sucesso | [VMs](docs/relatorio.md#ftp) |
| DVWA 1.0.7 na VM | Duas falhas e um sucesso em cada nível; High apresentou espera próxima de três segundos nas falhas | [VMs](docs/relatorio.md#dvwa) |
| SMB | Mesma senha inválida rejeitada em duas contas fictícias; política consultada com limiar de bloqueio zero | [VMs](docs/relatorio.md#smb) |
| DVWA no Docker | Low aceitou a senha válida após duas falhas; Impossible recusou a senha válida após três falhas | [Docker](docs/relatorio-docker.md) |

As medições e os eventos estão em [observacoes.json](docs/evidencias/observacoes.json) e [testes-docker.json](docs/evidencias/testes-docker.json). As amostras são pequenas e não constituem teste de carga nem auditoria completa de segurança.

## Medidas de mitigação

| Risco | Medidas recomendadas |
|---|---|
| Tentativas repetidas | Limitar por conta e origem, aplicar atrasos progressivos e bloqueios temporários calibrados |
| Tentativas distribuídas entre contas | Correlacionar falhas de várias contas e emitir alertas |
| Credenciais em URLs e registros | Usar POST, proteger o transporte e excluir senhas, cookies e tokens dos logs |
| Credenciais fracas | Adotar senhas longas e únicas, bloquear senhas comprometidas e usar MFA quando suportado |
| Serviços e protocolos antigos | Atualizar os serviços, revisar SMB1 e substituir FTP sem criptografia por uma alternativa protegida |
| Exposição desnecessária | Restringir acesso por firewall, desativar contas e serviços sem uso e manter o laboratório isolado |

O bloqueio do nível Impossible e o formato de log do proxy foram observados em execução. As demais medidas são recomendações; não foram todas implantadas ou retestadas. Bloqueios também podem ser usados para causar indisponibilidade de contas e precisam ser calibrados.

## Aprendizados

Rejeitar uma senha incorreta não demonstra, por si só, proteção contra tentativas repetidas. A comparação entre Low e Impossible mostrou o efeito do bloqueio por conta, enquanto os registros do DVWA revelaram a exposição de credenciais nos parâmetros da URL. No SMB, a consulta da política e a observação das respostas complementaram a análise dos eventos.

## Escopo e proteção dos dados

Use somente as VMs e os containers locais do laboratório, com contas descartáveis e senhas fictícias. Os testes registrados não envolveram contas reais ou sistemas de terceiros. O `.env` fica fora do Git; as evidências omitem senhas, cookies e tokens. Ao encerrar, desligue os ambientes e remova os dados temporários.

## Referências

- [Kali Linux](https://www.kali.org/)
- [Medusa](http://www.foofus.net/jmk/medusa/medusa.html)
- [DVWA](https://github.com/digininja/DVWA)
- [OWASP — autenticação](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
