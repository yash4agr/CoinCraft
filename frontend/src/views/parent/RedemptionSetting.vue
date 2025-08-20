<template>
  <v-container fluid class="pa-4">
    <!-- Header -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>
              <v-row
                class="align-center"
                align="center"
                justify="space-between"
                no-gutters
              >
                <!-- Icon + Title -->
                <v-col cols="12" md="auto" class="d-flex align-center mb-3 mb-md-0">
                  <v-icon class="me-2" color="success">mdi-cash-multiple</v-icon>
                  <span class="text-h6">Coin Redemption Settings</span>
                </v-col>

                <!-- Button -->
                <v-col cols="12" md="auto" class="text-md-right">
                  <v-btn
                    block
                    color="primary"
                    prepend-icon="mdi-content-save"
                    @click="saveSettings"
                    :loading="saving"
                  >
                    Save Settings
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>


    <v-row>
      <!-- Exchange Rate Settings -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="orange">mdi-swap-horizontal</v-icon>
            Exchange Rate
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model.number="settings.exchange_rate"
              label="1 Coin equals (in currency)"
              type="number"
              step="0.01"
              min="0.01"
              prepend-inner-icon="mdi-currency-usd"
              variant="outlined"
              :rules="[rules.required, rules.positive]"
              class="mb-3"
            />
            
            <v-select
              v-model="settings.currency"
              label="Currency"
              :items="currencies"
              prepend-inner-icon="mdi-cash"
              variant="outlined"
              class="mb-3"
            />
            
            <v-alert type="info" variant="tonal" density="compact">
              Current rate: 1 coin = {{ formatCurrency(settings.exchange_rate) }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Approval Settings -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="purple">mdi-check-circle</v-icon>
            Approval Settings
          </v-card-title>
          <v-card-text>
            <v-switch
              v-model="settings.require_approval"
              label="Require approval for all redemptions"
              color="primary"
              class="mb-3"
            />
            
            <v-expand-transition>
              <div v-if="!settings.require_approval">
                <v-text-field
                  v-model.number="settings.auto_approval_limit"
                  label="Auto-approve up to this amount (coins)"
                  type="number"
                  min="1"
                  prepend-inner-icon="mdi-star"
                  variant="outlined"
                  hint="Redemptions above this amount will require approval"
                  persistent-hint
                  class="mb-3"
                />
              </div>
            </v-expand-transition>
            
            <v-switch
              v-model="settings.notify_on_request"
              label="Notify me of redemption requests"
              color="primary"
              class="mb-3"
            />
            
            <v-select
              v-model="settings.processing_time"
              label="Expected processing time"
              :items="processingTimes"
              prepend-inner-icon="mdi-clock"
              variant="outlined"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Redemption Limits -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="warning">mdi-speedometer</v-icon>
            Redemption Limits
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="settings.daily_limit"
                  label="Daily limit (coins)"
                  type="number"
                  min="0"
                  prepend-inner-icon="mdi-calendar-today"
                  variant="outlined"
                  hint="0 = no limit"
                  persistent-hint
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="settings.weekly_limit"
                  label="Weekly limit (coins)"
                  type="number"
                  min="0"
                  prepend-inner-icon="mdi-calendar-week"
                  variant="outlined"
                  hint="0 = no limit"
                  persistent-hint
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="settings.monthly_limit"
                  label="Monthly limit (coins)"
                  type="number"
                  min="0"
                  prepend-inner-icon="mdi-calendar-month"
                  variant="outlined"
                  hint="0 = no limit"
                  persistent-hint
                />
              </v-col>
            </v-row>
            
            <v-divider class="my-4" />
            
            <v-switch
              v-model="settings.allow_savings_override"
              label="Allow exceeding limits for savings goals"
              color="primary"
              class="mb-2"
            />
            
            <v-switch
              v-model="settings.track_spending_categories"
              label="Track spending by categories"
              color="primary"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Redemption History -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="info">mdi-history</v-icon>
            Recent Redemption Requests
            <v-spacer />
            <v-btn
              variant="text"
              size="small"
              append-icon="mdi-arrow-right"
              @click="viewFullHistory"
            >
              View All
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="redemptionHeaders as any"
              :items="recentRedemptions"
              item-value="id"
              class="elevation-0"
              :items-per-page="5"
            >
              <template #item.child="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" :color="item.childColor" class="me-3">
                    <span class="text-caption text-white">{{ item.childInitials }}</span>
                  </v-avatar>
                  <div>
                    <div class="font-weight-medium">{{ item.child }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.childAge }} years old</div>
                  </div>
                </div>
              </template>

              <template #item.amount="{ item }">
                <div class="d-flex align-center">
                  <v-icon color="warning" size="small" class="me-1">mdi-star</v-icon>
                  <span class="font-weight-medium">{{ item.coins }}</span>
                  <span class="text-medium-emphasis ms-1">
                    ({{ formatCurrency(item.coins * settings.exchange_rate) }})
                  </span>
                </div>
              </template>

              <template #item.status="{ item }">
                <v-chip :color="getStatusColor(item.status)" size="small">
                  {{ item.status }}
                </v-chip>
              </template>

              <template #item.requestDate="{ item }">
                {{ formatDate(item.requestDate) }}
              </template>

              <template #item.actions="{ item }">
                <div v-if="item.status === 'Pending'" class="d-flex gap-1">
                  <v-btn
                    color="success"
                    size="small"
                    variant="tonal"
                    @click="approveRedemption(_item)"
                  >
                    Approve
                  </v-btn>
                  <v-btn
                    color="error"
                    size="small"
                    variant="tonal"
                    @click="rejectRedemption(_item)"
                  >
                    Reject
                  </v-btn>
                </div>
                <v-chip v-else size="small" variant="outlined">
                  {{ item.status }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Payment Methods -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="blue">mdi-credit-card</v-icon>
            Payment Methods
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="method in paymentMethods"
                :key="method.id"
              >
                <template #prepend>
                  <v-icon :color="method.color">{{ method.icon }}</v-icon>
                </template>
                <v-list-item-title>{{ method.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ method.description }}</v-list-item-subtitle>
                <template #append>
                  <v-switch
                    v-model="method.enabled"
                    density="compact"
                    hide-details
                  />
                </template>
              </v-list-item>
            </v-list>
            
            <v-divider class="my-3" />
            
            <v-btn
              block
              color="primary"
              variant="tonal"
              prepend-icon="mdi-plus"
              @click="addPaymentMethod"
            >
              Add Payment Method
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Spending Analytics -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="teal">mdi-chart-line</v-icon>
            Spending Analytics
          </v-card-title>
          <v-card-text>
            <div class="text-subtitle-2 mb-3">This Month</div>
            
            <v-row class="mb-3">
              <v-col cols="6">
                <div class="text-h6 font-weight-bold text-success">
                  {{ formatCurrency(analytics.totalRedeemed) }}
                </div>
                <div class="text-caption text-medium-emphasis">Total Redeemed</div>
              </v-col>
              <v-col cols="6">
                <div class="text-h6 font-weight-bold text-info">
                  {{ analytics.redemptionCount }}
                </div>
                <div class="text-caption text-medium-emphasis">Transactions</div>
              </v-col>
            </v-row>
            
            <div class="text-body-2 mb-2">Top Categories</div>
            <v-list density="compact">
              <v-list-item
                v-for="category in analytics.topCategories"
                :key="category.name"
                density="compact"
              >
                <v-list-item-title class="text-body-2">{{ category.name }}</v-list-item-title>
                <template #append>
                  <span class="text-body-2 font-weight-medium">
                    {{ formatCurrency(category.amount) }}
                  </span>
                </template>
              </v-list-item>
            </v-list>
            
            <v-btn
              block
              variant="tonal"
              prepend-icon="mdi-chart-bar"
              class="mt-3"
              @click="viewAnalytics"
            >
              View Detailed Analytics
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSuccessSnackbar"
      color="success"
      timeout="3000"
    >
      {{ successMessage }}
      <template #actions>
        <v-btn
          variant="text"
          @click="showSuccessSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useParentStore } from '@/stores/parent'
import type { RedemptionSettings } from '@/types'

const router = useRouter()
const parentStore = useParentStore()

// Reactive data
const saving = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')

// Settings data
const settings = reactive<RedemptionSettings>({
  exchange_rate: 0.10,
  currency: 'USD',
  require_approval: false,
  auto_approval_limit: 50,
  notify_on_request: true,
  processing_time: 'Within 24 hours',
  daily_limit: 100,
  weekly_limit: 300,
  monthly_limit: 1000,
  allow_savings_override: true,
  track_spending_categories: true
})

// Helper function to get child color consistently
const getChildColor = (childId: string): string => {
  const colors = ['purple', 'blue', 'green', 'orange', 'red', 'teal']
  const index = Math.abs(childId.split('').reduce((a, b) => a + b.charCodeAt(0), 0)) % colors.length
  return colors[index] || 'grey'
}

// Real data from parent store
const recentRedemptions = computed(() => 
  parentStore.redemptionRequests.map(request => {
    const child = parentStore.children.find(c => c.id === request.user_id)
    return {
      id: request.id,
      child: child?.name || 'Unknown Child',
      childInitials: child?.name?.charAt(0).toUpperCase() || 'U',
      childColor: getChildColor(request.user_id),
      childAge: child?.age || 0,
      coins: request.coins_amount || 0,
      description: request.description || 'Redemption request',
      status: request.status === 'pending' ? 'Pending' : 
              request.status === 'approved' ? 'Approved' :
              request.status === 'completed' ? 'Completed' : 'Rejected',
      requestDate: new Date(request.created_at),
      category: request.description?.split(' ')[0] || 'General'
    }
  })
)

// Analytics computed from real data
const analytics = computed(() => {
  const completedRedemptions = parentStore.redemptionRequests.filter(r => r.status === 'completed')
  const totalRedeemed = completedRedemptions.reduce((sum, r) => sum + (r.coins_amount || 0), 0) * settings.exchange_rate
  
  // Group by category for top categories
  const categoryTotals: Record<string, number> = {}
  completedRedemptions.forEach(r => {
    const category = r.description?.split(' ')[0] || 'General'
    const amount = (r.coins_amount || 0) * settings.exchange_rate
    categoryTotals[category] = (categoryTotals[category] || 0) + amount
  })
  
  const topCategories = Object.entries(categoryTotals)
    .map(([name, amount]) => ({ name, amount }))
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 4)
  
  return {
    totalRedeemed,
    redemptionCount: completedRedemptions.length,
    topCategories
  }
})

