#!/usr/bin/env python3
import argparse
from os import remove

from auth.user_repository import UserRepository
from auth.user_repository import DuplicateUserError
from auth.user_repository import UserNotFound
from auth.user import User
USER_REPO_FILE = "data/users.json"
user_repo = UserRepository(USER_REPO_FILE)

def list_users(args):
    users = user_repo.list_all()
    for user in users:
        print(f"Name: {user.name} | {'Ativo' if user.active else 'Desativado'} | UID: {user.uid}")

def add_user(args):
    new_user = User(args.name,True, int(args.uid))
    try:
        user_repo.add(new_user)
        print(f"Usuário(a) {new_user.name} adicionado com sucesso")
    except DuplicateUserError:
        print(f"Já existe um usuário com o UID: {new_user.uid}")
def remove_user(args):
    removed_user = user_repo.find_by_uid(args.uid)
    try:
        user_repo.remove(removed_user)
        print(f"O usuário {removed_user.name} foi removido!")
    except UserNotFound:
        print("Usuário não encontrado")


def main():
    parser = argparse.ArgumentParser(prog="smartlock",description="Script para gerenciamento da fechadura do clube Insabots")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponíveis")
    user_parser = subparsers.add_parser("user", help="Gerenciamento de usuários")
    user_subparsers = user_parser.add_subparsers(dest="subcommand", required=True, help="Ações de usuário")
    list_parser = user_subparsers.add_parser("list", help="Lista os usuários cadastrados")
    list_parser.set_defaults(func=list_users)
    add_parser = user_subparsers.add_parser("add", help="Adiciona um novo usuário")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--uid", required=True, type=int)
    add_parser.set_defaults(func=add_user)
    remove_parser = user_subparsers.add_parser("remove", help="Remove um usuário")
    remove_parser.add_argument("--uid", required=True, type=int)
    remove_parser.set_defaults(func=remove_user)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()