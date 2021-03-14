# Nao precisa testar, relaxa

### Integrantes
- Nathan - [Nium#6672](https://github.com/NiumXp) (Cycle, Tester e Desenvolvedor)
- Gabriel - [black1363#0257]() (Creativo, Tester e Desenvolvedor)
- João - [jv#8586](https://www.instagram.com/jvartesgraficas/) (Designer UX)
- Yago - [DNK#6725](https://github.com/yagomichalak) (Desenvolvedor)

### Resumo
A ideia central que tivemos para o projeto era de criar um jogo simples que nem o jogo da velha, mas um pouco estratégico que nem UNO. Para isso, pensamos em criar um servidor utilizando `http` e `ws`, só que o nosso grande problema era criar o front-end, não temos conhecimento suficiente para o que queriamos apresentar.

Queriamos muito ver o jogo funcionando, então decidimos utilizar a api do discord - os BOTs - ao invés de criar o front-end!

# Instalação
Como utilizamos a api do discord, criamos um BOT já em produção para pular a etapa de instalação e você ir direto para a diversão! Basta clicar [aqui](https://discord.com/api/oauth2/authorize?client_id=806297071690579968&permissions=8&scope=bot) e adicionar o BOT em algum servidor e digitar o comando `@CardBot help`!

Fizemos sim um passo a passo de instalação para rodar localmente ou em outro lugar o projeto, segue o passo passo [aqui](github/instalation.md)!

# Tutorial

Neste jogo você tem como objetivo remover todos os "corações" do seu oponente com suas cartas, cada uma delas tem sua habilidade, seus prós e contras. 

### Cartas
#### 🟥 Carta vermelho
Remove o coração vermelho do inimigo ❤️

#### 🟩 Carta verde
Remove o coração verde do inimigo 💚

#### 🟨 Carta amarelo
Remove o coração amarelo do inimigo 💛

#### 🟦 Carta azul
Remove qualquer coração inimigo

#### 🟪 Carta rosa
Repete o que a última carta jogada do jogador faz

#### ⬜ Carta branca
Remove uma carta aleatória do inimigo

#### ⬛ Carta preta
Recebe uma carta aleatória

As cartas serão distribuídas aleatoriamente para você e seu adversário.  
Na sua vez você poderá escolher entre suas cartas, uma que melhor se encaixa na situação em que você se encontra na partida, depois de você jogar sua carta á a vez do seu oponente após ele jogar é você novamente, vocês só podem jogar uma carta por vez, cada um em sua vez e por ai vai, se as cartas de ambos acabar "a decidir", agora se você não tiver mais corações significa que você perde e seu oponente venceu, se for ao contrario você ganha o jogo e ele perde e a partida acaba.
