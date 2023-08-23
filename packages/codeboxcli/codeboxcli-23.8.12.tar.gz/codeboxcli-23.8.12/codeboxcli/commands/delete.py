# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet
from codeboxcli.utils import messages

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def delete(args):
    # Initialize loop index
    i = 0
    while i < len(args):
        # Check if the current argument is "--help"
        if args[i] == "--help":
            print(messages.help_delete())
            return  # Exit the function

        # Delete a Snippet instance
        with Session() as session:
            snippet = session.query(Snippet).get(args[i])

            if snippet:
                session.delete(snippet)
                session.commit()
                i += 1
            else:
                print(messages.error_not_found(args[i]))
                i += 1
