<template>
  <div class="dashboard">
    <!-- Add Child Form -->
    <div class="add-child-form">
      <h1 class="text-2xl font-bold p-2 text-blue-600">Add New Child</h1>
      <form @submit.prevent="addChild" novalidate>
        <div class="form-group">
          <label>
            👤 Child's Name:
            <input v-model="newChild.name" type="text" required />
          </label>
        </div>

        <div class="form-group">
          <label>
            🎂 Age:
            <input v-model.number="newChild.age" type="number" min="3" max="18" required />
          </label>
        </div>

        <div class="form-group">
          <label>
            📧 Email (Optional):
            <input v-model="newChild.email" type="email" />
          </label>
        </div>

        <div class="form-group">
          <label>
            🎨 Avatar Color:
            <select v-model="newChild.avatarColor">
              <option v-for="color in avatarColors" :key="color" :value="color">
                {{ color }}
              </option>
            </select>
          </label>
        </div>

        <div class="form-actions">
          <button type="button" @click="resetForm">Cancel</button>
          <button type="submit" :disabled="!childFormValid || loading">Add Child</button>
        </div>
      </form>
    </div>

    <!-- Child List Display -->
    <div class="table-container">
      <h2>Children List</h2>

      <table v-if="children.length">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Age</th>
            <th>Email</th>
            <th>Avatar Color</th>
            <th>Username</th>
            <th>Password</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(child, index) in children" :key="child.id">
            <td>{{ index + 1 }}</td>
            <td>{{ child.name }}</td>
            <td>{{ child.age }}</td>
            <td>{{ child.email || '—' }}</td>
            <td>{{ child.avatarColor }}</td>
            <td>{{ child.name.toLowerCase() }}{{ child.age }}</td>
            <td>{{ child.password }}</td>
          </tr>
        </tbody>
      </table>

      <p v-else>No children added yet.</p>
    </div>

    <!-- Success Snackbar -->
    <div v-if="showSuccessSnackbar" class="snackbar">
      <span>{{ successMessage }}</span>
      <button @click="showSuccessSnackbar = false">✖</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import type { Parent, Child} from '@/types'




const children = ref<Child[]>([])
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const loading = ref(false)

const avatarColors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']

const newChild = reactive({
  name: '',
  age: null as number | null,
  email: '',
  avatarColor: 'Blue',
  password: ''
})

const childFormValid = computed(() => {
  return (
    newChild.name.trim() !== '' &&
    newChild.age !== null &&
    newChild.age >= 3 &&
    newChild.age <= 18
  )
})

const parent = ref<Parent>({
  id: '1',
  name: 'Priya',
  email: 'priya@example.com',
  children: [],
  createdAt: new Date(),
  updatedAt: new Date(),
  role: 'parent',
})

function resetForm() {
  newChild.name = ''
  newChild.age = null
  newChild.email = ''
  newChild.avatarColor = 'Blue'
  newChild.password = ''
}

function generateRandomPassword(length = 10): string {
  const chars =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+[]{}<>?'
  let password = ''
  for (let i = 0; i < length; i++) {
    password += chars[Math.floor(Math.random() * chars.length)]
  }
  return password
}

async function addChild() {
  if (!childFormValid.value) return
  loading.value = true

  try {
    await new Promise(resolve => setTimeout(resolve, 500)) // simulate delay

    const password = generateRandomPassword(12)

    const child: Child = {
      id: Date.now().toString(),
      name: newChild.name,
      age: newChild.age!,
      email: newChild.email || undefined,
      initials: newChild.name.charAt(0).toUpperCase(),
      avatarColor: newChild.avatarColor,
      password,
      coinBalance: 0,
      completedTasks: 0,
      currentGoals: [],
      recentActivity: [],
      parentId: parent.value.id,
      createdAt: new Date(),
      updatedAt: new Date()
    }

    children.value.push(child)
    showSuccessSnackbar.value = true
    successMessage.value = `${child.name} added successfully!`
    resetForm()
  } catch (err) {
    console.error('Failed to add child:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 700px;
  margin: 2rem auto;
  font-family: sans-serif;
}

.add-child-form {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  margin-bottom: 2rem;
  width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  margin-top: 0.25rem;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}

.table-container {
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #eee;
}

th,
td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}

th {
  font-weight: bold;
  text-align: left;
}

.snackbar {
  position: fixed;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  background-color: #4caf50;
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
}
</style>
