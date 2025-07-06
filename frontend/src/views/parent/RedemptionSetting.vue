<template>
    <div class="container" style="align-items: center;">
        <div class="row">
            <div class="col" style="width: 100%;">
                <div class="nav-card-body">
                    <h2 class="welcome-text" style="font-size: 20px;"> 💵 Coin Redemption Settings</h2>
                    <button class="add-child-btn" @click="saveSettings" :disabled="saving"> 
                         {{ saving ? "Saving..." : "Save Settings" }}
                    </button>
                </div>
            </div>
        </div>
      <div class="row" style="border-spacing: 0.1rem;">
          <div class="col" style="width: 560px;">
            <div class="create-task" style="width: 560px;">
                    <!-- Exchange Rate Section -->
                      <div class="card">
                        <div class="card-header">
                        <span class="icon">💵</span>
                        <h2 class="welcome-text">Exchange Rate</h2>
                        </div>

                        <div class="form-group">
                        <label>1 Coin equals (in currency)</label>
                        <div class="input-with-icon">
                            
                            <input
                            v-model.number="exchangeRate"
                            type="number"
                            min="0.01"
                            step="0.01"
                            />
                        </div>
                        </div>

                        <div class="form-group">
                        <label>Currency</label>
                        <div class="input-with-icon">
                            
                            <select v-model="currency">
                            <option v-for="cur in currencies" :key="cur" :value="cur">{{ cur }}</option>
                            </select>
                        </div>
                        </div>

                        <div class="info-box">
                        
                        Current rate: 1 coin = {{ formattedRate }}
                        </div>
                    </div>
                </div>
          </div>
            <div class="col" style="width: 560px;">
               <div class="create-task" style="max-width: 560px;">
                    <!-- Approval Settings -->
                    <div class="card">
                      <h2 class="welcome-text"> ✔️ Approval Settings</h2>
                      <label class="switch">
                        <input type="checkbox" v-model="settings.requireApproval" />
                        <span class="slider"></span>
                        Require approval for all redemptions
                      </label>

                      <div v-if="!settings.requireApproval" class="sub-field">
                        <label>
                          Auto‑approve up to (coins)
                          <input class="box" type="number" min="1" v-model.number="settings.autoApprovalLimit" />
                        </label>
                      </div>

                      <label class="switch">
                        <input type="checkbox" v-model="settings.notifyOnRequest" />
                        <span class="slider"></span>
                        Notify me of redemption requests
                      </label>

                      <label class="switch">
                        Processing time
                        <select class="box" v-model="settings.processingTime">
                          <option v-for="t in processingTimes" :key="t" :value="t">{{ t }}</option>
                        </select>
                      </label>
                    </div>
                </div>
            </div>
              <div class="col" style="width: 100%;">
                <div class="create-task" style="max-width: 100%;">
                    
                <div class="redemption-card">
                    <h2 class="section-title">
                      <span class="emoji">🚀</span> Redemption Limits
                    </h2>

                    <div class="limits-grid">
                      <div class="limit-field">
                        <label for="daily"><span class="icon">📅</span> Daily limit (coins)</label>
                        <input type="number" id="daily" v-model.number="dailyLimit" min="0" />
                        <div class="hint">0 = no limit</div>
                      </div>

                      <div class="limit-field">
                        <label for="weekly"><span class="icon">📅</span> Weekly limit (coins)</label>
                        <input type="number" id="weekly" v-model.number="weeklyLimit" min="0" />
                        <div class="hint">0 = no limit</div>
                      </div>

                      <div class="limit-field">
                        <label for="monthly"><span class="icon">📆</span> Monthly limit (coins)</label>
                        <input type="number" id="monthly" v-model.number="monthlyLimit" min="0" />
                        <div class="hint">0 = no limit</div>
                      </div>
                    </div>

                    <hr />

                      <div class="toggle-row">
                        <label class="toggle-item">
                          <input type="checkbox" v-model="allowSavings" />
                          Allow exceeding limits for savings goals
                        </label>
                      </div>

                      <div class="toggle-row">
                        <label class="toggle-item">
                          <input type="checkbox" v-model="trackCategories" />
                          Track spending by categories
                        </label>
                      </div>
                  </div>
                </div>
            </div>
            <div class="col" style="width: 100%;">
              <div class="create-task" style="max-width: 100%;">
                    <div class="card">
                      <div class="card-header">
                        <h2 class="section-title"><span class="emoji">🔄</span>
                        Recent Redemption Requests</h2>
                        <button class="view-all-btn">
                          View All <span class="arrow">→</span>
                        </button>
                      </div>

                      <table class="requests-table">
                        <thead>
                          <tr>
                            <th>Child</th>
                            <th>Amount</th>
                            <th>Description</th>
                            <th>Status</th>
                            <th>Requested</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(req, i) in requests" :key="i">
                            <td>
                              <div class="child-info">
                                <div class="avatar" :style="{ backgroundColor: req.color }">
                                  {{ req.name.charAt(0) }}
                                </div>
                                <div>
                                  <strong>{{ req.name }}</strong>
                                  <div class="child-age">{{ req.age }} years old</div>
                                </div>
                              </div>
                            </td>
                            <td>
                              ⭐ <strong>{{ req.amount }}</strong>
                              <span class="usd">(${{ (req.amount / 100).toFixed(2) }})</span>
                            </td>
                            <td>{{ req.description }}</td>
                            <td>
                              <span class="status" :class="req.status.toLowerCase()">{{ req.status }}</span>
                            </td>
                            <td>{{ req.date }}</td>
                            <td>
                              <div v-if="req.status === 'Pending'" class="action-buttons">
                                <button class="btn approve" @click="approveRedemption(req)">Approve</button>
                                <button class="btn reject" @click="rejectRedemption(req)">Reject</button>
                              </div>
                              <div v-else class="btn status-pill">{{ req.status }}</div>
                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <div class="pagination">
                        <label>
                          Items per page:
                          <select v-model="itemsPerPage">
                            <option>5</option>
                            <option>10</option>
                          </select>
                        </label>
                        <span class="page-info">1–{{ requests.length }} of {{ requests.length }}</span>
                      </div>
                    </div>
              </div>

            </div>
            <div class="dashboard">
    <!-- Payment Methods -->
    <div class="payment-card" >
      <div class="card-header">
        <span class="emoji">🧾</span>
        <h2>Payment Methods</h2>
      </div>

      <div v-for="(method, i) in paymentMethods" :key="i" class="method-row">
        <div class="method-info">
          <span class="emoji">{{ method.icon }}</span>
          <div>
            <div class="method-title">{{ method.name }}</div>
            <div class="method-subtitle">{{ method.desc }}</div>
          </div>
        </div>
        <label class="switch">
          <input type="checkbox" v-model="method.enabled" />
          <span class="slider"></span>
        </label>
      </div>

      <div class="add-button green">
        ➕ Add Payment Method
      </div>
    </div>

    <!-- Spending Analytics -->
    <div class="payment-card" >
      <div class="card-header">
        <span class="emoji">📈</span>
        <h2>Spending Analytics</h2>
      </div>

      <div class="analytics-section">
        <div class="total">
          <div class="amount green-text">${{ totalRedeemed.toFixed(2) }}</div>
          <div class="label">Total Redeemed</div>
        </div>
        <div class="transactions">
          <div class="amount blue-text">{{ transactionCount }}</div>
          <div class="label">Transactions</div>
        </div>
      </div>

      <div class="categories">
        <div class="category-row" v-for="(item, i) in categories" :key="i">
          <span>{{ item.name }}</span>
          <span class="amount">${{ item.amount.toFixed(2) }}</span>
        </div>
      </div>

      <div class="add-button gray">
        📊 View Detailed Analytics
      </div>
    </div>
  </div>
          </div>
    </div>
    

