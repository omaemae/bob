import bob
import logging
import multiprocessing
from discord.ext import commands
from flask import Flask, render_template


class ModPanel(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.logger = logging.getLogger("cogs.ModPanel")
        self.logger.debug("registered.")

        self.app = Flask("ModPanel")

        @self.app.route("/")
        def index():
            responses = len([response for question in bob.question_map.values() for response in question.responses])
            return render_template(
                'index.html',
                bob_version=bob.__version__,
                questions=len(bob.question_map.keys()),
                responses=responses,
                guilds=len(self.client.guilds),
                users=len(self.client.users),
                shards=self.client.shard_count
            )

        self.process = multiprocessing.Process(
            target=self.app.run,
            kwargs={"host": "127.0.0.1", "port": 8540},
            daemon=True
        )
        self.process.start()

    def cog_unload(self):
        self.process.kill()
        self.process.close()


def setup(client: commands.Bot):
    client.add_cog(ModPanel(client))
