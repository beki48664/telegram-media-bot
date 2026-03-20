const { Telegraf } = require('telegraf');
const axios = require('axios');

// Bot tokenini @BotFather dan oling va bu yerga yozing
const bot = new Telegraf('8064305593:AAHI5ytBdKajbpxatcp0nUObQYJD70nB7pE');

bot.start((ctx) => {
  ctx.reply('Salom! Qo\'shiq nomini yoki ijrochini yozing, men sizga musiqalarni topib beraman. 🎵');
});

bot.on('text', async (ctx) => {
  const query = ctx.message.text;
  const loadingMsg = await ctx.reply(`"${query}" qidirilmoqda... ⏳`);
  
  try {
    // iTunes API orqali musiqalarni qidirish
    const res = await axios.get(`https://itunes.apple.com/search?term=${encodeURIComponent(query)}&entity=song&limit=5`);
    const songs = res.data.results;
    
    if (songs.length === 0) {
      return ctx.telegram.editMessageText(
        ctx.chat.id, 
        loadingMsg.message_id, 
        null, 
        'Kechirasiz, bunday musiqa topilmadi. 😔'
      );
    }

    await ctx.telegram.deleteMessage(ctx.chat.id, loadingMsg.message_id);

    // Natijalarni yuborish
    for (const song of songs) {
      const caption = `🎵 <b>${song.trackName}</b>\n👤 ${song.artistName}\n💿 ${song.collectionName || 'Noma\'lum'}`;
      
      if (song.previewUrl) {
        await ctx.replyWithAudio(
          { url: song.previewUrl }, 
          { caption: caption, parse_mode: 'HTML' }
        );
      } else {
        await ctx.reply(caption, { parse_mode: 'HTML' });
      }
    }
  } catch (error) {
    console.error(error);
    ctx.reply('Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko\'ring. ⚠️');
  }
});

bot.launch().then(() => console.log('Bot ishga tushdi! 🚀'));

// Dastur to'xtatilganda botni ham to'xtatish
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
