import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'

export interface Student {
  id: string
  name: string
  avatar: string
  grade: number
  performance: number
  needsSupport: boolean
  lastActivity: Date
  progress: {
    [moduleId: string]: {
      completed: boolean
      score: number
      timeSpent: number
    }
  }
}

export interface Class {
  id: string
  name: string
  grade: number
  students: Student[]
  averagePerformance: number
  modules: string[]
  createdAt: Date
}

export interface Module {
  id: string
  title: string
  description: string
  content: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: number
  skills: string[]
  ageGroup: string
  category: string
  published: boolean
  createdBy: string
  createdAt: Date
  updatedAt: Date
}

export interface TeacherProfile {
  id: string
  name: string
  email: string
  school: string
  avatar: string
  classes: Class[]
}

export const useTeacherStore = defineStore('teacher', () => {
  // State
  const profile = ref<TeacherProfile | null>(null)
  const classes = ref<Class[]>([])
  const modules = ref<Module[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Demo data for development
  const demoClasses: Class[] = [
    {
      id: '1',
      name: 'Financial Literacy 101',
      grade: 6,
      students: [
        {
          id: '1',
          name: 'Emma Johnson',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight&accessoriesType=Blank&hairColor=BrownDark&facialHairType=Blank&clotheType=BlazerShirt&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light',
          grade: 6,
          performance: 85,
          needsSupport: false,
          lastActivity: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
          progress: {
            'mod1': { completed: true, score: 90, timeSpent: 45 },
            'mod2': { completed: true, score: 80, timeSpent: 30 },
            'mod3': { completed: false, score: 0, timeSpent: 10 }
          }
        },
        {
          id: '2',
          name: 'Liam Smith',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortRound&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=Blue01&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light',
          grade: 6,
          performance: 65,
          needsSupport: true,
          lastActivity: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
          progress: {
            'mod1': { completed: true, score: 70, timeSpent: 60 },
            'mod2': { completed: false, score: 60, timeSpent: 20 },
            'mod3': { completed: false, score: 0, timeSpent: 0 }
          }
        },
        {
          id: '3',
          name: 'Olivia Davis',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairCurly&accessoriesType=Blank&hairColor=Blonde&facialHairType=Blank&clotheType=GraphicShirt&clotheColor=Pink&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light',
          grade: 6,
          performance: 92,
          needsSupport: false,
          lastActivity: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
          progress: {
            'mod1': { completed: true, score: 95, timeSpent: 40 },
            'mod2': { completed: true, score: 90, timeSpent: 35 },
            'mod3': { completed: true, score: 85, timeSpent: 45 }
          }
        }
      ],
      averagePerformance: 80.7,
      modules: ['mod1', 'mod2', 'mod3'],
      createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    },
    {
      id: '2',
      name: 'Money Management',
      grade: 7,
      students: [
        {
          id: '4',
          name: 'Noah Wilson',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortWaved&accessoriesType=Blank&hairColor=Brown&facialHairType=BeardLight&facialHairColor=Brown&clotheType=CollarSweater&clotheColor=Gray01&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light',
          grade: 7,
          performance: 78,
          needsSupport: false,
          lastActivity: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
          progress: {
            'mod4': { completed: true, score: 80, timeSpent: 50 },
            'mod5': { completed: false, score: 75, timeSpent: 25 }
          }
        },
        {
          id: '5',
          name: 'Ava Brown',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight2&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=ShirtCrewNeck&clotheColor=Red&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Brown',
          grade: 7,
          performance: 60,
          needsSupport: true,
          lastActivity: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
          progress: {
            'mod4': { completed: true, score: 65, timeSpent: 70 },
            'mod5': { completed: false, score: 55, timeSpent: 15 }
          }
        }
      ],
      averagePerformance: 69,
      modules: ['mod4', 'mod5'],
      createdAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000)
    },
    {
      id: '3',
      name: 'Investment Basics',
      grade: 8,
      students: [
        {
          id: '6',
          name: 'Ethan Miller',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairTheCaesar&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=ShirtVNeck&clotheColor=Blue03&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Pale',
          grade: 8,
          performance: 88,
          needsSupport: false,
          lastActivity: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
          progress: {
            'mod6': { completed: true, score: 90, timeSpent: 40 },
            'mod7': { completed: true, score: 85, timeSpent: 45 }
          }
        },
        {
          id: '7',
          name: 'Mia Garcia',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairMiaWallace&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=Overall&clotheColor=Blue03&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Tanned',
          grade: 8,
          performance: 95,
          needsSupport: false,
          lastActivity: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
          progress: {
            'mod6': { completed: true, score: 95, timeSpent: 35 },
            'mod7': { completed: true, score: 95, timeSpent: 40 }
          }
        },
        {
          id: '8',
          name: 'Lucas Martinez',
          avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortCurly&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=BlazerShirt&clotheColor=Black&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=DarkBrown',
          grade: 8,
          performance: 72,
          needsSupport: true,
          lastActivity: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
          progress: {
            'mod6': { completed: true, score: 75, timeSpent: 55 },
            'mod7': { completed: false, score: 70, timeSpent: 30 }
          }
        }
      ],
      averagePerformance: 85,
      modules: ['mod6', 'mod7'],
      createdAt: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000)
    }
  ]

  const demoModules: Module[] = [
    {
      id: 'mod1',
      title: 'Introduction to Money',
      description: 'Learn the basics of money, its history, and importance in society.',
      content: 'Comprehensive introduction to money concepts...',
      difficulty: 'beginner',
      duration: 30,
      skills: ['Basic Money Concepts', 'History of Currency'],
      ageGroup: '10-12',
      category: 'Financial Literacy',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod2',
      title: 'Saving Basics',
      description: 'Understand the importance of saving and different saving strategies.',
      content: 'Detailed explanation of saving concepts...',
      difficulty: 'beginner',
      duration: 45,
      skills: ['Saving Strategies', 'Goal Setting'],
      ageGroup: '10-12',
      category: 'Financial Literacy',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 55 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod3',
      title: 'Needs vs Wants',
      description: 'Learn to differentiate between needs and wants for better financial decisions.',
      content: 'Interactive lessons on needs vs wants...',
      difficulty: 'beginner',
      duration: 35,
      skills: ['Decision Making', 'Budgeting Basics'],
      ageGroup: '10-12',
      category: 'Financial Literacy',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 50 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod4',
      title: 'Budgeting Fundamentals',
      description: 'Learn how to create and maintain a personal budget.',
      content: 'Step-by-step guide to budgeting...',
      difficulty: 'intermediate',
      duration: 60,
      skills: ['Budgeting', 'Financial Planning'],
      ageGroup: '12-14',
      category: 'Money Management',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod5',
      title: 'Smart Shopping',
      description: 'Develop skills to make informed purchasing decisions.',
      content: 'Techniques for smart shopping...',
      difficulty: 'intermediate',
      duration: 40,
      skills: ['Comparison Shopping', 'Value Assessment'],
      ageGroup: '12-14',
      category: 'Money Management',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod6',
      title: 'Introduction to Investing',
      description: 'Learn the basics of investing and different investment options.',
      content: 'Fundamentals of investing...',
      difficulty: 'advanced',
      duration: 75,
      skills: ['Investment Basics', 'Risk Management'],
      ageGroup: '14-16',
      category: 'Investing',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000)
    },
    {
      id: 'mod7',
      title: 'Stock Market Basics',
      description: 'Understand how the stock market works and how to analyze stocks.',
      content: 'Introduction to stock market concepts...',
      difficulty: 'advanced',
      duration: 90,
      skills: ['Stock Analysis', 'Market Understanding'],
      ageGroup: '14-16',
      category: 'Investing',
      published: true,
      createdBy: 'teacher1',
      createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000)
    }
  ]

  // Getters
  const getClassById = (classId: string) => {
    return classes.value.find(c => c.id === classId)
  }

  const getModuleById = (moduleId: string) => {
    return modules.value.find(m => m.id === moduleId)
  }

  const getStudentsNeedingSupport = (classId: string) => {
    const classData = getClassById(classId)
    return classData ? classData.students.filter(s => s.needsSupport) : []
  }

  const getModulesByCategory = (category: string) => {
    return modules.value.filter(m => m.category === category)
  }

  const getModulesByDifficulty = (difficulty: 'beginner' | 'intermediate' | 'advanced') => {
    return modules.value.filter(m => m.difficulty === difficulty)
  }

  const getClassPerformanceData = (classId: string) => {
    const classData = getClassById(classId)
    if (!classData) return null

    // Calculate performance distribution
    const performanceRanges = {
      excellent: 0, // 90-100
      good: 0,      // 75-89
      average: 0,   // 60-74
      needsHelp: 0  // <60
    }

    classData.students.forEach(student => {
      if (student.performance >= 90) performanceRanges.excellent++
      else if (student.performance >= 75) performanceRanges.good++
      else if (student.performance >= 60) performanceRanges.average++
      else performanceRanges.needsHelp++
    })

    return {
      averagePerformance: classData.averagePerformance,
      totalStudents: classData.students.length,
      performanceDistribution: performanceRanges,
      moduleCompletionRate: calculateModuleCompletionRate(classData)
    }
  }

  const calculateModuleCompletionRate = (classData: Class) => {
    const moduleCompletionRates: { [moduleId: string]: number } = {}
    
    classData.modules.forEach(moduleId => {
      let completedCount = 0
      
      classData.students.forEach(student => {
        if (student.progress[moduleId]?.completed) {
          completedCount++
        }
      })
      
      moduleCompletionRates[moduleId] = (completedCount / classData.students.length) * 100
    })
    
    return moduleCompletionRates
  }

  // Actions
  const loadTeacherProfile = async () => {
    isLoading.value = true
    error.value = null

    try {
      console.log('👨‍🏫 [TEACHER] Loading teacher profile...')
      
      // For now, use demo data until we implement teacher-specific API methods
      console.log('📊 [TEACHER] Using demo data for now...')
      
      // Update profile with demo data
      profile.value = {
        id: 'teacher1',
        name: 'Mrs. Johnson',
        email: 'teacher@demo.com',
        school: 'Financial Literacy Academy',
        avatar: 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=BlazerShirt&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light',
        classes: []
      }

      // Update classes with demo data
      classes.value = demoClasses
      modules.value = demoModules

      console.log('✅ [TEACHER] Demo profile loaded successfully')
    } catch (err) {
      console.error('❌ [TEACHER] Failed to load profile:', err)
      error.value = err instanceof Error ? err.message : 'Failed to load profile'
    } finally {
      isLoading.value = false
    }
  }

  const addClass = async (classData: Omit<Class, 'id' | 'createdAt' | 'averagePerformance'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Calculate average performance
      const totalPerformance = classData.students.reduce((sum, student) => sum + student.performance, 0)
      const averagePerformance = classData.students.length > 0 
        ? totalPerformance / classData.students.length 
        : 0
      
      const newClass: Class = {
        id: Date.now().toString(),
        ...classData,
        averagePerformance,
        createdAt: new Date()
      }
      
      classes.value.push(newClass)
      return newClass
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add class'
      console.error('Error adding class:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateClass = async (classId: string, updates: Partial<Omit<Class, 'id' | 'createdAt'>>) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const classIndex = classes.value.findIndex(c => c.id === classId)
      if (classIndex === -1) throw new Error('Class not found')
      
      // If students are updated, recalculate average performance
      if (updates.students) {
        const totalPerformance = updates.students.reduce((sum, student) => sum + student.performance, 0)
        updates.averagePerformance = updates.students.length > 0 
          ? totalPerformance / updates.students.length 
          : 0
      }
      
      classes.value[classIndex] = { ...classes.value[classIndex], ...updates }
      return classes.value[classIndex]
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update class'
      console.error('Error updating class:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteClass = async (classId: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const classIndex = classes.value.findIndex(c => c.id === classId)
      if (classIndex === -1) throw new Error('Class not found')
      
      classes.value.splice(classIndex, 1)
      return true
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete class'
      console.error('Error deleting class:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const addModule = async (moduleData: Omit<Module, 'id' | 'createdAt' | 'updatedAt'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newModule: Module = {
        id: `mod${modules.value.length + 1}`,
        ...moduleData,
        createdAt: new Date(),
        updatedAt: new Date()
      }
      
      modules.value.push(newModule)
      return newModule
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add module'
      console.error('Error adding module:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateModule = async (moduleId: string, updates: Partial<Omit<Module, 'id' | 'createdAt'>>) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const moduleIndex = modules.value.findIndex(m => m.id === moduleId)
      if (moduleIndex === -1) throw new Error('Module not found')
      
      modules.value[moduleIndex] = { 
        ...modules.value[moduleIndex], 
        ...updates,
        updatedAt: new Date()
      }
      
      return modules.value[moduleIndex]
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update module'
      console.error('Error updating module:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteModule = async (moduleId: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const moduleIndex = modules.value.findIndex(m => m.id === moduleId)
      if (moduleIndex === -1) throw new Error('Module not found')
      
      // Check if module is assigned to any class
      const isAssigned = classes.value.some(c => c.modules.includes(moduleId))
      if (isAssigned) {
        throw new Error('Cannot delete module that is assigned to classes')
      }
      
      modules.value.splice(moduleIndex, 1)
      return true
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete module'
      console.error('Error deleting module:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const assignModuleToClass = async (moduleId: string, classId: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const classIndex = classes.value.findIndex(c => c.id === classId)
      if (classIndex === -1) throw new Error('Class not found')
      
      const moduleIndex = modules.value.findIndex(m => m.id === moduleId)
      if (moduleIndex === -1) throw new Error('Module not found')
      
      // Check if module is already assigned
      if (classes.value[classIndex].modules.includes(moduleId)) {
        throw new Error('Module already assigned to this class')
      }
      
      // Add module to class
      classes.value[classIndex].modules.push(moduleId)
      
      // Initialize progress tracking for all students
      classes.value[classIndex].students.forEach(student => {
        if (!student.progress[moduleId]) {
          student.progress[moduleId] = {
            completed: false,
            score: 0,
            timeSpent: 0
          }
        }
      })
      
      return classes.value[classIndex]
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to assign module'
      console.error('Error assigning module:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const addStudentToClass = async (classId: string, studentData: Omit<Student, 'id'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const classIndex = classes.value.findIndex(c => c.id === classId)
      if (classIndex === -1) throw new Error('Class not found')
      
      const newStudent: Student = {
        id: Date.now().toString(),
        ...studentData
      }
      
      // Initialize progress for all modules in the class
      classes.value[classIndex].modules.forEach(moduleId => {
        if (!newStudent.progress[moduleId]) {
          newStudent.progress[moduleId] = {
            completed: false,
            score: 0,
            timeSpent: 0
          }
        }
      })
      
      // Add student to class
      classes.value[classIndex].students.push(newStudent)
      
      // Recalculate average performance
      const totalPerformance = classes.value[classIndex].students.reduce(
        (sum, student) => sum + student.performance, 0
      )
      classes.value[classIndex].averagePerformance = 
        totalPerformance / classes.value[classIndex].students.length
      
      return newStudent
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add student'
      console.error('Error adding student:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateStudentProgress = async (
    classId: string, 
    studentId: string, 
    moduleId: string, 
    progress: { completed?: boolean; score?: number; timeSpent?: number }
  ) => {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const classIndex = classes.value.findIndex(c => c.id === classId)
      if (classIndex === -1) throw new Error('Class not found')
      
      const studentIndex = classes.value[classIndex].students.findIndex(s => s.id === studentId)
      if (studentIndex === -1) throw new Error('Student not found')
      
      if (!classes.value[classIndex].modules.includes(moduleId)) {
        throw new Error('Module not assigned to this class')
      }
      
      // Update student progress
      const currentProgress = classes.value[classIndex].students[studentIndex].progress[moduleId] || {
        completed: false,
        score: 0,
        timeSpent: 0
      }
      
      classes.value[classIndex].students[studentIndex].progress[moduleId] = {
        ...currentProgress,
        ...progress
      }
      
      // Update student performance based on all module scores
      const studentModules = Object.values(classes.value[classIndex].students[studentIndex].progress)
      const completedModules = studentModules.filter(m => m.completed)
      
      if (completedModules.length > 0) {
        const totalScore = completedModules.reduce((sum, m) => sum + m.score, 0)
        classes.value[classIndex].students[studentIndex].performance = 
          totalScore / completedModules.length
      }
      
      // Recalculate class average performance
      const totalPerformance = classes.value[classIndex].students.reduce(
        (sum, student) => sum + student.performance, 0
      )
      classes.value[classIndex].averagePerformance = 
        totalPerformance / classes.value[classIndex].students.length
      
      return classes.value[classIndex].students[studentIndex]
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update student progress'
      console.error('Error updating student progress:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    profile,
    classes,
    modules,
    isLoading,
    error,
    
    // Getters
    getClassById,
    getModuleById,
    getStudentsNeedingSupport,
    getModulesByCategory,
    getModulesByDifficulty,
    getClassPerformanceData,
    
    // Actions
    loadTeacherProfile,
    addClass,
    updateClass,
    deleteClass,
    addModule,
    updateModule,
    deleteModule,
    assignModuleToClass,
    addStudentToClass,
    updateStudentProgress,
    clearError
  }
})