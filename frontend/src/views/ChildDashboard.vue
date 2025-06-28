<template>
    

    

    <!-- Main Content Area -->
    <main class="content" :class="{ 'sidebar-collapsed': sidebarCollapsed, 'mobile-view': isMobileView }">
      <div class="dashboard">
        <!-- Dummy content box -->
        <div class="dummy-content">
          <h2>Dashboard Content</h2>
          <p>This is where the main dashboard content will go. The Activity Hub, Piggy Bank, Goals, and Shop features will be redesigned here.</p>
          <div class="placeholder-box">
            <div class="placeholder-item">Activity Hub</div>
            <div class="placeholder-item">My Piggy Bank</div>
            <div class="placeholder-item">My Goals</div>
            <div class="placeholder-item">Shop</div>
          </div>
        </div>
      </div>
    </main>

    
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const sidebarCollapsed = ref(false)
const isMobileView = ref(false)

const checkScreenSize = () => {
  const width = window.innerWidth
  const wasMobileView = isMobileView.value
  
  if (width <= 768) {
    isMobileView.value = true
    // Force collapse sidebar on mobile
    if (!wasMobileView) {
      sidebarCollapsed.value = true
    }
  } else if (width <= 1024) {
    isMobileView.value = false
    // Force collapse sidebar on tablet
    if (wasMobileView) {
      sidebarCollapsed.value = true
    }
  } else {
    isMobileView.value = false
    // Reset to expanded on desktop if coming from mobile/tablet
    if (wasMobileView) {
      sidebarCollapsed.value = false
    }
  }
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const navigateToProfile = () => {
  console.log('Navigate to profile page')
}

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
})
</script>

<style scoped>
/* CSS Variables */
:root {
  --primary-blue: #3b82f6;
  --light-blue: #dbeafe;
  --light-yellow: #fef3c7;
  --primary-orange: #ff6b35;
  --light-orange: #fff5f2;
  --dark-gray: #2d3748;
  --medium-gray: #718096;
  --light-gray: #e2e8f0;
  --white: #ffffff;
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-xxl: 3rem;
  --spacing-xxxl: 4rem;
  
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 50%;
  
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
  --gradient-primary: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
}

/* Desktop Navigation with Profile */
.desktop-nav {
  display: block;
  background-color: var(--white);
  border-bottom: 1px solid var(--light-gray);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: var(--spacing-sm) 0;
  height: 60px;
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--primary-orange);
}

.logo-icon {
  font-size: 1.5rem;
}

.nav-profile {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  cursor: pointer;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
}

.nav-profile:hover {
  background-color: var(--light-gray);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid var(--primary-blue);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.welcome-text {
  font-weight: 600;
  color: var(--dark-gray);
  font-size: 1rem;
}

.coin-balance {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: var(--light-yellow);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  border: 2px solid var(--primary-orange);
}

.coin-icon {
  font-size: 1rem;
}

.balance {
  font-weight: 700;
  color: var(--primary-orange);
  font-size: 1rem;
}

/* Collapsible Sidebar */
.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  width: 250px;
  height: calc(100vh - 60px);
  background: var(--white);
  border-right: 1px solid var(--light-gray);
  transition: width 0.3s ease;
  z-index: 999;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

/* Mobile view sidebar - stacked layout */
.sidebar.mobile-view {
  width: 70px;
}

.sidebar.mobile-view.collapsed {
  width: 250px;
}

.sidebar-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--light-gray);
}

.collapse-btn {
  width: 100%;
  padding: var(--spacing-sm);
  background: var(--light-gray);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.collapse-btn:hover {
  background: var(--medium-gray);
  color: var(--white);
}

.chevron-icon {
  font-size: 1.5rem;
  font-weight: bold;
  font-family: monospace;
}

.sidebar-nav {
  padding: var(--spacing-md) 0;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  text-decoration: none;
  color: var(--dark-gray);
  transition: all 0.3s ease;
  white-space: nowrap;
  border-left: 3px solid transparent;
}

/* Mobile view - stacked layout for sidebar items */
.sidebar.mobile-view .sidebar-item {
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-sm);
  text-align: center;
}

.sidebar.mobile-view.collapsed .sidebar-item {
  flex-direction: row;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  text-align: left;
}

.sidebar-item:hover {
  background: var(--light-orange);
  color: var(--primary-orange);
  border-left-color: var(--primary-orange);
}

.sidebar-item.active {
  background: var(--light-orange);
  color: var(--primary-orange);
  border-left-color: var(--primary-orange);
  font-weight: 600;
}

.sidebar-icon {
  font-size: 1.25rem;
  min-width: 24px;
  text-align: center;
}

.sidebar-text {
  font-weight: 500;
  opacity: 1;
  transition: opacity 0.3s ease;
  font-size: 0.9rem;
}

/* Hide text when collapsed (except in mobile view) */
.sidebar.collapsed:not(.mobile-view) .sidebar-text {
  opacity: 0;
}

/* In mobile view, text is always visible but positioned differently */
.sidebar.mobile-view .sidebar-text {
  opacity: 1;
  font-size: 0.75rem;
}

/* Content Area */
.content {
  margin-left: 250px;
  margin-top: 60px;
  padding: var(--spacing-lg);
  transition: margin-left 0.3s ease;
  min-height: calc(100vh - 60px);
  background: #f8f9fa;
}

.content.sidebar-collapsed {
  margin-left: 70px;
}

/* Mobile view content adjustments */
.content.mobile-view {
  margin-left: 70px;
}

.content.mobile-view.sidebar-collapsed {
  margin-left: 250px;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

/* Dummy Content Styles */
.dummy-content {
  background: var(--white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-xl);
}

.dummy-content h2 {
  color: var(--dark-gray);
  margin-bottom: var(--spacing-lg);
  font-size: 1.5rem;
}

.dummy-content p {
  color: var(--medium-gray);
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

.placeholder-box {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.placeholder-item {
  background: var(--light-gray);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: 600;
  color: var(--dark-gray);
  border: 2px dashed var(--medium-gray);
}

/* Mobile Bottom Navigation */
.mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--white);
  border-top: 1px solid var(--light-gray);
  z-index: 1000;
  padding: var(--spacing-sm) 0;
}

.bottom-nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  max-width: 100%;
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--medium-gray);
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
  min-width: 60px;
}

.bottom-nav-item.active,
.bottom-nav-item:hover {
  color: var(--primary-orange);
  background-color: var(--light-orange);
}

.bottom-nav-item .nav-icon {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-xs);
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .desktop-nav,
  .sidebar {
    display: none;
  }
  
  .content {
    margin-left: 0 !important;
    margin-top: 0;
    padding-bottom: 100px;
  }
  
  .mobile-bottom-nav {
    display: block;
  }
  
  .nav-profile {
    gap: var(--spacing-sm);
  }
  
  .welcome-text {
    font-size: 0.9rem;
  }
  
  .coin-balance {
    padding: var(--spacing-xs) var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 var(--spacing-md);
  }
  
  .logo-text {
    display: none;
  }
  
  .nav-profile {
    gap: var(--spacing-xs);
  }
  
  .welcome-text {
    display: none;
  }
}
</style>