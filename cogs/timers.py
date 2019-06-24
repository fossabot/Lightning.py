import dataset
import time
from datetime import datetime
from discord.ext import commands
import asyncio
import traceback
import discord

class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.do_jobs())
        self.db = dataset.connect('sqlite:///config/powerscron.sqlite3')
        #self.jobs = self.db['cron_jobs']
        self.bot.log.info(f'{self.qualified_name} loaded')

    #def cog_unload(self):
        #self.do_timers.cancel()

    @commands.command(aliases=["addreminder", "timer"])
    async def remind(self, ctx, when: str, *, description: str = "something"):
        """Reminds you of something after a certain date.
        
        Examples:
        - ".remind 1d do essay" (1 day)
        - ".remind 1h do dishes" (1 hour)
        - ".remind 60s clean" (60 seconds)
        """
        current_timestamp = time.time()
        expiry_timestamp = self.bot.parse_time(when)

        if current_timestamp + 4 > expiry_timestamp:
            await ctx.send(f"{ctx.author.mention}: Minimum "
                            "remind interval is 5 seconds.")
            return

        expiry_datetime = datetime.utcfromtimestamp(expiry_timestamp)
        duration_text = self.bot.get_relative_timestamp(time_to=expiry_datetime,
                                                        include_to=True,
                                                        humanized=True)

        table = self.db["cron_jobs"]
        table.insert(dict(job_type="reminder", author=ctx.author.id,
                     channel=ctx.channel.id, remind_text=description,
                     expiry=expiry_timestamp, guild_id=ctx.guild.id))
        await ctx.send(f"{ctx.author.mention}: I'll remind you in {duration_text}.")

    @commands.command(aliases=['listreminds', 'listtimers'])
    async def listreminders(self, ctx):
        """Lists your reminders"""
        table = self.db["cron_jobs"].all()
        embed = discord.Embed(title="Reminders", description="\n")
        # Kinda hacky-ish code
        try:
            for job in table:
                if job['author'] == ctx.author.id:
                    if job['guild_id'] == ctx.guild.id:
                        expiry_timestr = datetime.utcfromtimestamp(job['expiry'])\
                            .strftime('%Y-%m-%d %H:%M:%S (UTC)')
                        embed.description += f"- {expiry_timestr}\nText: {job['remind_text']}\n"
        except:
            log_channel = self.bot.get_channel(527965708793937960)
            await log_channel.send(f"PowersCron has Errored! "
                                   f"```{traceback.format_exc()}```")
            embed.description += "No Timers Currently Running!"
        await ctx.send(embed=embed)

    async def do_jobs(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            jobs = self.db['cron_jobs'].all()
            timestamp = time.time()
            try:
                for jobtype in jobs:
                    expiry2 = jobtype['expiry']
                    if timestamp > expiry2:
                        if jobtype['job_type'] == "reminder":
                            channel = self.bot.get_channel(jobtype['channel'])
                            await channel.send(f"<@{jobtype['author']}>: "
                                               "Timer is up! "
                                               f"`{jobtype['remind_text']}`")
                            # Delete the timer
                            self.db['cron_jobs'].delete(author=jobtype['author'], expiry=expiry2,
                                                        job_type="reminder")
                        if jobtype['job_type'] == "timeban":
                            guid = self.bot.get_guild(jobtype['guild_id'])
                            uid = jobtype['user_id']
                            await guid.unban(uid, reason="PowersCron: "
                                             "Timed Ban Expired.")
                            # Delete the scheduled unban
                            self.db['cron_jobs'].delete(job_type="timeban", 
                                                        expiry=expiry2, user_id=uid)

            except:
                # Keep jobs for now if they errored
                log_channel = self.bot.get_channel(527965708793937960)
                await log_channel.send(f"PowersCron has Errored! "
                                       f"```{traceback.format_exc()}```")

            await asyncio.sleep(5)


        


def setup(bot):
    bot.add_cog(Timers(bot))