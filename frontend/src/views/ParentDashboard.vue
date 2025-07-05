<template>
    <div class="parent-container">
      <div class="nav-card-body">
        <span><h2 style="margin: 15px;">Welcome back, {{ parent.name }}<button class="btn btn-primary" @click="goToAddChild" style="margin-left: 750px;"> + Add Child</button></h2></span>
      </div>
      <div>
        <section id="P-features" class="P-features">
          <div class="container">
            <div class="P-features-grid">
              <div class="P-feature-card" v-for="feature in features" :key="feature.id" @click="() => router.push(feature.route)">
                <div class="P-feature-icon">{{ feature.icon }} {{ feature.title }}</div>           
              </div>
            </div>
          </div>
        </section>
      </div>
      <div>
          <section id="childcard" class="childcard" >
            <div class="container">
              <div class="childcard-grid" style="transform: scale(0.7); transform-origin: top left;">
                <div class="child-card" v-for=" child in children" :key="child.id">
                  <div class="row">
                    <div class="col-sm-6 col-md-4">
                      <div class="head">
                        <div class="avatar" :style="{ backgroundColor: child.avatarColor}">{{ child.initials }} </div>
                          <div class="childname">
                            <h1 class="text-xl font-semibold mb-1">{{ child.name }}</h1>
                            <div style="font-weight: lighter;">{{ child.age }} year old</div>
                          </div>
                      </div> 
                        <div class="container">
                          <div class="row" style="margin-top: 22px;">
                            <div class="stats-container">
                              <div class="stat-box">
                                <div class="stat-number coins">{{ child.coinBalance }}</div>
                                <div class="stat-label">Coins</div>
                              </div>
                              <div class="stat-box">
                                <div class="stat-number task">{{ child.completedTasks }}</div>
                                <div class="stat-label">Task Done</div>
                              </div>
                            </div>
                            <div class="activity-goals">
                                <!-- Recent Activity -->
                              <section class="section" style="margin-top: 20px;">
                                <h3 style="text-align: left; font-size: 20px;color: royalblue;">Recent Activity</h3>
                                <div v-for="activity in child.recentActivity" :key="activity.id">
                                  <div class="activity-item" >
                                    <span class="icon success" style="margin-bottom: 15px;">{{ activity.icon }}</span>
                                    <div class="activity-content" style="margin-left: 20px;">
                                      <div class="title">{{ activity.title }}</div>
                                      <div class="time">{{ formatRelativeTime(activity.timestamp) }}</div>
                                    </div>
                                    <span class="points" v-if="activity.coins" size="x-small" color="warning"> +{{ activity.coins }}</span>
                                  </div>
                                </div>
                              </section>
                                <!-- Current Goals -->
                              <section class="section">
                                <h3 style="text-align: left; font-size: 20px; color: royalblue;">Current Goals</h3>
                                <div v-if="child.currentGoals.length > 0">
                                <!-- Goal 1 -->
                                  <div class="goal-card" v-for="goal in child.currentGoals" :key="goal.id">
                                    <div class="goal-header">
                                      <span class="goal-icon purple">{{ goal.icon }}</span>
                                      <span class="goal-title">{{ goal.name }}</span>
                                      <span class="goal-progress">{{ goal.saved }}/{{ goal.target }}</span>
                                    </div>
                                    <div class="progress-bar purple"> 
                                      <div class="fill" :style="{ width: Math.min((goal.saved/goal.target)*100, 100)+ '%', backgroundColor: goal.color}"></div>
                                    </div>
                                  </div>            
                                </div>
                                <button class="btn-tonal" @click="viewChildProgress(child)">
                                  <i class="mdi mdi-eye"></i>
                                  Details
                                </button>
                              </section>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>   
    </div>

</template>

<script setup lang="ts">

import { ref } from 'vue'
import type { Parent, Child} from  '@/types'
import { useRouter } from 'vue-router'
import { formatDistanceToNow } from 'date-fns'



// Reactive data




// Parent data
const parent = ref<Parent>({
  id: '1',
  name: 'Priya',
  email: 'priya@example.com',
  children: ['1', '2'],
  createdAt: new Date(),
  updatedAt: new Date()
})

const router = useRouter();
function goToAddChild() {
  router.push('/addchild')
}

// feature data
const features = ref([
  {
    id: 1,
    icon: '➕',
    title: 'Assign Task',
    route:  '/assigntask'
    
  },
  {
    id: 2,
    icon: '🏆',
    title: 'Award Bonus',
    route:  ''
    
  },
  {
    id: 3,
    icon: '🎁',
    title: 'Redumption',
    route:  '/redeptionsetting'
    
  },
  {
    id: 4,
    icon: '📊',
    title: 'Reports',
    route:  '/childprogress'
    
  }
])