const paymentMethods = ref([
  {
    id: '1',
    name: 'Cash',
    description: 'Direct cash payment',
    icon: 'mdi-cash',
    color: 'green',
    enabled: true
  },
  {
    id: '2',
    name: 'Digital Transfer',
    description: 'Bank transfer or digital wallet',
    icon: 'mdi-bank-transfer',
    color: 'blue',
    enabled: true
  },
  {
    id: '3',
    name: 'Gift Cards',
    description: 'Store gift cards or vouchers',
    icon: 'mdi-gift',
    color: 'purple',
    enabled: false
  },
  {
    id: '4',
    name: 'Experience Rewards',
    description: 'Trips, activities, or experiences',
    icon: 'mdi-airplane',
    color: 'orange',
    enabled: true
  }
])

// Static data
const currencies = ['INR', 'USD', 'EUR', 'GBP', 'CAD', 'AUD']
const processingTimes = [
  'Immediately',
  'Within 1 hour',
  'Within 24 hours',
  'Within 2-3 days',
  'Within a week'
]

const redemptionHeaders = [
  { title: 'Child', key: 'child', sortable: true },
  { title: 'Amount', key: 'amount', sortable: true },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Requested', key: 'requestDate', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'center' }
]

// Validation rules
const rules = {
  required: (value: any) => !!value || 'This field is required',
  positive: (value: number) => value > 0 || 'Must be greater than 0'
}

