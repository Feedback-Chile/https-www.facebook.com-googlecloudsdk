# Reconstrucción de Código

Este repositorio contiene una utilidad pequeña para reconstruir código a partir de
fragmentos dispersos. La herramienta puede limpiar marcadores de delimitación y
prefijos típicos de prompts antes de unir los fragmentos.

## Uso rápido

```bash
python3 reconstruct.py fragmento1.txt fragmento2.txt > reconstruido.txt
```

Si no pasas archivos, la herramienta leerá desde `stdin`:

```bash
cat fragmentos.txt | python3 reconstruct.py
```

Para eliminar líneas duplicadas (por ejemplo cuando los fragmentos se solapan):

```bash
python3 reconstruct.py --dedupe fragmentos.txt
```

### Limpiar prompts de equipos de red

Si los fragmentos incluyen líneas con prompts como `Rep_Imilac#show ...`, puedes
limpiarlos con `--strip-prompts` o eliminando un prefijo específico:

```bash
python3 reconstruct.py --strip-prompts salida.txt
python3 reconstruct.py --strip-prefix "Rep_Imilac#" salida.txt
```

Para eliminar líneas completas que contienen el prompt y el comando:

```bash
python3 reconstruct.py --drop-prompt-lines salida.txt
```

Para eliminar líneas vacías después de la limpieza:

```bash
python3 reconstruct.py --drop-empty salida.txt
```
