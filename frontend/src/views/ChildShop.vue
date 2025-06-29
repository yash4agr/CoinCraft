<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 p-4 lg:pl-64 pt-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-shopping-bag-fill text-indigo-500 mr-3"></i>
          Coin Shop
        </h1>
        <p class="text-gray-600 text-lg">Spend your coins on awesome rewards!</p>
      </div>

      <!-- Shop Items -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Shop Item -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
          <div class="text-center">
            <div class="text-6xl mb-4">🎨</div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Art Supplies</h3>
            <p class="text-gray-600 mb-4">Get creative with new art supplies!</p>
            <div class="text-2xl font-bold text-indigo-500 mb-4">
              <i class="ri-coins-fill mr-1"></i>50 coins
            </div>
            <button class="bg-indigo-500 hover:bg-indigo-600 text-white px-6 py-2 rounded-full transition-colors w-full">
              <i class="ri-shopping-cart-line mr-2"></i>Buy Now
            </button>
          </div>
        </div>

        <!-- Shop Item -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
          <div class="text-center">
            <div class="text-6xl mb-4">📚</div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">New Book</h3>
            <p class="text-gray-600 mb-4">Pick a fun book to read!</p>
            <div class="text-2xl font-bold text-green-500 mb-4">
              <i class="ri-coins-fill mr-1"></i>30 coins
            </div>
            <button class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-full transition-colors w-full">
              <i class="ri-shopping-cart-line mr-2"></i>Buy Now
            </button>
          </div>
        </div>

        <!-- Shop Item -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
          <div class="text-center">
            <div class="text-6xl mb-4">🍦</div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Ice Cream Treat</h3>
            <p class="text-gray-600 mb-4">Enjoy a delicious ice cream!</p>
            <div class="text-2xl font-bold text-pink-500 mb-4">
              <i class="ri-coins-fill mr-1"></i>20 coins
            </div>
            <button class="bg-pink-500 hover:bg-pink-600 text-white px-6 py-2 rounded-full transition-colors w-full">
              <i class="ri-shopping-cart-line mr-2"></i>Buy Now
            </button>
          </div>
        </div>

        <!-- Shop Item -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
          <div class="text-center">
            <div class="text-6xl mb-4">🎮</div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Game Time</h3>
            <p class="text-gray-600 mb-4">Extra 30 minutes of game time!</p>
            <div class="text-2xl font-bold text-purple-500 mb-4">
              <i class="ri-coins-fill mr-1"></i>40 coins
            </div>
            <button class="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-full transition-colors w-full">
              <i class="ri-shopping-cart-line mr-2"></i>Buy Now
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Shop logic will go here
</script> 