// Methods
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: settings.currency
  }).format(amount)
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  }).format(date)
}

const getStatusColor = (status: string) => {
  const colors = {
    'Pending': 'warning',
    'Approved': 'info',
    'Completed': 'success',
    'Rejected': 'error'
  }
  return colors[status as keyof typeof colors] || 'grey'
}

const approveRedemption = async (item: any) => {
  try {
    const success = await parentStore.approveRedemption(item.id)
    if (success) {
      showSuccessSnackbar.value = true
      successMessage.value = `Redemption for ${item.child} approved!`
    } else {
      throw new Error('Failed to approve redemption')
    }
  } catch (error: any) {
    console.error('Failed to approve redemption:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Error: ${error.message || 'Failed to approve redemption'}`
  }
}

const rejectRedemption = async (item: any) => {
  try {
    const success = await parentStore.rejectRedemption(item.id)
    if (success) {
      showSuccessSnackbar.value = true
      successMessage.value = `Redemption for ${item.child} rejected.`
    } else {
      throw new Error('Failed to reject redemption')
    }
  } catch (error: any) {
    console.error('Failed to reject redemption:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Error: ${error.message || 'Failed to reject redemption'}`
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    // Simulate saving settings
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showSuccessSnackbar.value = true
    successMessage.value = 'Settings saved successfully!'
  } catch (error) {
    console.error('Failed to save settings:', error)
  } finally {
    saving.value = false
  }
}

const addPaymentMethod = () => {
  showSuccessSnackbar.value = true
  successMessage.value = 'Payment method configuration coming soon!'
}

const viewFullHistory = () => {
  router.push('/parent/redemption-history')
}

const viewAnalytics = () => {
  router.push('/parent/analytics')
}

// Lifecycle
onMounted(async () => {
  // Load redemption settings and data
  try {
    await Promise.all([
      parentStore.loadDashboard(),
      parentStore.loadRedemptions()
    ])
  } catch (error) {
    console.error('Failed to load data:', error)
    showSuccessSnackbar.value = true
    successMessage.value = 'Failed to load data. Please refresh the page.'
  }
})
</script>

