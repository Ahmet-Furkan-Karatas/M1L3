import discord
from discord.ext import commands
from config import token  # Botun tokenini config dosyasından içe aktarma

intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        await channel.send(f'Hoş geldiniz: , {member.mention}!')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        await ctx.guild.ban(member)
        await ctx.send(f"Kullanıcı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@bot.command()
async def poll(ctx, *, question):
    message = await ctx.send(f"🗳️ Oylama: {question}")
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    await message.add_reaction("🤷")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "https://" in message.content:
        await message.guild.ban(message.author)
        await message.channel.send(f"{message.author.name} bağlantı gönderdiği için banlandı.")
    else:
        await bot.process_commands(message)

bot.run(token)
