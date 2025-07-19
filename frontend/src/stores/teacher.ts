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

export interface ModuleSection {
  title: string
  type: 'lesson' | 'reading' | 'video' | 'discussion'
  content: string
  duration: string
  orderIndex?: number
}

export interface ModuleActivity {
  title: string
  type: 'exercise' | 'simulation' | 'case_study' | 'group_work' | 'project'
  description: string
  duration: string
  materials?: string
}

export interface QuizQuestion {
  question: string
  type: 'multiple_choice' | 'true_false'
  options: {
    text: string
    isCorrect: boolean
  }[]
  explanation?: string
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
  // Enhanced content for try mode
  sections?: ModuleSection[]
  activities?: ModuleActivity[]
  quiz?: QuizQuestion[]
  // AI-generated content properties
  learningObjectives?: string[]
  prerequisites?: string[]
  keyTopics?: string[]
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
      updatedAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000),
      sections: [
        {
          title: 'What is Money?',
          type: 'lesson',
          content: 'Money is a medium of exchange that people use to buy goods and services. It has three main functions: as a medium of exchange, a unit of account, and a store of value.',
          duration: '10 minutes',
          orderIndex: 1
        },
        {
          title: 'History of Money',
          type: 'reading',
          content: 'Money has evolved from barter systems to coins, paper money, and now digital currency. Understanding this history helps us appreciate the importance of money in society.',
          duration: '8 minutes',
          orderIndex: 2
        },
        {
          title: 'Types of Money',
          type: 'discussion',
          content: 'Explore different types of money including cash, checks, credit cards, and digital payments. Discuss the advantages and disadvantages of each.',
          duration: '12 minutes',
          orderIndex: 3
        }
      ],
      activities: [
        {
          title: 'Money Timeline Activity',
          type: 'exercise',
          description: 'Create a timeline showing the evolution of money from barter to digital currency. Students research and present different forms of money throughout history.',
          duration: '15 minutes',
          materials: 'Paper, markers, internet access for research'
        },
        {
          title: 'Money Role Play',
          type: 'simulation',
          description: 'Students act out different scenarios using various forms of money to understand how transactions work in real life.',
          duration: '20 minutes',
          materials: 'Play money, props for different scenarios'
        }
      ],
      quiz: [
        {
          question: 'What are the three main functions of money?',
          type: 'multiple_choice',
          options: [
            { text: 'Medium of exchange, unit of account, store of value', isCorrect: true },
            { text: 'Buying, selling, saving', isCorrect: false },
            { text: 'Coins, paper, digital', isCorrect: false },
            { text: 'Earning, spending, investing', isCorrect: false }
          ],
          explanation: 'Money serves as a medium of exchange (for buying/selling), a unit of account (measuring value), and a store of value (saving for later).'
        },
        {
          question: 'Which form of money came first in human history?',
          type: 'multiple_choice',
          options: [
            { text: 'Paper money', isCorrect: false },
            { text: 'Digital currency', isCorrect: false },
            { text: 'Barter system', isCorrect: true },
            { text: 'Coins', isCorrect: false }
          ],
          explanation: 'Before money existed, people used barter - exchanging goods and services directly with each other.'
        },
        {
          question: 'Digital payments are more secure than cash transactions.',
          type: 'true_false',
          options: [
            { text: 'True', isCorrect: true },
            { text: 'False', isCorrect: false }
          ],
          explanation: 'Digital payments often have built-in security features like encryption and fraud protection that cash doesn\'t have.'
        }
      ]
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
      updatedAt: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000),
      sections: [
        {
          title: 'Why Save Money?',
          type: 'lesson',
          content: 'Saving money helps us prepare for emergencies, achieve goals, and build financial security. It\'s like building a safety net for the future.',
          duration: '12 minutes',
          orderIndex: 1
        },
        {
          title: 'Saving Strategies',
          type: 'reading',
          content: 'Learn about different saving strategies like the 50/30/20 rule, automatic transfers, and setting up emergency funds.',
          duration: '15 minutes',
          orderIndex: 2
        },
        {
          title: 'Goal Setting',
          type: 'discussion',
          content: 'Discuss how to set realistic saving goals and create a plan to achieve them. Short-term vs long-term goals.',
          duration: '18 minutes',
          orderIndex: 3
        }
      ],
      activities: [
        {
          title: 'Savings Goal Calculator',
          type: 'exercise',
          description: 'Students calculate how long it will take to save for different goals based on their income and expenses.',
          duration: '20 minutes',
          materials: 'Calculator, paper, savings goal worksheet'
        },
        {
          title: 'Piggy Bank Challenge',
          type: 'simulation',
          description: 'Students track their savings for a week using a virtual piggy bank and see how small amounts add up over time.',
          duration: '25 minutes',
          materials: 'Virtual piggy bank app or spreadsheet'
        }
      ],
      quiz: [
        {
          question: 'What percentage of your income should you save according to the 50/30/20 rule?',
          type: 'multiple_choice',
          options: [
            { text: '10%', isCorrect: false },
            { text: '20%', isCorrect: true },
            { text: '30%', isCorrect: false },
            { text: '50%', isCorrect: false }
          ],
          explanation: 'The 50/30/20 rule suggests 50% for needs, 30% for wants, and 20% for savings and debt repayment.'
        },
        {
          question: 'What is an emergency fund?',
          type: 'multiple_choice',
          options: [
            { text: 'Money saved for vacations', isCorrect: false },
            { text: 'Money saved for unexpected expenses', isCorrect: true },
            { text: 'Money invested in stocks', isCorrect: false },
            { text: 'Money spent on entertainment', isCorrect: false }
          ],
          explanation: 'An emergency fund is money set aside for unexpected expenses like medical bills or car repairs.'
        },
        {
          question: 'It\'s better to save a small amount regularly than to save a large amount occasionally.',
          type: 'true_false',
          options: [
            { text: 'True', isCorrect: true },
            { text: 'False', isCorrect: false }
          ],
          explanation: 'Regular saving builds good habits and compound interest works better with consistent contributions.'
        }
      ]
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
      updatedAt: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000),
      sections: [
        {
          title: 'Understanding Needs vs Wants',
          type: 'lesson',
          content: 'Needs are essential items required for survival and basic well-being (food, shelter, clothing). Wants are things we desire but can live without (entertainment, luxury items).',
          duration: '12 minutes',
          orderIndex: 1
        },
        {
          title: 'Examples and Categories',
          type: 'reading',
          content: 'Explore real-world examples of needs vs wants. Learn how to categorize different expenses and understand that wants can vary between individuals and cultures.',
          duration: '10 minutes',
          orderIndex: 2
        },
        {
          title: 'Decision Making Process',
          type: 'discussion',
          content: 'Discuss strategies for making smart financial decisions when choosing between needs and wants. Learn about opportunity cost and delayed gratification.',
          duration: '13 minutes',
          orderIndex: 3
        }
      ],
      activities: [
        {
          title: 'Needs vs Wants Sorting Game',
          type: 'exercise',
          description: 'Students sort various items into needs and wants categories, then discuss their reasoning with classmates.',
          duration: '15 minutes',
          materials: 'Picture cards of various items, sorting mats'
        },
        {
          title: 'Budget Decision Simulation',
          type: 'simulation',
          description: 'Students are given a limited budget and must prioritize needs over wants in various scenarios.',
          duration: '20 minutes',
          materials: 'Budget worksheets, scenario cards'
        }
      ],
      quiz: [
        {
          question: 'Which of the following is a need?',
          type: 'multiple_choice',
          options: [
            { text: 'New video game', isCorrect: false },
            { text: 'School supplies', isCorrect: true },
            { text: 'Movie tickets', isCorrect: false },
            { text: 'Designer clothes', isCorrect: false }
          ],
          explanation: 'School supplies are essential for education and learning, making them a need rather than a want.'
        },
        {
          question: 'What is opportunity cost?',
          type: 'multiple_choice',
          options: [
            { text: 'The price of an item', isCorrect: false },
            { text: 'What you give up when you choose one option over another', isCorrect: true },
            { text: 'The cost of borrowing money', isCorrect: false },
            { text: 'The amount you save', isCorrect: false }
          ],
          explanation: 'Opportunity cost is the value of what you give up when you choose one option over another.'
        },
        {
          question: 'All wants are bad and should be avoided.',
          type: 'true_false',
          options: [
            { text: 'True', isCorrect: false },
            { text: 'False', isCorrect: true }
          ],
          explanation: 'Wants aren\'t inherently bad - they can improve quality of life. The key is balancing needs and wants within your budget.'
        }
      ]
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
      updatedAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      sections: [
        {
          title: 'What is a Budget?',
          type: 'lesson',
          content: 'A budget is a financial plan that helps you track income and expenses. It\'s like a roadmap for your money that helps you achieve financial goals.',
          duration: '15 minutes',
          orderIndex: 1
        },
        {
          title: 'Creating Your First Budget',
          type: 'reading',
          content: 'Learn the step-by-step process of creating a budget: track income, list expenses, categorize spending, and set financial goals.',
          duration: '20 minutes',
          orderIndex: 2
        },
        {
          title: 'Budgeting Methods',
          type: 'discussion',
          content: 'Explore different budgeting methods like the 50/30/20 rule, envelope method, and zero-based budgeting. Discuss which method works best for different situations.',
          duration: '25 minutes',
          orderIndex: 3
        }
      ],
      activities: [
        {
          title: 'Personal Budget Creation',
          type: 'exercise',
          description: 'Students create their own personal budget using provided templates and real-world scenarios.',
          duration: '25 minutes',
          materials: 'Budget templates, calculators, sample income/expense data'
        },
        {
          title: 'Budget Tracking Challenge',
          type: 'simulation',
          description: 'Students track their spending for a week and compare it to their planned budget, learning about budget variance.',
          duration: '30 minutes',
          materials: 'Spending tracker worksheets, budget apps'
        }
      ],
      quiz: [
        {
          question: 'What is the first step in creating a budget?',
          type: 'multiple_choice',
          options: [
            { text: 'Set financial goals', isCorrect: false },
            { text: 'Track your income', isCorrect: true },
            { text: 'List all expenses', isCorrect: false },
            { text: 'Choose a budgeting method', isCorrect: false }
          ],
          explanation: 'The first step is to track your income - you need to know how much money you have coming in before you can plan how to spend it.'
        },
        {
          question: 'What percentage of your income should go to needs in the 50/30/20 rule?',
          type: 'multiple_choice',
          options: [
            { text: '20%', isCorrect: false },
            { text: '30%', isCorrect: false },
            { text: '50%', isCorrect: true },
            { text: '80%', isCorrect: false }
          ],
          explanation: 'In the 50/30/20 rule, 50% goes to needs, 30% to wants, and 20% to savings and debt repayment.'
        },
        {
          question: 'A budget should be flexible and adjusted as needed.',
          type: 'true_false',
          options: [
            { text: 'True', isCorrect: true },
            { text: 'False', isCorrect: false }
          ],
          explanation: 'Budgets should be flexible and adjusted as your financial situation changes. Regular review and updates are important.'
        }
      ]
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

  const addModule = async (moduleData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      console.log('💾 [TEACHER] Adding module via API:', moduleData)
      
      // Make actual API call to create module
      const response = await apiService.createModule(moduleData)
      console.log('✅ [TEACHER] Module saved successfully via API:', response)
      
      // Convert API response to Module format
      const savedModule = response.module
      const newModule: Module = {
        id: savedModule.id,
        title: savedModule.title,
        description: savedModule.description,
        content: savedModule.content || moduleData.content || '',
        difficulty: savedModule.difficulty,
        duration: savedModule.duration,
        skills: savedModule.skills || [],
        ageGroup: savedModule.ageGroup || '11-14',
        category: savedModule.category,
        published: savedModule.published,
        createdBy: savedModule.created_by || profile.value?.id || 'teacher1',
        createdAt: new Date(savedModule.created_at),
        updatedAt: new Date(savedModule.updated_at || savedModule.created_at),
        // Enhanced content for Try Mode
        sections: savedModule.sections || [],
        activities: savedModule.activities || [],
        quiz: savedModule.quiz || [],
        // AI-generated content properties
        learningObjectives: savedModule.learningObjectives || [],
        prerequisites: savedModule.prerequisites || [],
        keyTopics: savedModule.keyTopics || []
      }
      
      modules.value.push(newModule)
      return newModule
      
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Failed to add module'
      console.error('❌ [TEACHER] Error adding module:', err)
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

  const loadModules = async () => {
    isLoading.value = true
    error.value = null

    try {
      console.log('📚 [TEACHER] Loading modules from API...')
      
      // Fetch modules from API
      const apiModules = await apiService.getTeacherModules()
      console.log('🌐 [TEACHER] API modules received:', apiModules)
      
      // Convert API modules to Module format
      const convertedModules: Module[] = apiModules.map(apiModule => ({
        id: apiModule.id,
        title: apiModule.title,
        description: apiModule.description,
        content: apiModule.content || '',
        difficulty: apiModule.difficulty as 'beginner' | 'intermediate' | 'advanced',
        duration: apiModule.duration || 30,
        skills: apiModule.skills || [],
        ageGroup: apiModule.ageGroup || 'Unknown',
        category: apiModule.category || 'General',
        published: apiModule.published || false,
        createdBy: apiModule.created_by || 'unknown',
        createdAt: new Date(apiModule.created_at),
        updatedAt: new Date(apiModule.updated_at),
        // Enhanced content
        sections: apiModule.sections || [],
        activities: apiModule.activities || [],
        quiz: apiModule.quiz || [],
        // AI-generated content properties
        learningObjectives: apiModule.learningObjectives || [],
        prerequisites: apiModule.prerequisites || [],
        keyTopics: apiModule.keyTopics || []
      }))
      
      // Merge with existing demo modules (keep demo modules for now)
      const allModules = [...demoModules, ...convertedModules]
      modules.value = allModules
      
      console.log('✅ [TEACHER] Modules loaded successfully:', modules.value.length)
      console.log('📊 [TEACHER] - Demo modules:', demoModules.length)
      console.log('📊 [TEACHER] - API modules:', convertedModules.length)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load modules'
      console.error('❌ [TEACHER] Failed to load modules:', err)
      
      // Fallback to demo modules only
      console.log('🔄 [TEACHER] Falling back to demo modules only')
      modules.value = demoModules
      
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
    loadModules,
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