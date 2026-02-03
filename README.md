# 🎮 Flappy Bird AI

Jogo Flappy Bird com Inteligência Artificial usando algoritmo genético NEAT.

## 📋 Requisitos

- Python 3.14+ (ou Python 3.8+)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone/Baixe o Projeto

Certifique-se de ter todos os arquivos:

- `FlappyBird.py`
- `config.txt`
- `requirements.txt`
- Pasta `imgs/` com todas as imagens

### 2. Instale as Dependências

Abra o terminal/prompt de comando na pasta do projeto e execute:

```bash
python -m pip install -r requirements.txt
```

Ou instale manualmente:

```bash
python -m pip install pygame-ce neat-python
```

### 3. Execute o Jogo

```bash
python FlappyBird.py
```

## 🎯 Como Funciona

- **Modo AI**: Por padrão, a IA treina sozinha usando algoritmo genético NEAT
- A cada geração, os pássaros aprendem a jogar melhor
- Você verá "Geração: X" no canto superior esquerdo
- A pontuação aparece no canto superior direito

## 🎮 Modo Manual (Opcional)

Para jogar manualmente, edite `FlappyBird.py` e mude a linha 6:

```python
ai_jogando = False  # Mude de True para False
```

Depois pressione **ESPAÇO** para pular.

## 📦 Dependências

- **pygame-ce** (2.5.6+): Engine do jogo
- **neat-python** (1.1.0+): Algoritmo genético para IA

## ⚠️ Solução de Problemas

### Erro: "No module named 'pygame'"

```bash
python -m pip install pygame-ce
```

### Erro: "No module named 'neat'"

```bash
python -m pip install neat-python
```

### Erro no config.txt

Certifique-se de que o arquivo `config.txt` está completo e na mesma pasta que `FlappyBird.py`

## 📁 Estrutura do Projeto

```
FlappyBirdAI/
├── FlappyBird.py          # Código principal
├── config.txt             # Configuração do NEAT
├── requirements.txt       # Dependências
├── README.md             # Este arquivo
└── imgs/                 # Pasta de imagens
    ├── bird1.png
    ├── bird2.png
    ├── bird3.png
    ├── pipe.png
    ├── base.png
    └── bg.png
```

## 🎓 Sobre o NEAT

NEAT (NeuroEvolution of Augmenting Topologies) é um algoritmo genético que evolui redes neurais. Neste projeto:

- Cada pássaro tem seu próprio "cérebro" (rede neural)
- Os pássaros que sobrevivem mais tempo têm maior fitness
- A cada geração, os melhores cérebros são combinados para criar a próxima geração
- Com o tempo, a IA aprende a jogar perfeitamente!

---

Desenvolvido com Python, Pygame e NEAT 🚀
