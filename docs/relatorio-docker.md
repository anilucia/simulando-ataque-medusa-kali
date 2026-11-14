# Comparação de autenticação no DVWA em Docker

Executada em **14/11/2026**, com um cliente HTTP Python no hospedeiro e acesso exclusivo a `http://127.0.0.1:4280/`. Os [registros sanitizados](evidencias/testes-docker.json) contêm os valores medidos, as versões e os digests das imagens. Os resultados das VMs de 13/11 estão em [outro relatório](relatorio.md).

A [validação final](evidencias/validacao-docker-2026-11-14.json) também confirma a configuração de redes e portas, a preservação do `.env`, os links locais e a ausência das contas descartáveis no banco.

## Ambiente e acesso

O Docker Engine 29.2.1 executou DVWA, MariaDB e um proxy Nginx. O banco e o proxy estavam saudáveis; a aplicação respondeu HTTP 200. O DVWA e o banco estavam somente na rede interna `laboratorio`, sem portas publicadas. Apenas o proxy publicou `127.0.0.1:4280`, usando uma segunda rede bridge de entrada. Essa rede do proxy possui conectividade externa; o proxy encaminha requisições a um único destino interno, `dvwa:80`.

A tabela IPv4 do DVWA continha somente a rota da sub-rede, sem rota padrão. Foram conferidas as redes efetivamente ligadas aos containers e a publicação da porta em execução. Não foi realizado teste de saída por todos os protocolos nem teste de um cliente externo contra o firewall do hospedeiro.

Na tentativa inicial, a publicação de porta em uma rede somente interna não entrou em vigor, embora constasse na configuração. Foi adicionado o proxy para manter aplicação e banco isolados. O comportamento coincide com um [relato no projeto Moby](https://github.com/moby/moby/discussions/53256). A conectividade HTTP foi confirmada depois dessa correção.

As versões e distribuições estão em [ambientes.md](ambientes.md); os digests das imagens estão no JSON da execução. O perfil opcional Kali não foi construído nem usado nesta comparação.

## Método

O banco exclusivo do laboratório foi inicializado, e uma conta descartável recebeu uma credencial aleatória conhecida. O acesso inicial à aplicação utilizou o token anti-CSRF da página de login. O teste mudou o nível de segurança pela interface HTTP e verificou o cookie de nível antes de enviar as tentativas ao módulo Brute Force.

Em Low, foram enviadas duas senhas inválidas e depois a credencial válida. Em Impossible, foram enviadas três senhas inválidas e depois a credencial válida. Os tokens exigidos pelo nível Impossible foram obtidos e usados normalmente, sem desabilitar autenticação ou contornar o controle.

A comparação foi repetida após uma falha na coleta de metadados, usando uma nova conta descartável. **Foram realizadas 14 verificações no módulo, mais dois logins iniciais na aplicação.** A tabela apresenta somente as medições da segunda execução, arquivada integralmente; os logs sanitizados incluem as duas.

## Resultados arquivados

| Nível | Credencial | Tentativa | Resposta | Duração | Contador antes → depois |
|---|---|---|---|---|---|
| Low | Inválida | 1 | Rejeitada | 0,047 s | 0 → 0 |
| Low | Inválida | 2 | Rejeitada | 0,016 s | 0 → 0 |
| Low | Válida conhecida | 3 | Aceita | 0,063 s | 0 → 0 |
| Impossible | Inválida | 1 | Rejeitada | 4,110 s | 0 → 1 |
| Impossible | Inválida | 2 | Rejeitada | 2,015 s | 1 → 2 |
| Impossible | Inválida | 3 | Rejeitada | 2,078 s | 2 → 3 |
| Impossible | Válida conhecida | 4 | Rejeitada após bloqueio | 3,062 s | 3 → 4 |

Todas as respostas tiveram status HTTP 200. A classificação de sucesso e falha considerou o conteúdo retornado pelo módulo. O contador foi consultado diretamente no banco pelo administrador do laboratório; as credenciais do banco não foram publicadas.

O código instalado de Impossible configurava limiar de **três falhas**, bloqueio de **15 minutos** e espera aleatória de **dois a quatro segundos** no caminho de falha. Os valores observados são compatíveis com esse código. A senha válida foi recusada quando o contador já era três, o que demonstra o bloqueio naquele momento. A quarta resposta também incrementou o contador. Não foi aguardado o período de expiração para testar a liberação da conta.

## Registros e proteção de dados

Em Low, o formulário usou GET. O Apache registrou usuário e senha na URL; esses valores foram substituídos antes de salvar a evidência. Em Impossible, o formulário usou POST. Isso removeu as credenciais da URL nesse caminho, mas não constitui uma garantia geral de que dados nunca serão registrados.

O proxy foi configurado para registrar método, caminho sem parâmetros e status. Seus eventos coletados não incluíram query strings. Cookies e tokens não foram exportados. A conta descartável foi excluída ao final de cada execução; o banco de demonstração foi preservado para uso local. O nível inicial do Compose permanece `impossible` para novas sessões.

Os horários dos registros HTTP usam UTC; a data principal do JSON usa São Paulo (`-03:00`). Os endereços nos eventos são privados da rede Docker. A verificação foi feita por HTTP, inspeção do Docker e consulta administrativa do contador.

## Aprendizado e limites

Low permitiu autenticação válida depois de falhas sem alterar esse contador. Impossible acrescentou bloqueio por conta e atraso, impedindo o acesso imediato mesmo com a credencial válida. Isso demonstra um efeito observável do controle, mas também reforça a necessidade de calibrar bloqueios para evitar indisponibilidade deliberada de contas.

O teste utilizou credenciais conhecidas e não demonstrou descoberta de uma senha desconhecida. Não houve Medusa no teste web, teste de carga, estudo estatístico de tempos, verificação de recuperação após 15 minutos nem auditoria completa de segurança. O nome Impossible é um nível didático da aplicação; não certifica que ela seja adequada para produção.
