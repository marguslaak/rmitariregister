from django.core.management.base import BaseCommand, CommandError
from metadata.models import Workflow


class Command(BaseCommand):
    help = "Run workflow"

    def add_arguments(self, parser):
        parser.add_argument("id", nargs="+", type=int)

    def handle(self, *args, **options):
        for wid in options["id"]:
            workflow = Workflow.objects.get(pk=wid)
            if workflow.run_steps():
                self.stdout.write(
                    self.style.SUCCESS('Successfully runned "%s"' % wid)
                )
