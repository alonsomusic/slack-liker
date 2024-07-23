const { App } = require('@slack/bolt');
require('dotenv').config();

// Загружаем переменные окружения
const userToken = process.env.SLACK_USER_TOKEN;
const appToken = process.env.SLACK_APP_TOKEN;
const channelId = process.env.SLACK_CHANNEL_ID;

// Инициализация приложения Bolt
const app = new App({
  token: userToken,
  appToken: appToken,
  socketMode: true,
});

processedMessages = new Set()

// Обработка сообщений
app.message(async ( event ) => {
  const { message, say } = event

  console.log('Event: ', event.event)
//   console.log('Received message:', message); // Логирование входящих сообщений

  if (message.channel === channelId && !message.subtype) {
    if (processedMessages.has(message.ts)) {
        return
      }

    processedMessages.add(message.ts)

    try {
      await app.client.reactions.add({
        token: userToken,
        channel: message.channel,
        name: 'heart',
        timestamp: message.ts,
      });
      console.log(`Добавлена реакция сердца к новому сообщению с timestamp ${message.ts}`);
    } catch (error) {
      console.error(`Ошибка при добавлении реакции: ${error.message}`);
    }
  } else {
    console.log('Сообщение не соответствует условиям для добавления реакции.');
  }
});

(async () => {
  // Запускаем приложение
  await app.start();
  console.log('Slack app is running!');
})();