</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const saving = ref(false)
const showSuccess = ref(false)
const successMessage = ref('')
const dailyLimit = ref(100)
const weeklyLimit = ref(300)
const monthlyLimit = ref(1000)
const allowSavings = ref(true)
const trackCategories = ref(true)

// reactive settings
const settings = reactive({
  exchangeRate: 0.10,
  currency: 'USD',
  requireApproval: false,
  autoApprovalLimit: 50,
  notifyOnRequest: true,
  processingTime: 'Within 24 hours',
  dailyLimit: 100,
  weeklyLimit: 300,
  monthlyLimit: 1000,
  allowSavingsOverride: true,
  trackSpendingCategories: true
})

// Mock data
const paymentMethods = ref([
  { name: 'Cash', desc: 'Direct cash payment', icon: '💵', enabled: true },
  { name: 'Digital Transfer', desc: 'Bank transfer or digital wallet', icon: '🏦', enabled: false },
  { name: 'Gift Cards', desc: 'Store gift cards or vouchers', icon: '🎁', enabled: true },
  { name: 'Experience Rewards', desc: 'Trips, activities, or experiences', icon: '✈️', enabled: false }
])

const totalRedeemed = ref(125.5)
const transactionCount = ref(12)

const categories = ref([
  { name: 'Toys & Games', amount: 45.0 },
  { name: 'Books', amount: 32.5 },
  { name: 'Art Supplies', amount: 28.0 },
  { name: 'Sports', amount: 20.0 }
])

