# pylint: disable=arguments-differ
# pylint: disable=function-redefined
# pylint: disable=protected-access
# pylint: disable=unused-argument

import functools

from django.core.management.commands.test import Command
from django.test import runner


@functools.wraps(runner._setup_databases)
def setup_databases(*args, keepdb=False, **kwargs):
  return setup_databases.__wrapped__(*args, keepdb=False, **kwargs)


class Command(Command):

  def add_arguments(self, parser):
    super().add_arguments(parser)
    parser.add_argument(
      '--tuhoa',
      action='store_true',
      help=(
        'Tuhoa testitietokanta ennen uuden luontia.'
        ' Hyödyllinen `--keepdb`-valitsimen yhteydessä.'
      ),
    )
    # def add_arguments

  def handle(self, *args, tuhoa, **options):
    if tuhoa:
      runner._setup_databases = setup_databases
    return super().handle(*args, **options)
    # def handle

  # class Command
