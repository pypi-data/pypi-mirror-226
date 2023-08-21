# generatore-piva
Un semplice generatore di PIVA

Questo pacchetto permette di generare delle Partite IVA casuali ma formalmente valide.
L'obbiettivo di questo strumento è aiutare gli sviluppatori nel testing dei loro applicativi.

Non mi assumo alcuna responsabilià di un utilizzo improprio di questo strumento.

## Installazione

Puoi installare questo pacchetto dal [PyPI](https://pypi.org/project/generatorepiva/):

    python -m pip install generatorepiva

## Esempio d'uso
```
from generatorepiva import GeneratorePiva


def main():
    generatore_piva = GeneratorePiva()

    # Genera 100 PIVA
    for _ in range(100):
        piva = generatore_piva.genera()
        print(f'PIVA: {piva}')


if __name__ == '__main__':
    main()
```
