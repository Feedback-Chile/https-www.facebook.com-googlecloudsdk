# Reconstrucción de Código

Este repositorio contiene una utilidad pequeña para reconstruir código a partir de
fragmentos dispersos. La herramienta elimina líneas duplicadas y omite marcadores
comunes de delimitación (por ejemplo `<<<`, `>>>`, `===`).

## Uso rápido

```bash
python3 reconstruct.py fragmento1.txt fragmento2.txt > reconstruido.txt
```

Si no pasas archivos, la herramienta leerá desde `stdin`:

```bash
cat fragmentos.txt | python3 reconstruct.py
```

Para conservar las líneas duplicadas:

```bash
python3 reconstruct.py --keep-duplicates fragmentos.txt
```
