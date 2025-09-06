<template>
  <div class="forbidden-view">
    <div class="error-container">
      <h1>Нет доступа</h1>
      
      <p>
        У вас нет активной подписки. Чтобы читать книги, 
        оформите подписку через Telegram-бот и попробуйте снова.
      </p>
      
      <div class="help-text">
        <p>
          Если у вас есть подписка, убедитесь, что вы перешли по ссылке 
          из Telegram-бота с правильным параметром uid.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Forbidden view component
</script>

<style scoped>
.forbidden-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.error-container {
  text-align: center;
  max-width: 500px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.error-container h1 {
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-container p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.help-text {
  margin-top: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #007acc;
}

.help-text p {
  margin: 0;
  font-size: 0.9em;
  color: #555;
}
</style>