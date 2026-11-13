"""
Gera um MP3 para cada trecho de texto, com voz feminina da Espanha (es-ES).

Uso:
    pip install edge-tts
    python gerar_audios.py

Prepare um arquivo "textos.txt" na mesma pasta, com os trechos separados
por uma linha contendo apenas três hífens:

    Primer texto aquí, con su puntuación.
    ---
    Segundo texto aquí.
    ---
    Tercer texto...

Os áudios serão salvos na pasta "audios" como audio_01.mp3, audio_02.mp3...
"""

import asyncio
from pathlib import Path

import edge_tts

# Vozes femininas es-ES: "es-ES-ElviraNeural" ou "es-ES-XimenaNeural"
VOZ = "es-ES-ElviraNeural"
VELOCIDADE = "+0%"  # ex.: "-10%" para mais lento, "+10%" para mais rápido

ARQUIVO_TEXTOS = Path("textos.txt")
PASTA_SAIDA = Path("audios")


def ler_trechos(caminho: Path) -> list[str]:
    conteudo = caminho.read_text(encoding="utf-8")
    partes = [p.strip() for p in conteudo.split("\n---\n")]
    return [p for p in partes if p]


async def gerar(trechos: list[str]) -> None:
    PASTA_SAIDA.mkdir(exist_ok=True)
    for i, texto in enumerate(trechos, start=1):
        destino = PASTA_SAIDA / f"audio_{i:02d}.mp3"
        comunicador = edge_tts.Communicate(texto, VOZ, rate=VELOCIDADE)
        await comunicador.save(str(destino))
        print(f"[{i}/{len(trechos)}] salvo em {destino}")


def main() -> None:
    if not ARQUIVO_TEXTOS.exists():
        raise SystemExit(f"Arquivo '{ARQUIVO_TEXTOS}' não encontrado.")
    trechos = ler_trechos(ARQUIVO_TEXTOS)
    print(f"{len(trechos)} trechos encontrados. Voz: {VOZ}")
    asyncio.run(gerar(trechos))
    print("Pronto!")


if __name__ == "__main__":
    main()
