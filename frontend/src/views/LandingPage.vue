<template>
  <div class="main">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="logo">
          <span class="logo-icon">🪙</span>
          <span class="logo-text">CoinCraft</span>
        </div>
        <div class="nav-buttons">
          <button class="btn btn-outline" @click="$router.push('/auth/login')">Sign In</button>
          <button class="btn btn-primary" @click="$router.push('/auth/register')">Join the Fun!</button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="section hero">
      <div class="container hero-container">
        <div class="hero-content">
          <div class="hero-badge">
            <span class="badge-icon">⭐</span>
            <span>Learn Money Skills While Having Fun!</span>
          </div>
          <h1 class="hero-title">
            Welcome to <span class="highlight">CoinCraft!</span>
            <br>Where Money Learning is <span class="highlight-2">Super Fun!</span>
          </h1>
          <p class="hero-description">
            Join thousands of kids learning about money through exciting games, 
            cool challenges, and awesome rewards! 🎮💰
          </p>
          <div class="hero-buttons">
            <button class="btn btn-large btn-primary" @click="$router.push('/auth/register')">
              <span class="btn-icon">🚀</span>
              Start Your Adventure!
            </button>
            <button class="btn btn-large btn-secondary" @click="scrollToFeatures">
              <span class="btn-icon">👀</span>
              See What's Cool!
            </button>
          </div>
          <div class="hero-stats">
            <div class="stat">
              <span class="stat-number">10,000+</span>
              <span class="stat-label">Happy Kids</span>
            </div>
            <div class="stat">
              <span class="stat-number">500+</span>
              <span class="stat-label">Fun Games</span>
            </div>
            <div class="stat">
              <span class="stat-number">95%</span>
              <span class="stat-label">Love It!</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-elements">
            <div class="floating-coin coin-1">🪙</div>
            <div class="floating-coin coin-2">💰</div>
            <div class="floating-coin coin-3">⭐</div>
            <div class="floating-coin coin-4">🎯</div>
            <div class="floating-coin coin-5">🏆</div>
            <div class="floating-coin coin-6">💎</div>
          </div>
          <div class="hero-character">
            <div class="character-circle">
              <span class="character-emoji">🦸‍♀️</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="section features">
      <div class="container">
        <h2 class="section-title">Why Kids Love CoinCraft! 🌟</h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="section cta">
      <div class="container">
        <div class="cta-content">
          <h2>Ready to Start Your Money Adventure? 🚀</h2>
          <p>Join thousands of kids who are already having fun while learning!</p>
          <button class="btn btn-large btn-primary" @click="$router.push('/auth/register')">
            <span class="btn-icon">✨</span>
            Join CoinCraft Now!
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const features = ref([
  {
    id: 1,
    icon: '🎮',
    title: 'Super Fun Games',
    description: 'Play awesome games while learning about saving, spending, and earning money!'
  },
  {
    id: 2,
    icon: '🏆',
    title: 'Cool Rewards',
    description: 'Earn coins, badges, and trophies as you complete challenges and learn new skills!'
  },
  {
    id: 3,
    icon: '👨‍👩‍👧‍👦',
    title: 'Family Fun',
    description: 'Parents can join in and help you on your money learning adventure!'
  },
  {
    id: 4,
    icon: '📚',
    title: 'Easy Learning',
    description: 'Learn step-by-step with fun stories and simple explanations!'
  }
])

const scrollToFeatures = () => {
  const featuresElement = document.getElementById('features')
  if (featuresElement) {
    featuresElement.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'slideInUp 0.6s ease-out'
      }
    })
  }, observerOptions)

  // Observe feature cards
  const featureCards = document.querySelectorAll('.feature-card')
  featureCards.forEach(card => {
    observer.observe(card)
  })
})
</script>

<style scoped>
/* Hero Section */
.hero {
  padding: var(--spacing-xxl) 0;
  min-height: 80vh;
  display: flex;
  align-items: center;
}

.hero-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xxl);
  align-items: center;
}

.hero-content {
  animation: slideInLeft 1s ease-out;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: var(--light-yellow);
  color: var(--primary-orange);
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-full);
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
  /* animation: pulse 2s infinite; */
}

.badge-icon {
  font-size: 1.2em;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: var(--spacing-lg);
  color: var(--dark-gray);
}

.highlight {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.highlight-2 {
  background: var(--gradient-secondary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.25rem;
  color: var(--medium-gray);
  margin-bottom: var(--spacing-xl);
  font-family: var(--font-secondary);
}

.hero-buttons {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.hero-stats {
  display: flex;
  gap: var(--spacing-xl);
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-orange);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--medium-gray);
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 400px;
  animation: slideInRight 1s ease-out;
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
}

.floating-coin {
  position: absolute;
  font-size: 2rem;
  animation: float 3s ease-in-out infinite;
}

.coin-1 { top: 10%; left: 20%; animation-delay: 0s; }
.coin-2 { top: 20%; right: 10%; animation-delay: 0.5s; }
.coin-3 { top: 40%; left: 10%; animation-delay: 1s; }
.coin-4 { top: 60%; right: 20%; animation-delay: 1.5s; }
.coin-5 { bottom: 20%; left: 30%; animation-delay: 2s; }
.coin-6 { bottom: 10%; right: 30%; animation-delay: 2.5s; }

.hero-character {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.character-circle {
  width: 200px;
  height: 200px;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-colored);
  animation: bounce 2s infinite;
}

.character-emoji {
  font-size: 4rem;
}

/* Features Section */
.features {
  padding: var(--spacing-xxxl) 0;
  background: var(--white);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}

.feature-card {
  background: var(--white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-orange);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-lg);
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--dark-gray);
}

.feature-card p {
  color: var(--medium-gray);
  font-family: var(--font-secondary);
}

/* CTA Section */
.cta {
  padding: var(--spacing-xxl) 0;
  background: var(--gradient-primary);
  color: var(--white);
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--spacing-lg);
}

.cta-content p {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-xl);
  font-family: var(--font-secondary);
}

.cta .btn-primary {
  background: var(--white);
  color: var(--primary-orange);
}

.cta .btn-primary:hover {
  background: var(--light-gray);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
    gap: var(--spacing-xl);
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: var(--spacing-xl) 0;
  }
  
  .hero-title {
    font-size: 1.75rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
}
</style>