import discord
from discord.ext import commands
import sqlite3
import config


def vt_kur():
    baglanti = sqlite3.connect("destek_talepleri.db")
    imlec = baglanti.cursor()
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS talepler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT,
            kullanici_id TEXT,
            departman TEXT,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    baglanti.commit()
    baglanti.close()

vt_kur()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("----------------------------------------")
    print(f"Bot Basariyla Acildi: {bot.user.name}")
    print("Alabilecegin Her Sey - Destek Sistemi Aktif!")
    print("----------------------------------------")


@bot.command(name="sss")
async def sss(ctx):
    embed = discord.Embed(
        title="Alabilecegin Her Sey - Sikca Sorulan Sorular",
        description="Musterilerimizin en cok merak ettigi konular ve cevaplari:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="1. Kargo ve Teslimat Süresi", 
        value="Siparisleriniz 1-3 is gunu icerisinde kargoya verilir.", 
        inline=False
    )
    embed.add_field(
        name="2. Iade ve Degisim Kosullari", 
        value="14 gun icerisinde ambalaji bozulmamis urunleri iade edebilirsiniz.", 
        inline=False
    )
    embed.add_field(
        name="3. Odeme Yontemleri", 
        value="Kredi karti, banka karti ve Havale/EFT ile guvenle odeme yapabilirsiniz.", 
        inline=False
    )
    embed.add_field(
        name="4. Garanti Ve Teknik Destek", 
        value="Tum urunlerimiz 2 yil resmi distributor garantilidir.", 
        inline=False
    )
    embed.set_footer(text="Aradiginiz cevabi bulamadiysaniz '!destek' komutunu kullanabilirsiniz.")
    
    await ctx.send(embed=embed)


@bot.command(name="destek")
async def destek(ctx, departman: str = None, *, detay: str = None):
    if departman is None:
        embed = discord.Embed(
            title="Alabilecegin Her Sey - Destek Merkezi",
            description="Lutfen sorununuzu ve departmani belirterek talep olusturun:\n\n"
                        "**Kullanim Formati:**\n`!destek <departman> <sorununuz>`\n\n"
                        "**Departmanlar:**\n"
                        "- `yazilim` : Web sitesi, giris ve odeme hatalari\n"
                        "- `satis` : Urunler, stok durumu ve siparis takibi",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
        return

    departman = departman.lower()

    if departman not in ["yazilim", "yazılım", "teknik", "satis", "satış", "urun", "ürün"]:
        await ctx.send("Hatali departman! Kullanim: `!destek yazilim <mesaj>` veya `!destek satis <mesaj>`")
        return

    if detay is None:
        await ctx.send("Lutfen sorununuzu da yazin. Ornek: `!destek yazilim Odeme sayfasinda hata aliyorum`")
        return

    
    baglanti = sqlite3.connect("destek_talepleri.db")
    imlec = baglanti.cursor()
    imlec.execute(
        "INSERT INTO talepler (kullanici_adi, kullanici_id, departman, mesaj) VALUES (?, ?, ?, ?)",
        (str(ctx.author), str(ctx.author.id), departman, detay)
    )
    baglanti.commit()
    baglanti.close()


    if departman in ["yazilim", "yazılım", "teknik"]:
        embed = discord.Embed(
            title="Yazilim & Teknik Destek Talebi Olusturuldu",
            description=f"**Kullanici:** {ctx.author.mention}\n**Sorun:** {detay}\n\nTalebiniz veritabanina kaydedildi ve Programci ekibimize iletildi.",
            color=discord.Color.red()
        )
        await ctx.send(content="Ilgili Departman: @Programcı", embed=embed)

    else:
        embed = discord.Embed(
            title="Satis & Urun Destek Talebi Olusturuldu",
            description=f"**Kullanici:** {ctx.author.mention}\n**Sorun:** {detay}\n\nTalebiniz veritabanina kaydedildi ve Satis ekibimize iletildi.",
            color=discord.Color.green()
        )
        await ctx.send(content="Ilgili Departman: @Satış Temsilcisi", embed=embed)

bot.run(config.TOKEN)
