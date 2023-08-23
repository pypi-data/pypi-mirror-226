# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet
from codeboxcli.utils import default_editor
from codeboxcli.utils import messages

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def edit(args):
    if len(args) == 1:
        # Check if the current argument is "--help"
        if args[0] == "--help":
            print(messages.help_edit())
            return  # Exit the function

        # Update a Snippet instance
        with Session() as session:
            snippet = session.query(Snippet).get(args[0])

            if snippet:
                snippet.content = default_editor.open_default_editor(
                    snippet.content)
                session.commit()
            else:
                print(messages.error_not_found(args[0]))
    else:
        print(messages.help_edit())