const analytics = ref({
  totalRedeemed: 125.50,
  redemptionCount: 12,
  topCategories: [
    { name: 'Toys & Games', amount: 45.00 },
    { name: 'Books', amount: 32.50 },
    { name: 'Art Supplies', amount: 28.00 },
    { name: 'Sports', amount: 20.00 }
  ]
})

const exchangeRate = ref(2)
const currency = ref('INR')
const currencies = ['INR','USD','EUR','CAD','AUD']
const processingTimes = ['Immediately','Within 1 hour','Within 24 hours','Within 2-3 days','Within a week']

const formattedRate = computed(() =>
  new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency.value,
  }).format(exchangeRate.value)
)

const requests = ref([
  { name: 'Luna', age: 9, amount: 25, description: 'Art supplies', status: 'Pending', date: 'Jul 4, 6:38 PM', color: '#9C27B0' },
  { name: 'Harry', age: 12, amount: 50, description: 'Video game', status: 'Approved', date: 'Jul 3, 8:38 PM', color: '#2196F3' },
  { name: 'Luna', age: 9, amount: 15, description: 'Book series', status: 'Completed', date: 'Jul 1, 8:38 PM', color: '#9C27B0' },
  { name: 'Harry', age: 12, amount: 30, description: 'Sports equipment', status: 'Rejected', date: 'Jun 29, 8:38 PM', color: '#2196F3' },
])

const itemsPerPage = ref(5)

const formatCurrency = (amt:number) =>
  new Intl.NumberFormat('en-US',{style:'currency',currency:settings.currency}).format(amt)

const formatDate = (d:Date) =>
  new Intl.DateTimeFormat('en-US',{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}).format(d)

const statusClass = (s:string) =>
  ({'Pending':'pending','Approved':'approved','Rejected':'rejected','Completed':'completed'})[s]||''

async function saveSettings(){
  saving.value = true
  await new Promise(r=>setTimeout(r,1000))
  saving.value = false
  showSuccess.value = true
  successMessage.value = 'Settings saved'
}

async function approveRedemption(item:any){
  item.status='Approved'
  showSuccess.value=true
  successMessage.value='Approved'
}
async function rejectRedemption(item:any){
  item.status='Rejected'
  showSuccess.value=true
  successMessage.value='Rejected'
}
</script>

<style scoped>
.nav-card-body {
    background-color: white;
    border-radius: 15px;
    max-width: 100%;
    height: 50px;
    margin-top: 20px;
    margin-bottom: 5px;
    margin-left: 20px;
    margin-right: 20px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

}

.welcome-text {
  font-size: 20px;
  font-weight: bold;
  
  }

.add-child-btn {
  font-weight: bold;
  padding: 5px 5px;
  border: 2px solid;
  border-radius: 15px;
  cursor: pointer;
  font-size: 10px;
  background-color: rgb(235, 229, 229);
  margin: 20px;
}



.add-child-btn {
  font-weight: bold;
  padding: 10px 10px;
  border: 2px solid;
  border-radius: 15px;
  cursor: pointer;
  font-size: 15px;
  background-color: rgb(235, 229, 229);
}


.create-task {
    background-color: white;
    border-radius: 20px;
    height: auto;
    max-width: 750px;
    margin-top: 10px;
    margin-bottom: 20px;
    margin-left: 20px;
    margin-right: 5px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

  }

