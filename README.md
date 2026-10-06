# Marcenaria 3D — importação automática de .BLEND

Esta versão permite escolher um arquivo `.blend` no celular/tablet. O navegador envia o arquivo ao backend Python; o **Blender instalado no servidor** abre o `.blend` em modo sem interface, exporta automaticamente para `.glb`, e o visualizador Three.js carrega o resultado.

## Importante
GitHub Pages sozinho **não executa Python nem Blender**. O GitHub pode guardar o código, mas esta versão precisa ser publicada em um servidor/container que permita instalar e executar Blender.

## Testar no computador
1. Instale Blender 4.x e Python 3.11+.
2. No terminal, dentro da pasta: `python -m venv .venv`
3. Ative o ambiente e rode: `pip install -r requirements.txt`
4. Se `blender` não estiver no PATH, defina `BLENDER_BIN` apontando para o executável do Blender.
5. Rode: `python app.py`
6. Abra `http://localhost:8000`.

## Fluxo no celular
Abra o endereço do servidor → **Abrir .BLEND** → escolha o arquivo → aguarde a conversão → o modelo aparece na cena.

## Estrutura
- `app.py`: servidor Flask e upload/conversão.
- `convert_blend.py`: script executado dentro do Blender para exportar GLB.
- `static/index.html`: visualizador 3D mobile.
- `uploads/`: arquivos temporários enviados.
- `converted/`: GLBs gerados.

## Próximo passo recomendado
Criar uma biblioteca persistente no servidor (Cozinha, Quarto, Banheiro, Painéis, Eletros), para cada `.blend` ser convertido só uma vez e depois aparecer como item do catálogo.
