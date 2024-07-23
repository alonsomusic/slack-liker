# Используем официальный Node.js образ в качестве базового
FROM node:16-alpine

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Копируем package.json и package-lock.json
COPY package*.json ./

COPY .env ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальной исходный код
COPY . .

# Указываем команду для запуска приложения
CMD ["node", "app.js"]