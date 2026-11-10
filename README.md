# Auditoria defensiva de autenticação: Kali Linux, Medusa e laboratório isolado

Projeto de estudo sobre tentativas repetidas de autenticação e formas de detectá-las e mitigá-las. O objetivo é compreender o risco e documentar controles defensivos em um ambiente local, isolado e autorizado.

> **Estado deste repositório:** este README é um roteiro de laboratório e um modelo de relatório. Nenhum teste foi executado e nenhum resultado deve ser considerado observado até que os campos de registro sejam preenchidos com evidências próprias.

## Objetivos

- Entender, em nível conceitual, como tentativas repetidas de senha afetam FTP, formulários web e SMB.
- Montar uma rede de laboratório sem conexão com redes de terceiros.
- Observar registros e controles de autenticação durante testes autorizados.
- Recomendar medidas para reduzir tentativas automatizadas e o impacto de credenciais comprometidas.
- Registrar evidências sem publicar senhas, tokens, endereços públicos ou dados pessoais.

## Escopo e regras de segurança

Todos os testes devem permanecer nas VMs locais que você controla. Não aponte ferramentas para endereços públicos, redes corporativas, contas reais ou sistemas de terceiros. Não reutilize senhas reais. Use contas descartáveis, credenciais fictícias e o mínimo de tentativas necessário para observar o comportamento defensivo.

Este repositório não contém listas de senhas nem automação de tentativa de credenciais. A atividade deve ser conduzida somente conforme autorização explícita e regras do laboratório. Se o isolamento ou o escopo não puder ser confirmado, não execute testes.

## Ambiente de laboratório

### Componentes

- VirtualBox atualizado.
- Kali Linux para observação e estudo.
- Metasploitable 2 e/ou DVWA em uma VM separada.
- Uma rede **Host-only** criada no VirtualBox, sem adaptador em modo *Bridged*.

### Preparação segura

1. Crie uma rede Host-only no VirtualBox e confirme que ela não oferece roteamento para a rede local ou para a Internet.
2. Configure os adaptadores das VMs para usar somente essa rede durante os exercícios.
3. Não habilite pastas compartilhadas, área de transferência ou *drag-and-drop* entre o sistema hospedeiro e a VM vulnerável, a menos que isso seja indispensável.
4. Inicialize as VMs e registre as versões e endereços privados atribuídos pelo próprio laboratório. Não presuma que um endereço padrão será igual no seu ambiente.
5. Confirme que as VMs se comunicam entre si e que a VM vulnerável não alcança redes externas. Se houver acesso externo inesperado, desligue as VMs e corrija a configuração antes de continuar.
6. Faça um snapshot antes dos testes e use contas de laboratório sem qualquer relação com contas pessoais.
7. Mantenha os serviços de laboratório desligados quando não estiverem em uso.

### Inventário

| Item | Valor observado |
|---|---|
| Sistema hospedeiro e versão | _Preencher_ |
| VirtualBox e versão | _Preencher_ |
| Kali Linux e versão | _Preencher_ |
| Metasploitable 2 e/ou DVWA e versão | _Preencher_ |
| Tipo e faixa da rede privada | _Preencher sem publicar dados sensíveis_ |
| Data do teste | _Preencher_ |

## Roteiro de estudo

Os cenários abaixo são para observação controlada e documentação. Use somente as interfaces do laboratório, credenciais fictícias e procedimentos autorizados pelo instrutor. Não publique comandos de tentativa em massa, listas de credenciais ou dados de acesso.

### FTP

Estude quais controles o serviço FTP oferece contra falhas repetidas de autenticação. Em um cenário autorizado, observe os registros do serviço e do sistema, a resposta a credenciais inválidas e se existe limitação de tentativas. Não use credenciais reais nem teste fora da VM de laboratório.

**Registre:** serviço e versão observados, controle existente, evidência sanitizada e oportunidade de melhoria.

### Formulário web (DVWA)