// Children data
const children = ref<Child[]>([
  {
    id: '1',
    name: 'Luna',
    age: 9,
    email: 'luna@example.com',
    initials: 'L',
    avatarColor: 'purple',
    coinBalance: 125,
    completedTasks: 23,
    currentGoals: [
      {
        id: '1',
        name: 'Magic Hat',
        target: 50,
        saved: 35,
        icon: '🎩',
        color: 'purple'
      },
      {
        id: '2',
        name: 'Art Supplies',
        target: 30,
        saved: 18,
        icon: '🎨',
        color: 'orange'
      }
    ],
    recentActivity: [
      {
        id: '1',
        title: 'Completed homework',
        icon: '✅',
        color: 'success',
        coins: 15,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        id: '2',
        title: 'Finished "Smart Shopping" module',
        icon: '🎓',
        color: 'info',
        coins: 25,
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      }
    ],
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    id: '2',
    name: 'Harry',
    age: 12,
    email: 'harry@example.com',
    initials: 'H',
    avatarColor: 'blue',
    coinBalance: 280,
    completedTasks: 24,
    currentGoals: [
      {
        id: '3',
        name: 'Headphones',
        target: 120,
        saved: 95,
        icon: '🎧',
        color: 'blue'
      }
    ],
    recentActivity: [
      {
        id: '3',
        title: 'Created budget plan',
        icon: '📝',
        color: 'primary',
        coins: 20,
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
      },
      {
        id: '4',
        title: 'Cleaned room',
        icon: '🧹',
        color: 'success',
        coins: 10,
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      }
    ],
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date()
  }
])

function formatRelativeTime(timestamp: Date | string | number): string {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
}

const viewChildProgress = (child: Child) => {
  router.push(`/childprogress/${child.id}`)
}

</script>

<style scoped>
  .nav-card-body {
    background-color: white;
    border-radius: 20px;
    height: 80px;
    margin-top: 20px;
    margin-bottom: 20px;
    margin-left: 50px;
    margin-right: 50px;
    color: var(--primary-orange);
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
  }

/* Features Section */
.P-features {
  padding: var(--spacing-s) 0;

  
}

.P-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--spacing-xl);
  
}

.P-feature-card {
  
  padding: var(--spacing-s);
  border-radius: var(--radius-lg);
  text-align: center;
  box-shadow: var(--shadow-lg);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  background-color: aqua;
}

.P-feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-orange);
}

.P-feature-icon {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

/* child view */

.childcard {
  padding: var(--spacing-l);
  font-size: x-large;
  margin-left: 0%;
  margin: 10px;
  margin-top: 20px;

}

.childcard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-l);
}

.child-card {
  background: var(--white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  text-align: center;
  box-shadow: var(--shadow-lg);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  width: 500px;
  
}



.child-card p {
  color: var(--medium-gray);
  font-family: var(--font-secondary);
}

.head {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: large;
}

.avatar{
  width: 90px;
  height: 90px;
  border-radius: 100%;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin-right: 12px;
}

.childname{
  font-weight: 700;
  font-size: 1.5rem;
  }

.stats-container{
  display: flex;
  justify-content: center;
  gap: 250px;
  padding: 10px;
}

.stat-box{
  text-align: center;
}

.stat-number{
  font-size: 20px;
  
}

.coins{
  color: orange;
  font-size: xxx-large;
  font-weight: lighter;
}

.task{
  color: green;
  font-size: xxx-large;
  font-weight: lighter;
}


/* recent activity */

.activity-goals {
  font-family: 'Courier New', Courier, monospace;
  max-width: 400px;
  margin: 0; 
  font-size: 20px;
}

.section {
  margin-bottom: 10px;
}

h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: #333;
}

/* === Activity === */
.activity-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  text-align: left;
  margin-top: 20px;
  
}

.icon {
  font-size: 18px;
  margin-right: 10px;
}

.success {
  color: green;
}

.activity-content {
  flex-grow: 1;
}

.title {
  font-weight: bold;
  color: #333;
}

.time {
  font-size: 12px;
  color: gray;
}

.points {
  font-size: 13px;
  background: #ffe8c8;
  color: #f39c12;
  padding: 2px 8px;
  border-radius: 12px;
}

.points.orange {
  background: #ffe2cc;
  color: #e67e22;
}

/* === Goals === */
.goal-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 10px 14px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.goal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.goal-icon {
  font-size: 18px;
  margin-right: 8px;
}

.goal-title {
  flex-grow: 1;
  font-weight: bold;
  color: #333;
}

.goal-progress {
  font-size: 13px;
  color: #666;
}

/* Progress Bar */
.progress-bar {
  height: 6px;
  background: #eee;
  border-radius: 4px;
  margin-top: 6px;
  overflow: hidden;
}

.progress-bar .fill {
  height: 100%;
  border-radius: 4px;
}

.purple .fill {
  background: #9b59b6;
}

.orange .fill {
  background: #f39c12;
}

@media(max-width: 768px){
  .desktop-nav {
    display: none;
  }

  .mobile-nav {
    display: block;
  }
}

</style>