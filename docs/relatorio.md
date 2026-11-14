# Relatório dos testes nas VMs

Exercícios realizados em **13/11/2026**. Fonte dos valores: [observações sanitizadas](evidencias/observacoes.json). Este relatório descreve a etapa VirtualBox; não registra testes no Docker.

## Objetivo e método

Foram criadas duas contas descartáveis, com senhas fictícias, para observar falhas e sucessos de autenticação. Uma delas também foi adicionada ao banco do DVWA. Os testes partiram do hospedeiro pela interface Host-only; duas verificações complementares de FTP partiram do Medusa no Kali. Todas as credenciais válidas foram fornecidas previamente: não houve descoberta de uma senha desconhecida.

Os snapshots das duas VMs foram criados antes dos exercícios. Apenas a rede Host-only estava habilitada; a comunicação entre Kali e Metasploitable foi confirmada nas duas direções. As tabelas de rotas não apresentavam rota externa utilizável, e uma consulta local de rota fora da sub-rede retornou `Network is unreachable`. Nenhum envio a um alvo externo foi necessário para essa consulta. No hospedeiro, a interface Host-only não tinha gateway IPv4 ou IPv6 nem encaminhamento habilitado; nenhuma regra foi retornada por `Get-NetNat`.

O JSON usa horário de São Paulo (`-03:00`). Os registros HTTP da VM indicam `-0500`; trechos de outros serviços e do Medusa preservam seus horários de origem. O Kali usou temporariamente 384 MB de RAM, o que limita conclusões sobre desempenho. As durações são medições locais, não resultados de um teste de carga.

## FTP

O banner do serviço anunciou **vsFTPd 2.3.4**. Havia também ProFTPD instalado, mas ele não foi o serviço anunciado na conexão testada. A versão do banner não foi confirmada por auditoria do binário.

| Origem | Verificação | Quantidade | Resposta |
|---|---|---|---|
| Hospedeiro | Senha inválida | 3 | `530 Login incorrect.` |
| Hospedeiro | Credencial válida conhecida | 1 | `230 Login successful.` |
| Kali / Medusa 2.3 | Senha inválida | 1 | Sem indicação de sucesso; evento de falha no servidor |
| Kali / Medusa 2.3 | Credencial válida conhecida | 1 | Sucesso indicado pelo Medusa e pelo registro do servidor |

As falhas medidas pelo hospedeiro levaram **3,344 s; 3,094 s; 3,828 s**. O sucesso levou **0,016 s**. O componente responsável pelo atraso não foi isolado. Cada execução do Medusa recebeu somente um par de credenciais, com um login concorrente e sem novas tentativas de conexão configuradas.

O registro do serviço mostrou `FAIL LOGIN` e `OK LOGIN`, com conta e origem ocultadas no JSON. A autenticação válida após as falhas confirma que a conta estava utilizável naquele momento. A amostra não permite afirmar ausência de qualquer limitação ou bloqueio em outros intervalos e volumes.

**Recomendação:** restringir acesso ao serviço, adotar transporte protegido, monitorar falhas e avaliar limitação de tentativas e bloqueios temporários. Essas medidas não foram implantadas nesta execução.

## DVWA

Foi testado o módulo de autenticação da versão **1.0.7 instalada na VM**. Houve um login válido inicial na aplicação, além das nove verificações do módulo abaixo.

| Nível | Falhas | Duração das falhas | Sucessos | Duração do sucesso |
|---|---|---|---|---|
| Low | 2 | 0,062 s e 0,063 s | 1 | 0,078 s |
| Medium | 2 | 0,047 s e 0,062 s | 1 | 0,047 s |
| High | 2 | 3,031 s e 3,016 s | 1 | 0,031 s |

As falhas retornaram uma mensagem genérica de usuário e/ou senha incorretos. O sucesso exibiu a área protegida. O código instalado do nível High continha uma espera de três segundos no caminho de falha, compatível com os tempos observados. Não foi observado atraso progressivo na amostra.

O tratamento de entrada do nível Medium não produziu o atraso observado em High. Tratar entrada e limitar tentativas são controles distintos. Os resultados desta versão antiga não demonstram o comportamento dos níveis do DVWA atual.

**Achado de exposição de dados:** os registros HTTP continham usuário e senha nos parâmetros da URL do módulo. Os valores foram removidos da evidência pública. Respostas de sucesso e falha tiveram status HTTP 200; a classificação dependeu do conteúdo da página, não apenas do status.

**Recomendação:** evitar credenciais em URLs e registros, proteger o transporte e implementar controles de autenticação e limitação de tentativas. Atraso fixo, isoladamente, não demonstra proteção completa contra automação. Veja as [orientações da OWASP sobre autenticação](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).

## SMB

O serviço informou **Samba 3.0.20-Debian**. O cliente Impacket 0.13.1 negociou o dialeto **NT LM 0.12 (SMB1)**. Esse dialeto identifica a versão do protocolo SMB; a versão do mecanismo NTLM de autenticação não foi registrada separadamente.

A mesma senha inválida foi fornecida uma vez para cada uma das duas contas fictícias, para observar o conceito de tentativas distribuídas entre contas. Cada conta também recebeu uma autenticação válida de controle. Não houve enumeração de usuários.

| Conta fictícia | Senha inválida | Credencial válida conhecida |
|---|---|---|
| A | `STATUS_LOGON_FAILURE` | Aceita |
| B | `STATUS_LOGON_FAILURE` | Aceita |

| Política consultada no servidor | Valor retornado |
|---|---|
| `bad lockout attempt` | 0 |
| `lockout duration` | 30 |
| `min password length` | 5 |

O limiar zero indica bloqueio por esse contador desabilitado. O valor de duração não é evidência de que ocorreu bloqueio. As rejeições foram registradas no cliente; os trechos do servidor coletados mostram abertura e fechamento de sessões válidas. Não foram localizados eventos específicos das duas falhas SMB nesses trechos com a configuração de log existente.

**Recomendação:** atualizar o serviço para uma versão suportada, revisar protocolos e políticas de autenticação e configurar alertas que correlacionem várias contas. A observabilidade das falhas no servidor precisa ser melhorada. A configuração deve ser adaptada à versão implantada, conforme a [documentação do Samba](https://www.samba.org/samba/docs/current/man-html/smb.conf.5).

## Conclusão e limites

Os serviços rejeitaram as senhas incorretas e aceitaram as credenciais válidas conhecidas. Isso permite comparar respostas e eventos, mas não comprova resistência a tentativas repetidas em escala. O DVWA mostrou diferenças de atraso entre níveis e exposição de credenciais em registros; o SMB mostrou a necessidade de combinar consulta de política e observação dos eventos.

Não foram realizados teste de carga, exploração de vulnerabilidades ou descoberta de credenciais reais. As recomendações não foram aplicadas nem retestadas. As evidências são textuais e sanitizadas. As VMs foram encerradas pelo usuário; a remoção das contas temporárias e a restauração dos snapshots não foram verificadas.
