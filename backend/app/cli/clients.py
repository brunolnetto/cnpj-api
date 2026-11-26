"""
Manage API clients.

Usage:
    python -m backend.app.cli.clients create "Client name"
    python -m backend.app.cli.clients list
    python -m backend.app.cli.clients deactivate <client_id>
    python -m backend.app.cli.clients activate <client_id>
"""

import argparse
import sys

from backend.app.api.repositories.auth import ApiClientRepository
from backend.app.database.base import get_session, init_database
from backend.app.setup.config import settings


def _repository_session():
    return get_session(settings.POSTGRES_DBNAME_AUDIT)


def create_client(name: str) -> int:
    with _repository_session() as session:
        client, client_secret = ApiClientRepository(session).create(name)

    print(f"client_id:     {client.apcl_client_id}")
    print(f"client_secret: {client_secret}")
    print("Store the secret now: it is not saved and cannot be shown again.")

    return 0


def list_clients() -> int:
    with _repository_session() as session:
        clients = ApiClientRepository(session).list()

        for client in clients:
            status = "active" if client.apcl_is_active else "inactive"
            print(f"{client.apcl_client_id}\t{status}\t{client.apcl_name}")

    return 0


def set_client_active(client_id: str, is_active: bool) -> int:
    with _repository_session() as session:
        found = ApiClientRepository(session).set_active(client_id, is_active)

    if not found:
        print(f"Client {client_id} not found.", file=sys.stderr)
        return 1

    state = "activated" if is_active else "deactivated"
    print(f"Client {client_id} {state}.")

    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Manage API clients.")
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="Create a client and print its secret")
    create.add_argument("name")

    commands.add_parser("list", help="List clients")

    deactivate = commands.add_parser("deactivate", help="Revoke a client's access")
    deactivate.add_argument("client_id")

    activate = commands.add_parser("activate", help="Restore a client's access")
    activate.add_argument("client_id")

    args = parser.parse_args(argv)

    # Creates the api_clients table if it does not exist yet
    init_database()

    if args.command == "create":
        return create_client(args.name)
    if args.command == "list":
        return list_clients()

    return set_client_active(args.client_id, args.command == "activate")


if __name__ == "__main__":
    sys.exit(main())
