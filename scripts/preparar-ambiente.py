"""Gera apenas as senhas locais do banco; nao executa tentativas de login."""

from pathlib import Path
import secrets


def main():
    root = Path(__file__).resolve().parents[1]
    target = root / ".env"
    content = (
        "# Gerado localmente. Nao adicionar ao Git.\n"
        f"DVWA_DB_PASSWORD={secrets.token_hex(24)}\n"
        f"DVWA_DB_ROOT_PASSWORD={secrets.token_hex(24)}\n"
    )
    try:
        with target.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError:
        print(".env ja existe; preservado sem alteracoes.")
    else:
        print(".env criado com credenciais locais. Os valores nao serao exibidos.")


if __name__ == "__main__":
    main()
