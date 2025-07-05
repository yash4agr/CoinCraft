export interface User {
  id: string
  name: string
  email: string
  role: 'child' | 'parent' | 'teacher'
  avatar?: string
  createdAt: Date
  updatedAt: Date
}

export interface Child extends User {
  age: number
  coins: number
  level: number
  parentId: string
  classId?: string
}

export interface Parent extends User {
  children: string[] // child IDs
}

export interface Teacher extends User {
  classes: string[] // class IDs
}

export interface Transaction {
  id: string
  userId: string
  type: 'earn' | 'spend' | 'transfer'
  amount: number
  description: string
  category: string
  source: string
  createdAt: Date
}

export interface Goal {
  id: string
  userId: string
  title: string
  description: string
  targetAmount: number
  currentAmount: number
  icon: string
  color: string
  deadline?: Date
  completed: boolean
  createdAt: Date
  updatedAt: Date
}

export interface Task {
  id: string
  title: string
  description: string
  reward: number
  assignedBy: string
  assignedTo: string
  status: 'pending' | 'in-progress' | 'completed' | 'approved'
  dueDate?: Date
  requiresApproval: boolean
  createdAt: Date
  updatedAt: Date
}

export interface Notification {
  id: string
  userId: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  read: boolean
  actionUrl?: string
  createdAt: Date
}

export interface Module {
  id: string
  title: string
  description: string
  content: string
  ageGroup: string
  duration: number
  skills: string[]
  reward: number
  createdBy: string
  published: boolean
  createdAt: Date
  updatedAt: Date
}

export interface Class {
  id: string
  name: string
  teacherId: string
  students: string[]
  modules: string[]
  createdAt: Date
}

export interface ShopItem {
  id: string
  name: string
  description: string
  price: number
  category: string
  icon: string
  color: string
  available: boolean
  createdAt: Date
}

export interface Budget {
  id: string
  userId: string
  saving: number
  spending: number
  wants: number
  totalAmount: number
  updatedAt: Date
}

export interface ActivityProgress {
  id: string
  userId: string
  moduleId: string
  progress: number
  completed: boolean
  score?: number
  timeSpent: number
  startedAt: Date
  completedAt?: Date
}

export interface FilterOptions {
  dateRange?: {
    start: Date
    end: Date
  }
  category?: string
  type?: string
  amount?: {
    min: number
    max: number
  }
}

export interface SortOptions {
  field: string
  direction: 'asc' | 'desc'
}

export interface PaginationOptions {
  page: number
  limit: number
  total: number
}