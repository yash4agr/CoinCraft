import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Child {
  id: string
  name: string
  age: number
  coins: number
  goalsActive: number
  lastActivity: Date
  avatar: string
}

export interface Task {
  id: string
  childId: string
  description: string
  coins: number
  dueDate?: Date
  completed: boolean
  requiresApproval: boolean
  createdAt: Date
}

export interface RedemptionRequest {
  id: string
  childId: string
  childName: string
  amount: number
  coins: number
  status: 'pending' | 'approved' | 'rejected'
  createdAt: Date
}

export const useParentStore = defineStore('parent', () => {
  const children = ref<Child[]>([
    {
      id: '1',
      name: 'Luna',
      age: 9,
      coins: 135,
      goalsActive: 2,
      lastActivity: new Date(Date.now() - 7200000),
      avatar: '👧'
    },
    {
      id: '2',
      name: 'Harry',
      age: 12,
      coins: 245,
      goalsActive: 1,
      lastActivity: new Date(Date.now() - 86400000),
      avatar: '👦'
    }
  ])

  const tasks = ref<Task[]>([
    {
      id: '1',
      childId: '1',
      description: 'Clean your room',
      coins: 15,
      completed: false,
      requiresApproval: true,
      createdAt: new Date(Date.now() - 86400000)
    }
  ])

  const redemptionRequests = ref<RedemptionRequest[]>([
    {
      id: '1',
      childId: '1',
      childName: 'Luna',
      amount: 2.50,
      coins: 25,
      status: 'approved',
      createdAt: new Date(Date.now() - 172800000)
    },
    {
      id: '2',
      childId: '2',
      childName: 'Harry',
      amount: 5.00,
      coins: 50,
      status: 'pending',
      createdAt: new Date(Date.now() - 86400000)
    }
  ])

  const exchangeRate = ref(0.10)
  const autoApproveLimit = ref(5)

  const addChild = (child: Omit<Child, 'id'>) => {
    children.value.push({
      ...child,
      id: Date.now().toString()
    })
  }

  const assignTask = (task: Omit<Task, 'id' | 'createdAt'>) => {
    tasks.value.push({
      ...task,
      id: Date.now().toString(),
      createdAt: new Date()
    })
  }

  const approveRedemption = (requestId: string) => {
    const request = redemptionRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'approved'
    }
  }

  const rejectRedemption = (requestId: string) => {
    const request = redemptionRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'rejected'
    }
  }

  return {
    children,
    tasks,
    redemptionRequests,
    exchangeRate,
    autoApproveLimit,
    addChild,
    assignTask,
    approveRedemption,
    rejectRedemption
  }
})