.create-task {
    background-color: white;
    border-radius: 20px;
    height: auto;
    max-width: 750px;
    margin-top: 10px;
    margin-bottom: 20px;
    margin-left: 20px;
    margin-right: 5px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

  }

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
  
}

.card {
  background: white;
  border: none;
  padding: 20px;
  width: 600px;
  margin-left: 2px;
  margin-right: 2px;
  font-family: sans-serif;
}


.card-header {
  font-size: 1.5rem;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header .icon {
  margin-right: 10px;
  font-size: 1.5rem;
  color: orange;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 6px;
  color: #555;
  font-weight: 500;
}

.input-with-icon {
  display: flex;
  align-items: center;
  border-radius: 15px;
  background: #fff;
  border-width: 200px;
}

.input-icon {
  font-size: 1.1rem;
  color: #666;
}

input,
select {
  border: none;
  outline: none;
  flex: 1;
  font-size: 1rem;
  background: transparent;
}

.info-box {
  background-color: #e6f1fb;
  border-radius: 8px;
  padding: 12px;
  font-size: 0.95rem;
  color: #1a73e8;
  display: flex;
  align-items: center;
}

.info-icon {
  margin-right: 8px;
  font-size: 1.2rem;
}


.switch {
  margin: 20px;
}

.slider {
  margin-left: 20px;
}

.sub-field {
  margin: 20px;
}

.box {
  width: 400px;
  height: 40px;
  margin-top: 10px;
  border-style: groove;
  border-radius: 10px;
}

.redemption-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  width: 100%;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.limits-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.limit-field {
  flex: 1;
  min-width: 200px;
}

.limit-field label {
  display: block;
  font-weight: bold;
  margin-bottom: 6px;
}

.limit-field input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.hint {
  font-size: 0.85rem;
  color: gray;
  margin-top: 4px;
}

.toggle-row {
  margin-top: 12px;
  display: flex;
  align-items: center;
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 1rem;
}


.select-group label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #666;
}

.card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  margin: 1rem auto;
  overflow-x: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.4rem;
}

.view-all-btn {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  cursor: pointer;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.requests-table th,
.requests-table td {
  padding: 0.75rem;
  text-align: left;
  vertical-align: middle;
  border-bottom: 1px solid #eee;
}

.child-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #fff;
  display: grid;
  place-content: center;
  font-weight: bold;
}

.child-age {
  font-size: 0.8rem;
  color: #777;
}

.usd {
  color: #777;
  font-size: 0.85rem;
  margin-left: 0.3rem;
}

.status {
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  font-weight: 500;
  font-size: 0.85rem;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.approved {
  background: #e3f2fd;
  color: #1976d2;
}

.status.completed {
  background: #d4edda;
  color: #2e7d32;
}

.status.rejected {
  background: #f8d7da;
  color: #c62828;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  font-weight: bold;
  font-size: 0.85rem;
  border: none;
  cursor: pointer;
}

.approve {
  background-color: #d4edda;
  color: #2e7d32;
}

.reject {
  background-color: #f8d7da;
  color: #c62828;
}

.status-pill {
  border: 1px solid #aaa;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  background: white;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.pagination select {
  margin-left: 0.5rem;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.dashboard {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  margin-left: 20px;
  margin-right: 20px;
}

.payment-card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  flex: 1;
  min-width: 360px;
  max-width: 49%;
}

.method-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid #eee;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.method-title {
  font-weight: bold;
}

.method-subtitle {
  font-size: 0.85rem;
  color: #777;
}
.switch input:checked + .slider {
  background-color: #4caf50;
}
.switch input:checked + .slider::before {
  transform: translateX(18px);
}
.add-button {
  margin-top: 1rem;
  background: #e8f5e9;
  padding: 0.8rem;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
  border: 1px solid #c8e6c9;
}

.add-button.gray {
  background: #f5f5f5;
  border: 1px solid #ddd;
}
.analytics-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.total, .transactions {
  text-align: center;
}

.amount {
  font-size: 1.3rem;
  font-weight: bold;
}

.green-text {
  color: #4caf50;
}
.blue-text {
  color: #42a5f5;
}

.label {
  font-size: 0.85rem;
  color: #777;
}

.categories {
  margin-top: 1rem;
}

.category-row {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0;
  font-size: 0.95rem;
}
</style>