Use a aplicação vulnerável apenas localmente. Examine como o nível de segurança configurado afeta a validação do formulário, a resposta a falhas de autenticação, o registro de eventos e a presença de controles como atraso ou limitação de tentativas. A finalidade é comparar controles e propor correções, não obter acesso a contas reais.

**Registre:** nível de segurança, comportamento observado, controles ausentes/presentes e evidência sanitizada. Não publique cookies de sessão, tokens ou credenciais.

### SMB

Estude o risco de *password spraying* como conceito: poucas senhas comuns distribuídas entre várias contas podem causar bloqueios e comprometer contas com senhas fracas. Faça a análise somente com contas fictícias preparadas para o laboratório e por meio de observação defensiva dos eventos do serviço. Evite enumeração automatizada de usuários ou qualquer teste em redes que não sejam suas.

**Registre:** mecanismo de autenticação, política de senha e bloqueio, eventos observados e medidas de mitigação.

## Registro dos resultados

Preencha a tabela apenas após realizar os exercícios no ambiente isolado. Não invente resultados. Evite incluir comandos operacionais, senhas, nomes de usuário reais, IPs públicos ou informações que permitam reutilizar o teste contra terceiros.

| Cenário | Data | Configuração/controle observado | Resultado e evidência sanitizada | Recomendação |
|---|---|---|---|---|
| FTP | _Pendente_ | _Pendente_ | _Pendente_ | _Pendente_ |
| DVWA | _Pendente_ | _Pendente_ | _Pendente_ | _Pendente_ |
| SMB | _Pendente_ | _Pendente_ | _Pendente_ | _Pendente_ |

### Evidências

Se incluir capturas de tela, salve-as em `images/` e remova ou oculte credenciais, cookies, tokens, nomes pessoais, endereços externos e informações do hospedeiro. Inclua uma legenda com data, cenário e o que a captura demonstra. Não inclua capturas que revelem instruções operacionais de tentativa automatizada.

## Recomendações de mitigação

- Aplicar senhas longas, únicas e bloqueio de senhas conhecidas como comprometidas.
- Habilitar MFA sempre que suportado, especialmente para administração e acesso remoto.
- Limitar tentativas por conta e por origem, com atrasos progressivos e bloqueios temporários cuidadosamente calibrados.
- Monitorar falhas repetidas, tentativas distribuídas entre contas e padrões de origem incomuns; encaminhar alertas para a equipe responsável.
- Evitar mensagens de erro que revelem se um usuário existe.
- Desabilitar serviços e contas não utilizados e restringir FTP/SMB por firewall à menor faixa de rede necessária.
- Preferir protocolos seguros; evitar FTP sem criptografia e revisar a configuração do SMB conforme as recomendações atuais do fornecedor.
- Usar controles contra automação no formulário web, proteção de sessão, limitação de requisições e registro de eventos sem armazenar senhas.
- Revisar periodicamente políticas de autenticação, registros e procedimentos de resposta a incidentes.
- Tratar bloqueios para reduzir o risco de negação de serviço causada por bloqueios deliberados de contas.

## Encerramento do laboratório

Ao terminar, desligue as VMs, restaure o snapshot se necessário e confirme que a rede Host-only continua isolada. Remova contas e credenciais temporárias. Antes de publicar o repositório, revise o histórico e os arquivos para garantir que nenhum segredo ou dado sensível foi incluído.

## Referências

- [Kali Linux](https://www.kali.org/)
- [DVWA — Damn Vulnerable Web Application](https://github.com/digininja/DVWA)
- [Medusa — página do projeto](http://www.foofus.net/jmk/medusa/medusa.html)
- [Nmap Reference Guide](https://nmap.org/book/)
- [Documentação do VirtualBox](https://www.virtualbox.org/manual/)

## Entrega

Depois de executar os estudos e preencher os resultados com suas próprias observações, publique este projeto em um repositório público do GitHub. Revise cuidadosamente o conteúdo e as evidências antes da publicação. No formulário de entrega da DIO, inclua o link do repositório e uma breve descrição do aprendizado.
