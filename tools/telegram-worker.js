// Пример обработчика заявок: Cloudflare Worker -> Telegram-бот.
// 1) Создайте бота у @BotFather, добавьте его в чат/канал салона, узнайте chat_id.
// 2) Создайте Worker, вставьте этот код, в Settings → Variables добавьте секреты BOT_TOKEN и CHAT_ID
//    и переменную ALLOWED_ORIGIN (адрес сайта, например https://topdress-kzn.ru).
// 3) Адрес Worker впишите в assets/config.js → lead.endpoint.
export default {
  async fetch(req, env) {
    const cors = {
      'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });
    let d;
    try { d = await req.json(); } catch { return new Response('Bad JSON', { status: 400, headers: cors }); }
    if (!d.name || !d.phone) return new Response('Missing fields', { status: 400, headers: cors });
    const utm = d.utm && Object.keys(d.utm).length ? '\nUTM: ' + JSON.stringify(d.utm) : '';
    const text = '🤍 Заявка на примерку (TOPDRESS)\n' +
      'Имя: ' + d.name + '\nТелефон: ' + d.phone + '\nНаправление: ' + (d.direction || '—') +
      '\nДата: ' + (d.date || 'не указана') + (d.comment ? '\nКомментарий: ' + d.comment : '') + utm;
    const r = await fetch('https://api.telegram.org/bot' + env.BOT_TOKEN + '/sendMessage', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: env.CHAT_ID, text })
    });
    return new Response(r.ok ? 'ok' : 'telegram error', { status: r.ok ? 200 : 502, headers: cors });
  }
};
